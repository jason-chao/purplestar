"""
Palace (宮位) calculations for 紫微斗數.

Palace indexing: 0=寅, 1=卯, 2=辰, 3=巳, 4=午, 5=未,
                 6=申, 7=酉, 8=戌, 9=亥, 10=子, 11=丑
"""
from purplestar.data.constants import (
    HEAVENLY_STEMS, EARTHLY_BRANCHES, PALACE_CODES,
    TIGER_RULE, FIVE_ELEMENTS_TABLE, FIVE_ELEMENTS_CLASS,
    BRANCH_YINYANG, YANG_BRANCHES,
)


def fix_index(n: int, max_val: int = 12) -> int:
    """Wrap integer to range [0, max_val)."""
    return n % max_val


def branch_to_palace(branch: str) -> int:
    """Convert earthly branch name to palace index (0=寅)."""
    return fix_index(EARTHLY_BRANCHES.index(branch) - 2)


def palace_to_branch(palace_idx: int) -> str:
    """Convert palace index to earthly branch name."""
    return EARTHLY_BRANCHES[fix_index(palace_idx + 2)]


def fix_lunar_month_index(lunar_month: int, is_leap: bool = False,
                           lunar_day: int = 1, time_index: int = 0) -> int:
    """Get palace index for the lunar month (正月=0=寅宮).

    If it is a leap month and fix_leap is in effect (lunar_day > 15 and not 晚子時),
    advance the month by one.
    """
    need_add = is_leap and lunar_day > 15 and time_index != 12
    return fix_index(lunar_month - 1 + (1 if need_add else 0))


def get_five_elements_class(stem_idx: int, branch_idx_full: int) -> str:
    """Determine the five elements bureau (五行局) from stem and branch indices.

    stem_idx: index in HEAVENLY_STEMS (0-9)
    branch_idx_full: index in EARTHLY_BRANCHES (0-11, 子=0)

    Returns a key from FIVE_ELEMENTS_TABLE: 'water2','wood3','metal4','earth5','fire6'
    """
    stem_num = stem_idx // 2 + 1  # 甲乙=1, 丙丁=2, 戊己=3, 庚辛=4, 壬癸=5
    branch_mod = fix_index(branch_idx_full, 6)  # wrap to 0-5, so 午=0,未=1,申=2,酉=3,戌=4,亥=5...
    # Actually: 子=0,丑=1,寅=2,卯=3,辰=4,巳=5 then 午=0,未=1,申=2,酉=3,戌=4,亥=5
    branch_num = branch_mod // 2 + 1  # 子午丑未=1, 寅申卯酉=2, 辰戌巳亥=3
    total = stem_num + branch_num
    while total > 5:
        total -= 5
    return FIVE_ELEMENTS_TABLE[total - 1]


def get_soul_and_body(year_stem_idx: int, lunar_month: int, lunar_day: int,
                       time_index: int, is_leap: bool = False) -> dict:
    """Calculate soul palace (命宮) and body palace (身宮) indices.

    Returns dict with:
    - soul_index: palace index of 命宮 (0-11, 0=寅)
    - body_index: palace index of 身宮
    - soul_stem_idx: heavenly stem index of 命宮
    - soul_branch: earthly branch name of 命宮
    - five_elements: five elements class key
    """
    # Month index: 正月 = palace 0 (寅)
    month_palace = fix_lunar_month_index(lunar_month, is_leap, lunar_day, time_index)

    # Hour's earthly branch index in the full 12-branch array
    hour_branch_full_idx = time_index % 12  # 子=0, 丑=1, ..., 亥=11

    # Soul palace: from 寅, forward to birth month, then backward to birth hour
    soul_index = fix_index(month_palace - hour_branch_full_idx)

    # Body palace: from 寅, forward to birth month, then forward to birth hour
    body_index = fix_index(month_palace + hour_branch_full_idx)

    # Soul palace heavenly stem (via 五虎遁)
    yin_stem = TIGER_RULE[HEAVENLY_STEMS[year_stem_idx]]  # stem at 寅 palace
    yin_stem_idx = HEAVENLY_STEMS.index(yin_stem)
    soul_stem_idx = fix_index(yin_stem_idx + soul_index, 10)

    # Soul palace earthly branch
    soul_branch = palace_to_branch(soul_index)
    soul_branch_full_idx = EARTHLY_BRANCHES.index(soul_branch)

    # Five elements class
    five_elements = get_five_elements_class(soul_stem_idx, soul_branch_full_idx)

    return {
        'soul_index': soul_index,
        'body_index': body_index,
        'soul_stem_idx': soul_stem_idx,
        'soul_branch': soul_branch,
        'five_elements': five_elements,
    }


def get_palace_names(soul_index: int) -> list[str]:
    """Return list of 12 palace codes indexed by palace position (0=寅).

    palace_names[i] = palace code for physical position i.
    """
    return [PALACE_CODES[fix_index(i - soul_index)] for i in range(12)]


def get_palace_stems(year_stem_idx: int) -> list[int]:
    """Return list of heavenly stem indices for each palace position (0=寅)."""
    yin_stem = TIGER_RULE[HEAVENLY_STEMS[year_stem_idx]]
    yin_stem_idx = HEAVENLY_STEMS.index(yin_stem)
    return [fix_index(yin_stem_idx + i, 10) for i in range(12)]


def get_horoscope(year_stem_idx: int, year_branch: str, soul_index: int,
                   five_elements_key: str, gender: str) -> list[dict]:
    """Calculate decadal luck (大限) for all 12 palaces.

    Returns list of 12 dicts indexed by palace position, each with:
    - range: [start_age, end_age]
    - stem: heavenly stem of the decade
    - branch: earthly branch of the decade
    - position: palace position (1-12, 1=寅)
    """
    five_elements_value = FIVE_ELEMENTS_CLASS[five_elements_key]
    year_branch_yang = year_branch not in ('chou','mao','si','wei','you','hai')  # yang branches
    gender_yang = (gender == 'male')
    forward = (gender_yang == year_branch_yang)  # 陽男陰女順，陰男陽女逆

    palace_stems = get_palace_stems(year_stem_idx)
    decadals = [None] * 12

    for i in range(12):
        if forward:
            idx = fix_index(soul_index + i)
        else:
            idx = fix_index(soul_index - i)
        start_age = five_elements_value + 10 * i
        stem = HEAVENLY_STEMS[palace_stems[idx]]
        branch = palace_to_branch(idx)
        decadals[idx] = {
            'range': [start_age, start_age + 9],
            'stem': stem,
            'branch': branch,
            'position': idx + 1,
        }

    return decadals
