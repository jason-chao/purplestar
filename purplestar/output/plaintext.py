"""
Plaintext output for 紫微斗數 natal charts.

Produces the structured plain-text format described in
guides/purplestar_chart_plaintext_format.md, suitable for
WhatsApp sharing and LLM input.
"""
from importlib.metadata import version as pkg_version
from purplestar.data.constants import (
    PALACE_ZH, EARTHLY_BRANCH_ZH, HEAVENLY_STEM_ZH,
    STAR_ZH, BRIGHTNESS_ZH, TRANSFORM_ZH,
    FIVE_ELEMENTS_ZH, HOUR_ZH,
)

_MAJOR_CATEGORIES = {'major'}
_MINOR_CATEGORIES = {'minor'}
_MALEFIC_CODES = {'qing_yang', 'tuo_luo', 'huo_xing', 'ling_xing', 'di_kong', 'di_jie'}
_TRANSFORM_STARS = {'lu_cun', 'tian_ma', 'zuo_fu', 'you_bi', 'wen_chang', 'wen_qu',
                     'tian_kui', 'tian_yue'}


def to_plaintext(chart: dict) -> str:
    """Convert a chart dict to structured plain-text format."""
    lines = []
    lines.append('=' * 36)
    lines.append('紫微斗數命盤')
    lines.append('=' * 36)
    lines.append('')

    # Section 1: 命盤資料
    lines.append('【命盤資料】')
    bd = chart['birth_data']
    prof = chart['chart']['profile']

    subject_id = chart.get('subject', {}).get('id', '')
    if subject_id and subject_id != 'unknown':
        lines.append(f'代號：{subject_id}')

    gender_zh = '男' if bd['gender'] == 'male' else '女'
    lines.append(f'性別：{gender_zh}')
    lines.append(f'陽曆：{bd["solar_date"]}')

    lunar_year = bd.get("lunar_year", "")
    lunar_gz = bd.get("year_gz_zh", "")
    lunar_month = bd.get("lunar_month", "")
    lunar_day = bd.get("lunar_day", "")
    leap_str = '閏' if bd.get('is_leap_month') else ''
    lines.append(f'陰曆：{lunar_gz} {leap_str}{_month_zh(lunar_month)}{_day_zh(lunar_day)}')
    lines.append(f'陰曆閏月：{"是" if bd.get("is_leap_month") else "否"}')

    if bd.get('time_known', True):
        lines.append(f'時辰：{bd.get("hour_zh", "")}')
    else:
        lines.append('時辰：不詳')

    soul_branch_zh = EARTHLY_BRANCH_ZH.get(prof['soul_branch'], prof['soul_branch'])
    lines.append(f'命宮地支：{soul_branch_zh}')

    # Body palace name
    body_pos = prof['body_palace_position'] - 1  # 0-indexed
    body_palace_code = chart['chart']['palaces'][body_pos]['palace']
    body_palace_zh = PALACE_ZH.get(body_palace_code, body_palace_code)
    lines.append(f'身宮所在：{body_palace_zh}')

    lines.append(f'五行局：{prof["five_element_bureau"]["zh"]}')
    lines.append(f'命主：{prof["life_master_zh"]}')
    lines.append(f'身主：{prof["body_master_zh"]}')
    if chart['system'].get('school'):
        lines.append(f'派別：{chart["system"]["school"]}')

    lines.append('')
    lines.append('-' * 36)
    lines.append('【十二宮】')
    lines.append('-' * 36)
    lines.append('')

    # Section 2: 十二宮
    # Conventional 紫微斗數 interpretation order:
    # 命宮 → 父母宮 → 福德宮 → 田宅宮 → 事業宮 → 交友宮 → 遷移宮 → 疾厄宮 → 財帛宮 → 子女宮 → 夫妻宮 → 兄弟宮
    palace_order = ['life','parents','spirit','property','career','friends',
                    'travel','health','wealth','children','spouse','siblings']

    # Build palace lookup by code
    palace_by_code = {p['palace']: p for p in chart['chart']['palaces']}

    for code in palace_order:
        p = palace_by_code.get(code)
        if p is None:
            continue
        branch_zh = EARTHLY_BRANCH_ZH[p['branch']]
        palace_zh = PALACE_ZH[code]
        body_mark = ' ★身宮' if p['is_body_palace'] else ''
        lines.append(f'【{palace_zh}】{branch_zh}{body_mark}')

        # Stars by category
        major = [s for s in p['stars'] if s['category'] == 'major']
        minor_stars = [s for s in p['stars']
                       if s['category'] in ('minor', 'auxiliary')
                       and s['code'] not in _MALEFIC_CODES]
        malefic = [s for s in p['stars'] if s['code'] in _MALEFIC_CODES]

        # 主星
        if major:
            parts = []
            for s in major:
                name = STAR_ZH.get(s['code'], s['code'])
                bright = BRIGHTNESS_ZH.get(s.get('brightness', ''), '')
                parts.append(f'{name}({bright})' if bright else name)
            lines.append('主星：' + '、'.join(parts))
        else:
            lines.append('主星：（無）')

        # 輔星 (minor/auxiliary, non-malefic)
        if minor_stars:
            parts = [STAR_ZH.get(s['code'], s['code']) for s in minor_stars]
            lines.append('輔星：' + '、'.join(parts))
        else:
            lines.append('輔星：（無）')

        # 四化 - collect from all stars in this palace
        transforms = []
        for s in p['stars']:
            if s.get('natal_transformation'):
                name = STAR_ZH.get(s['code'], s['code'])
                tr = TRANSFORM_ZH.get(s['natal_transformation'], s['natal_transformation'])
                transforms.append(f'{name}-{tr}')
        if transforms:
            lines.append('四化：' + '、'.join(transforms))
        else:
            lines.append('四化：（無）')

        # 煞星
        if malefic:
            parts = [STAR_ZH.get(s['code'], s['code']) for s in malefic]
            lines.append('煞星：' + '、'.join(parts))
        else:
            lines.append('煞星：（無）')

        # 大限
        decadals = chart.get('overlays', {}).get('decade_limits') or []
        palace_decadal = None
        for d in decadals:
            if d and d.get('position') == p['position']:
                palace_decadal = d
                break
        if palace_decadal:
            r = palace_decadal['range']
            lines.append(f'大限：{r[0]}–{r[1]}')
        else:
            lines.append('大限：（無）')

        lines.append('')

    # Section 3: 備註
    lines.append('-' * 36)
    lines.append('【備註】')
    lines.append('-' * 36)
    notes = []
    notes.append(f'- 本命盤由 purplestar {pkg_version("purplestar")} 自動生成，三合派排盤。')
    if not bd.get('time_known', True):
        notes.append('- 出生時間不詳，預設以子時（00:00–01:00）排盤，結果僅供參考。')
    lines.extend(notes)
    lines.append('=' * 36)

    return '\n'.join(lines)


def _month_zh(month: int) -> str:
    """Convert lunar month number to Chinese string."""
    months = ['正月','二月','三月','四月','五月','六月',
              '七月','八月','九月','十月','十一月','十二月']
    if 1 <= month <= 12:
        return months[month - 1]
    return f'{month}月'


def _day_zh(day: int) -> str:
    """Convert lunar day number to Chinese string."""
    days = ['初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
            '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
            '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十']
    if 1 <= day <= 30:
        return days[day - 1]
    return f'{day}日'
