"""
Main chart generation for 紫微斗數.
"""
from __future__ import annotations
import datetime
from datetime import time as _dt_time
from typing import Optional

from purplestar.data.constants import (
    HEAVENLY_STEMS, EARTHLY_BRANCHES, PALACE_CODES,
    HEAVENLY_STEM_ZH, EARTHLY_BRANCH_ZH, PALACE_ZH,
    FIVE_ELEMENTS_ZH, FIVE_ELEMENTS_CLASS,
    SOUL_MASTER, SOUL_MASTER_ZH, BODY_MASTER, BODY_MASTER_ZH,
    HOUR_BRANCH, HOUR_ZH, MUTAGENS, TRANSFORM_ZH,
)
from purplestar.core.lunar import solar_to_lunar, get_year_gz, time_to_index, parse_time
from purplestar.core.solar_time import apply_true_solar, tz_meridian_deg
from purplestar.core.palace import (
    get_soul_and_body, get_palace_names, get_palace_stems,
    get_horoscope, fix_index, branch_to_palace, palace_to_branch,
    get_five_elements_class,
)
from purplestar.core.stars import (
    get_start_index, get_major_stars, get_minor_stars,
    get_changsheng12, get_boshi12, get_jiangqian12, get_suiqian12,
    get_adjective_stars, _get_lu_yang_tuo_ma,
)


