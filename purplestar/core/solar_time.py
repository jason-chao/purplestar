"""True solar time correction.

Math adapted from the sister project `purplestar_timing/birth_time.py`
(MIT). Converts a civil clock time at a given longitude into 真太陽時
by applying longitude offset (4 min/° from the timezone meridian) plus
the equation-of-time correction.

The `tz_meridian` is derived from the actual UTC offset at noon on the
birth date — this handles historical zone changes and DST in one step,
so callers must NOT pre-strip DST before invoking `apply_true_solar`.
"""
from __future__ import annotations

import math
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def equation_of_time_minutes(d: date) -> float:
    """NOAA simplified equation of time (minutes), accurate to ~30 s."""
    n = d.timetuple().tm_yday
    B = math.radians(360.0 / 365.0 * (n - 81))
    return 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)


def true_solar_offset_minutes(lon_deg: float, d: date, tz_name: str) -> float:
    """Minutes to ADD to civil clock time to obtain true solar time."""
    sample = datetime(d.year, d.month, d.day, 12, 0, tzinfo=ZoneInfo(tz_name))
    utc_off = sample.utcoffset() or timedelta(0)
    tz_meridian = (utc_off.total_seconds() / 3600.0) * 15.0
    return 4.0 * (lon_deg - tz_meridian) + equation_of_time_minutes(d)


def tz_meridian_deg(d: date, tz_name: str) -> float:
    sample = datetime(d.year, d.month, d.day, 12, 0, tzinfo=ZoneInfo(tz_name))
    utc_off = sample.utcoffset() or timedelta(0)
    return (utc_off.total_seconds() / 3600.0) * 15.0


def apply_true_solar(d: date, t: time, lon_deg: float, tz_name: str
                     ) -> tuple[date, time, float]:
    """Apply TST correction. Returns (corrected_date, corrected_time, offset_minutes)."""
    delta = true_solar_offset_minutes(lon_deg, d, tz_name)
    dt = datetime(d.year, d.month, d.day, t.hour, t.minute) + timedelta(minutes=delta)
    return dt.date(), dt.time().replace(second=0, microsecond=0), delta
