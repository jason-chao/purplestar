"""Offline place-of-birth → coordinates / timezone resolver.

Backed by the MIT-licensed ``geonamescache`` package (which bundles a
GeoNames snapshot). Lookup is exact / asciiname / alternate-name match,
case-insensitive. Ambiguous matches are resolved by:

  1. country-code filter (when the query is "City, CC"), then
  2. highest population.

Usage::

    from purplestar.core.geo import resolve_place
    m = resolve_place("Taipei, TW")
    if m:
        print(m.lat, m.lon, m.tz)
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class PlaceMatch:
    name: str
    country: str
    lat: float
    lon: float
    tz: str
    population: int


@lru_cache(maxsize=1)
def _cache():
    try:
        import geonamescache  # type: ignore
    except ImportError as e:  # pragma: no cover
        raise ImportError(
            "geonamescache is required for --place lookup. "
            "Install with `pip install geonamescache`."
        ) from e
    return geonamescache.GeonamesCache()


def _row_to_match(row: dict) -> PlaceMatch:
    return PlaceMatch(
        name=row['name'],
        country=row['countrycode'],
        lat=float(row['latitude']),
        lon=float(row['longitude']),
        tz=row['timezone'],
        population=int(row.get('population', 0) or 0),
    )


def _split_query(query: str) -> tuple[str, Optional[str]]:
    parts = [p.strip() for p in query.split(',')]
    if len(parts) >= 2 and len(parts[-1]) == 2 and parts[-1].isalpha():
        return parts[0], parts[-1].upper()
    return parts[0], None


def resolve_place(query: str) -> Optional[PlaceMatch]:
    """Resolve a place query to a PlaceMatch, or None if no match.

    The query may be just a city name ("Taipei") or "City, CC" with a
    two-letter ISO country code. Longer free-text queries (e.g.
    "Taipei, Taiwan") are accepted: only the first segment is used as
    the city name and a 2-letter trailing token is used as country code.
    """
    if not query or not query.strip():
        return None
    name, cc = _split_query(query)
    gc = _cache()
    hits_list = gc.get_cities_by_name(name)
    candidates: list[dict] = []
    for entry in hits_list:
        for row in entry.values():
            candidates.append(row)

    if not candidates:
        # Fall back to scanning alternate names (slower but covers
        # romanisations like "Taipei" vs "Taibei"). Only invoked on miss.
        nlow = name.lower()
        for row in gc.get_cities().values():
            alts = [a.lower() for a in row.get('alternatenames', [])]
            if nlow == row['name'].lower() or nlow in alts:
                candidates.append(row)

    if cc:
        filtered = [r for r in candidates if r['countrycode'] == cc]
        if filtered:
            candidates = filtered

    if not candidates:
        return None

    candidates.sort(key=lambda r: int(r.get('population', 0) or 0), reverse=True)
    return _row_to_match(candidates[0])


def infer_tz_from_coords(lat: float, lon: float) -> Optional[str]:
    """Return IANA timezone name for the given coordinates, or None.

    Requires the ``[geo-tz]`` extra (``timezonefinder``). Raises
    ImportError with a clear message if the extra is not installed.
    """
    try:
        from timezonefinder import TimezoneFinder  # type: ignore
    except ImportError as e:
        raise ImportError(
            "timezonefinder is required for tz inference from coordinates. "
            "Install the extra: `pip install purplestar[geo-tz]`."
        ) from e
    return TimezoneFinder().timezone_at(lat=lat, lng=lon)
