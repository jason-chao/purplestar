"""
JSON schema output for 紫微斗數 natal charts.

Serialises a chart dict produced by generate_chart() into the
Zi Wei Dou Shu Interchange Schema v2 format described in
guides/purplestar_chart_schema.md.
"""
import json
import datetime
from purplestar.data.constants import (
    HEAVENLY_STEMS, EARTHLY_BRANCHES, PALACE_CODES,
    HEAVENLY_STEM_ZH, EARTHLY_BRANCH_ZH, PALACE_ZH,
    STAR_ZH, STAR_EN, BRIGHTNESS_ZH, BRIGHTNESS_EN,
    TRANSFORM_ZH, TRANSFORM_EN,
    FIVE_ELEMENTS_ZH, FIVE_ELEMENTS_EN,
)

# Catalog entries for all codes
_STEMS_CATALOG = {
    stem: {
        'code': stem,
        'labels': {'zh-Hant': HEAVENLY_STEM_ZH[stem], 'en': stem.capitalize()}
    }
    for stem in HEAVENLY_STEMS
}

_BRANCHES_CATALOG = {
    branch: {
        'code': branch,
        'labels': {'zh-Hant': EARTHLY_BRANCH_ZH[branch], 'en': branch.capitalize()}
    }
    for branch in EARTHLY_BRANCHES
}

_PALACES_CATALOG = {
    code: {
        'code': code,
        'labels': {'zh-Hant': PALACE_ZH[code].rstrip('宮'), 'en': code.replace('_', ' ').title()}
    }
    for code in PALACE_CODES
}

_STARS_CATALOG = {
    code: {
        'code': code.replace('_', '_'),
        'labels': {
            'zh-Hant': STAR_ZH.get(code, code),
            'en': STAR_EN.get(code, code.replace('_', ' ').title()),
        }
    }
    for code in STAR_ZH
}

_BRIGHTNESS_CATALOG = {
    k: {'code': k, 'labels': {'zh-Hant': BRIGHTNESS_ZH[k], 'en': BRIGHTNESS_EN[k]}}
    for k in ['miao', 'wang', 'de', 'li', 'ping', 'bu', 'xian']
}

_TRANSFORMS_CATALOG = {
    k: {'code': k, 'labels': {'zh-Hant': TRANSFORM_ZH[k], 'en': TRANSFORM_EN[k]}}
    for k in ['lu', 'quan', 'ke', 'ji']
}


def to_json_schema(chart: dict, indent: int = 2) -> str:
    """Convert chart dict to JSON schema v2 string."""
    doc = _build_schema_doc(chart)
    return json.dumps(doc, ensure_ascii=False, indent=indent)


def _build_schema_doc(chart: dict) -> dict:
    bd = chart['birth_data']
    ch = chart['chart']
    prof = ch['profile']
    overlays = chart.get('overlays', {})

    palaces_out = []
    for p in ch['palaces']:
        stars_out = []
        for s in p['stars']:
            entry = {
                'star': s['code'],
                'category': s['category'],
            }
            if s.get('brightness'):
                entry['brightness'] = s['brightness']
            if s.get('natal_transformation'):
                entry['natal_transformation'] = s['natal_transformation']
                entry['transformation_source'] = 'self'
            stars_out.append(entry)

        markers = p.get('markers', {})
        palace_doc = {
            'position': p['position'],
            'palace': p['palace'],
            'stem': p['stem'],
            'branch': p['branch'],
            'is_body_palace': p['is_body_palace'],
            'stars': stars_out,
        }
        if markers:
            palace_doc['markers'] = markers

        palaces_out.append(palace_doc)

    # Decade limits
    decade_limits_out = []
    for d in (overlays.get('decade_limits') or []):
        if d is None:
            continue
        transforms = []
        year_stem = d.get('stem', '')
        if year_stem and year_stem in chart.get('birth_data', {}).get('year_stem', ''):
            pass  # natal transforms not applicable here
        # For decade limit transformations, use the decade's heavenly stem
        from purplestar.data.constants import MUTAGENS
        transform_keys = ['lu', 'quan', 'ke', 'ji']
        if year_stem in MUTAGENS:
            for i, star in enumerate(MUTAGENS[year_stem]):
                transforms.append({'star': star, 'transformation': transform_keys[i]})
        else:
            # Fallback: empty
            transforms = [{'star': '', 'transformation': k} for k in transform_keys]
        decade_limits_out.append({
            'age_range': d['range'],
            'palace_position': d['position'],
            'stem': d['stem'],
            'transformations': transforms,
        })

    doc = {
        'schema_version': '2.0.0',
        'chart_type': 'ziwei.natal',
        'default_locale': 'zh-Hant',
        'meta': {
            'generated_by': 'purplestar 1.0.0',
            'generated_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        },
        'subject': chart.get('subject', {'id': 'unknown'}),
        'birth_data': {
            'calendar': 'solar',
            'year': bd['solar_year'],
            'month': bd['solar_month'],
            'day': bd['solar_day'],
            'is_leap_month': bd['is_leap_month'],
            'hour_branch': bd['hour_branch'],
            'gender': bd['gender'],
            'timezone': bd['timezone'],
        },
        'system': chart['system'],
        'catalog': {
            'stems': _STEMS_CATALOG,
            'branches': _BRANCHES_CATALOG,
            'palaces': _PALACES_CATALOG,
            'stars': _STARS_CATALOG,
            'brightness': _BRIGHTNESS_CATALOG,
            'transformations': _TRANSFORMS_CATALOG,
        },
        'chart': {
            'profile': {
                'yin_yang': prof['yin_yang'],
                'five_element_bureau': {
                    'element': prof['five_element_bureau']['key'].rstrip('23456'),
                    'number': prof['five_element_bureau']['number'],
                },
                'life_master': prof['life_master'],
                'body_master': prof['body_master'],
                'ming_palace_position': prof['ming_palace_position'],
                'body_palace_position': prof['body_palace_position'],
            },
            'palaces': palaces_out,
        },
    }

    if bd.get('place'):
        doc['birth_data']['place'] = {'name': bd['place']}
    if bd.get('input_clock_time'):
        doc['birth_data']['input_clock_time'] = bd['input_clock_time']

    if decade_limits_out:
        doc['overlays'] = {'decade_limits': decade_limits_out}

    return doc