def generate_chart(
    gender: str,
    solar_date: str,
    time: Optional[str] = None,
    timezone: Optional[str] = None,
    place: Optional[str] = None,
    name: Optional[str] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
) -> dict:
    """Generate a complete 紫微斗數 natal chart.

    Args:
        gender: 'male' or 'female'
        solar_date: Solar date string 'YYYY-MM-DD'
        time: Time string 'HH:MM' or None for unknown
        timezone: Timezone string e.g. 'Asia/Taipei'
        place: Place name string. If `longitude` is not given, attempts to
            resolve via geonamescache to fill in lon/lat/tz for true-solar
            correction.
        name: Person identifier
        longitude: Optional birth longitude (decimal degrees, east positive).
            When supplied together with `time` and a real IANA `timezone`,
            the clock time is converted to 真太陽時 before casting.
        latitude: Optional birth latitude (decimal degrees). Recorded as
            metadata only.

    Returns:
        Chart dict suitable for JSON serialization or plaintext output.
    """
    # Parse inputs
    parts = solar_date.split('-')
    sy, sm, sd = int(parts[0]), int(parts[1]), int(parts[2])

    # Place resolution + true-solar correction. Defaults to today's
    # behaviour: no resolution, no correction.
    place_resolution = {'source': 'none'}
    solar_time_correction = {'applied': False}
    original_time = time

    resolved_lon = longitude
    resolved_lat = latitude
    resolved_tz = timezone

    if longitude is None and place:
        try:
            from purplestar.core.geo import resolve_place
            match = resolve_place(place)
        except ImportError:
            match = None
        if match is not None:
            resolved_lon = match.lon
            resolved_lat = match.lat
            if not resolved_tz or resolved_tz == 'UTC':
                resolved_tz = match.tz
            place_resolution = {
                'source': 'geonames',
                'matched_name': match.name,
                'country': match.country,
                'population': match.population,
                'latitude': match.lat,
                'longitude': match.lon,
                'timezone': match.tz,
            }
    elif longitude is not None:
        place_resolution = {
            'source': 'explicit',
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone,
        }

    if (resolved_lon is not None and time and resolved_tz
            and resolved_tz != 'UTC'):
        try:
            t_parts = time.strip().split(':')
            t_obj = _dt_time(int(t_parts[0]),
                             int(t_parts[1]) if len(t_parts) > 1 else 0)
            from datetime import date as _date
            corrected_date, corrected_time, offset_min = apply_true_solar(
                _date(sy, sm, sd), t_obj, resolved_lon, resolved_tz)
            sy, sm, sd = corrected_date.year, corrected_date.month, corrected_date.day
            time = corrected_time.strftime('%H:%M')
            solar_time_correction = {
                'applied': True,
                'offset_minutes': round(offset_min, 2),
                'original_time': original_time,
                'corrected_time': time,
                'longitude': resolved_lon,
                'tz_meridian_deg': round(tz_meridian_deg(corrected_date, resolved_tz), 4),
            }
        except (ValueError, KeyError):
            pass

    time_index = parse_time(time)
    time_known = time is not None and time.lower() not in ('unknown', '未知', '')

    # Convert to lunar date
    lunar_year, lm, ld, is_leap = solar_to_lunar(sy, sm, sd)
    # If late rat hour (time_index==12), lunar day may advance - handle simply
    # For late rat hour, the effective lunar day for most calculations is the next day
    # We keep ld as-is but pass time_index=12 to functions that need it

    # Year's heavenly stem and earthly branch
    year_stem_idx, year_branch_idx = get_year_gz(sy, sm, sd)
    year_stem = HEAVENLY_STEMS[year_stem_idx]
    year_branch = EARTHLY_BRANCHES[year_branch_idx]

    # Soul and body palace
    sb = get_soul_and_body(year_stem_idx, lm, ld, time_index, is_leap)
    soul_index = sb['soul_index']
    body_index = sb['body_index']
    soul_stem_idx = sb['soul_stem_idx']
    soul_branch = sb['soul_branch']
    five_elements = sb['five_elements']
    five_elements_value = FIVE_ELEMENTS_CLASS[five_elements]

    # Palace names and stems
    palace_names = get_palace_names(soul_index)  # indexed by palace position
    palace_stem_indices = get_palace_stems(year_stem_idx)

    # Zi Wei and Tian Fu indices
    ziwei_idx, tianfu_idx = get_start_index(ld, five_elements_value, time_index)

    # Determine yin-yang polarity (命盤陰陽)
    # Yang male or yin female = forward (陽男陰女)
    year_branch_yang = year_branch not in ('chou','mao','si','wei','you','hai')
    gender_yang = (gender == 'male')
    chart_yinyang = 'yang' if (gender_yang == year_branch_yang) else 'yin'
    # Actually yin-yang of the chart is based on year branch and gender separately
    # The chart profile yin_yang = yin if female, yang if male (simplified)
    profile_yinyang = 'yang' if gender_yang else 'yin'

    # Life and body masters
    life_master = SOUL_MASTER[soul_branch]
    life_master_zh = SOUL_MASTER_ZH[soul_branch]
    body_master = BODY_MASTER[year_branch]
    body_master_zh = BODY_MASTER_ZH[year_branch]

    # Stars
    major = get_major_stars(ziwei_idx, tianfu_idx, year_stem)
    minor = get_minor_stars(year_stem, year_branch, lm, time_index)
    adjective = get_adjective_stars(year_stem, year_branch, lm, ld, time_index,
                                     soul_index, body_index, gender)

    # Markers
    cs12 = get_changsheng12(five_elements, gender, year_branch, soul_index)
    lu_idx, _, _, _ = _get_lu_yang_tuo_ma(year_stem, year_branch)
    bs12 = get_boshi12(year_stem, year_branch, gender, lu_idx)
    jq12 = get_jiangqian12(year_branch)
    sq12 = get_suiqian12(year_branch)

    # Decadal luck
    decadals = get_horoscope(year_stem_idx, year_branch, soul_index, five_elements, gender)

    # Build natal transformations (四化) from year stem
    natal_transforms = []
    transform_keys = ['lu', 'quan', 'ke', 'ji']
    if year_stem in MUTAGENS:
        for i, star_code in enumerate(MUTAGENS[year_stem]):
            natal_transforms.append({'star': star_code, 'transformation': transform_keys[i]})

    # Build palace data
    palaces = []
    for i in range(12):
        all_stars = major[i] + minor[i] + adjective[i]
        markers = {}
        if cs12[i]:
            markers['changsheng12'] = cs12[i]
        if bs12[i]:
            markers['boshi12'] = bs12[i]
        if jq12[i]:
            markers['jiangqian12'] = jq12[i]
        if sq12[i]:
            markers['suiqian12'] = sq12[i]

        palace = {
            'position': i + 1,
            'palace': palace_names[i],
            'stem': HEAVENLY_STEMS[palace_stem_indices[i]],
            'branch': palace_to_branch(i),
            'is_body_palace': (i == body_index),
            'stars': all_stars,
            'markers': markers,
        }
        palaces.append(palace)

    # Lunar year stem/branch for display
    lunar_year_stem = HEAVENLY_STEM_ZH[year_stem]
    lunar_year_branch = EARTHLY_BRANCH_ZH[year_branch]

    chart = {
        'schema_version': '2.0.0',
        'chart_type': 'ziwei.natal',
        'subject': {'id': name or 'unknown'},
        'birth_data': {
            'calendar': 'solar',
            'solar_year': sy, 'solar_month': sm, 'solar_day': sd,
            'solar_date': f'{sy:04d}-{sm:02d}-{sd:02d}',
            'input_solar_date': solar_date,
            'lunar_year': lunar_year, 'lunar_month': lm, 'lunar_day': ld,
            'is_leap_month': is_leap,
            'time_index': time_index,
            'time_known': time_known,
            'hour_branch': HOUR_BRANCH[time_index],
            'hour_zh': HOUR_ZH[time_index],
            'gender': gender,
            'timezone': resolved_tz or 'UTC',
            'place': place,
            'longitude': resolved_lon,
            'latitude': resolved_lat,
            'place_resolution': place_resolution,
            'solar_time_correction': solar_time_correction,
            'year_stem': year_stem,
            'year_branch': year_branch,
            'year_gz_zh': lunar_year_stem + lunar_year_branch + '年',
        },
        'system': {
            'family': 'ziwei_doushu',
            'school': '三合派',
            'engine': {'name': 'purplestar', 'version': '1.0.0'},
        },
        'chart': {
            'profile': {
                'yin_yang': profile_yinyang,
                'five_element_bureau': {
                    'key': five_elements,
                    'number': five_elements_value,
                    'zh': FIVE_ELEMENTS_ZH[five_elements],
                },
                'life_master': life_master,
                'life_master_zh': life_master_zh,
                'body_master': body_master,
                'body_master_zh': body_master_zh,
                'ming_palace_position': soul_index + 1,
                'body_palace_position': body_index + 1,
                'soul_stem': HEAVENLY_STEMS[soul_stem_idx],
                'soul_branch': soul_branch,
                'soul_stem_zh': HEAVENLY_STEM_ZH[HEAVENLY_STEMS[soul_stem_idx]],
                'soul_branch_zh': EARTHLY_BRANCH_ZH[soul_branch],
            },
            'palaces': palaces,
        },
        'overlays': {
            'decade_limits': decadals,
            'natal_transformations': natal_transforms,
        },
    }

    return chart
