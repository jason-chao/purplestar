"""
Star placement functions for 紫微斗數.

All functions return lists of length 12 indexed by palace position (0=寅).
Each entry is a list of star dicts: {code, category, brightness, natal_transformation}
"""
from purplestar.data.constants import (
    HEAVENLY_STEMS, EARTHLY_BRANCHES, PALACE_CODES,
    TIGER_RULE, MUTAGENS, FIVE_ELEMENTS_CLASS, BRANCH_YINYANG,
)
from purplestar.data.stars_data import STAR_BRIGHTNESS
from purplestar.core.palace import fix_index, branch_to_palace, palace_to_branch


def init_stars() -> list[list]:
    """Return empty 12-palace star array."""
    return [[] for _ in range(12)]


def get_brightness(star_code: str, palace_idx: int) -> str:
    """Get brightness of a star at a given palace index."""
    if star_code in STAR_BRIGHTNESS:
        return STAR_BRIGHTNESS[star_code][fix_index(palace_idx)]
    return ''


def get_natal_transformation(star_code: str, year_stem: str) -> str | None:
    """Get the natal transformation (四化) for a star given year stem."""
    if year_stem in MUTAGENS:
        mutagens = MUTAGENS[year_stem]  # [lu, quan, ke, ji]
        transform_keys = ['lu', 'quan', 'ke', 'ji']
        for i, s in enumerate(mutagens):
            if s == star_code:
                return transform_keys[i]
    return None


def get_start_index(lunar_day: int, five_elements_value: int, time_index: int = 0,
                     day_divide: str = 'forward') -> tuple[int, int]:
    """Calculate 紫微星 and 天府星 palace indices.

    Algorithm: 起紫微星訣
    六五四三二，酉午亥辰丑，
    局數除日數，商數宮前走；
    若見數無餘，便要起虎口，
    日數小於局，還直宮中守。
    """
    day = lunar_day
    if time_index == 12 and day_divide != 'current':
        day += 1
    # We don't adjust for month overflow here (handled by caller if needed)

    offset = 0
    remainder = -1
    quotient = 0

    while remainder != 0:
        divisor = day + offset
        quotient = divisor // five_elements_value
        remainder = divisor % five_elements_value
        if remainder != 0:
            offset += 1

    quotient %= 12
    ziwei_index = quotient - 1

    if offset % 2 == 0:
        ziwei_index += offset
    else:
        ziwei_index -= offset

    ziwei_index = fix_index(ziwei_index)
    tianfu_index = fix_index(12 - ziwei_index)

    return ziwei_index, tianfu_index


def get_major_stars(ziwei_index: int, tianfu_index: int, year_stem: str) -> list[list]:
    """Place the 14 major stars (主星)."""
    stars = init_stars()

    # Zi Wei group: placed counterclockwise from Zi Wei
    ziwei_group = ['zi_wei','tian_ji','','tai_yang','wu_qu','tian_tong','','','lian_zhen']
    for i, code in enumerate(ziwei_group):
        if code:
            idx = fix_index(ziwei_index - i)
            stars[idx].append({
                'code': code,
                'category': 'major',
                'brightness': get_brightness(code, idx),
                'natal_transformation': get_natal_transformation(code, year_stem),
            })

    # Tian Fu group: placed clockwise from Tian Fu
    tianfu_group = ['tian_fu','tai_yin','tan_lang','ju_men','tian_xiang','tian_liang','qi_sha','','','','po_jun']
    for i, code in enumerate(tianfu_group):
        if code:
            idx = fix_index(tianfu_index + i)
            stars[idx].append({
                'code': code,
                'category': 'major',
                'brightness': get_brightness(code, idx),
                'natal_transformation': get_natal_transformation(code, year_stem),
            })

    return stars


def get_minor_stars(year_stem: str, year_branch: str, lunar_month: int,
                     time_index: int) -> list[list]:
    """Place the 14 minor/auxiliary stars (輔星)."""
    stars = init_stars()

    # 左輔右弼 (by lunar month)
    # 辰上順正月寅起左輔, 戌上逆正月寅起右弼
    chen_palace = branch_to_palace('chen')  # 辰 palace index
    xu_palace = branch_to_palace('xu')      # 戌 palace index
    zuo_idx = fix_index(chen_palace + (lunar_month - 1))
    you_idx = fix_index(xu_palace - (lunar_month - 1))

    # 文昌文曲 (by time index)
    # 戌上逆時覓文昌, 辰上順時文曲位
    chang_idx = fix_index(xu_palace - fix_index(time_index))
    qu_idx = fix_index(chen_palace + fix_index(time_index))

    # 天魁天鉞 (by year stem)
    kui_idx, yue_idx = _get_kui_yue(year_stem)

    # 祿存擎羊陀羅天馬 (by year stem and branch)
    lu_idx, yang_idx, tuo_idx, ma_idx = _get_lu_yang_tuo_ma(year_stem, year_branch)

    # 地空地劫 (by time index)
    hai_palace = branch_to_palace('hai')  # 亥 palace index
    kong_idx = fix_index(hai_palace - fix_index(time_index))
    jie_idx = fix_index(hai_palace + fix_index(time_index))

    # 火星鈴星 (by year branch and time index)
    huo_idx, ling_idx = _get_huo_ling(year_branch, time_index)

    def add(idx, code, cat='minor'):
        stars[idx].append({
            'code': code,
            'category': cat,
            'brightness': get_brightness(code, idx),
            'natal_transformation': get_natal_transformation(code, year_stem),
        })

    add(zuo_idx, 'zuo_fu')
    add(you_idx, 'you_bi')
    add(chang_idx, 'wen_chang')
    add(qu_idx, 'wen_qu')
    add(kui_idx, 'tian_kui')
    add(yue_idx, 'tian_yue')
    add(lu_idx, 'lu_cun')
    add(ma_idx, 'tian_ma')
    add(kong_idx, 'di_kong')
    add(jie_idx, 'di_jie')
    add(huo_idx, 'huo_xing')
    add(ling_idx, 'ling_xing')
    add(yang_idx, 'qing_yang')
    add(tuo_idx, 'tuo_luo')

    return stars


def _get_ku_yue_alias(year_stem):
    # alias for external call
    return _get_kui_yue(year_stem)


def _get_kui_yue(year_stem: str) -> tuple[int, int]:
    """天魁天鉞 indices by year stem."""
    mapping = {
        'jia': ('chou', 'wei'), 'wu': ('chou', 'wei'), 'geng': ('chou', 'wei'),
        'yi': ('zi', 'shen'), 'ji': ('zi', 'shen'),
        'xin': ('wu', 'yin'),
        'bing': ('hai', 'you'), 'ding': ('hai', 'you'),
        'ren': ('mao', 'si'), 'gui': ('mao', 'si'),
    }
    kui_branch, yue_branch = mapping[year_stem]
    return branch_to_palace(kui_branch), branch_to_palace(yue_branch)


def _get_lu_yang_tuo_ma(year_stem: str, year_branch: str) -> tuple[int, int, int, int]:
    """祿存擎羊陀羅天馬 indices."""
    lu_mapping = {
        'jia': 'yin', 'yi': 'mao', 'bing': 'si', 'ding': 'wu',
        'wu': 'si', 'ji': 'wu', 'geng': 'shen', 'xin': 'you',
        'ren': 'hai', 'gui': 'zi',
    }
    ma_mapping = {
        frozenset({'yin','wu','xu'}): 'shen',
        frozenset({'shen','zi','chen'}): 'yin',
        frozenset({'si','you','chou'}): 'hai',
        frozenset({'hai','mao','wei'}): 'si',
    }
    lu_branch = lu_mapping[year_stem]
    lu_idx = branch_to_palace(lu_branch)
    yang_idx = fix_index(lu_idx + 1)
    tuo_idx = fix_index(lu_idx - 1)

    ma_branch = 'shen'
    for group, branch in ma_mapping.items():
        if year_branch in group:
            ma_branch = branch
            break
    ma_idx = branch_to_palace(ma_branch)

    return lu_idx, yang_idx, tuo_idx, ma_idx


def _get_huo_ling(year_branch: str, time_index: int) -> tuple[int, int]:
    """火星鈴星 indices by year branch and time index."""
    t = fix_index(time_index)
    if year_branch in ('yin','wu','xu'):
        huo = branch_to_palace('chou') + t
        ling = branch_to_palace('mao') + t
    elif year_branch in ('shen','zi','chen'):
        huo = branch_to_palace('yin') + t
        ling = branch_to_palace('xu') + t
    elif year_branch in ('si','you','chou'):
        huo = branch_to_palace('mao') + t
        ling = branch_to_palace('xu') + t
    else:  # hai, mao, wei
        huo = branch_to_palace('you') + t
        ling = branch_to_palace('xu') + t
    return fix_index(huo), fix_index(ling)


def get_changsheng12(five_elements_key: str, gender: str,
                      year_branch: str, soul_index: int) -> list[str | None]:
    """Calculate 長生12神 markers. Returns list of 12 indexed by palace (0=寅)."""
    fe_value = FIVE_ELEMENTS_CLASS[five_elements_key]
    start_mapping = {2: 'shen', 3: 'hai', 4: 'si', 5: 'shen', 6: 'yin'}
    start_idx = branch_to_palace(start_mapping[fe_value])

    year_yang = year_branch not in ('chou','mao','si','wei','you','hai')
    gender_yang = (gender == 'male')
    forward = (gender_yang == year_yang)

    seq = ['chang_sheng','mu_yu','guan_dai','lin_guan','di_wang',
           'shuai','bing','si','mu','jue','tai','yang']

    result = [None] * 12
    for i, name in enumerate(seq):
        if forward:
            idx = fix_index(start_idx + i)
        else:
            idx = fix_index(start_idx - i)
        result[idx] = name
    return result


def get_boshi12(year_stem: str, year_branch: str, gender: str, lu_idx: int) -> list[str | None]:
    """Calculate 博士12神 markers."""
    year_yang = year_branch not in ('chou','mao','si','wei','you','hai')
    gender_yang = (gender == 'male')
    forward = (gender_yang == year_yang)

    seq = ['bo_shi','li_shi','qing_long','xiao_hao','jiang_jun','zou_shu',
           'fei_lian_b','xi_shen','bing_fu','da_hao','fu_bing','guan_fu']

    result = [None] * 12
    for i, name in enumerate(seq):
        idx = fix_index(lu_idx + i if forward else lu_idx - i)
        result[idx] = name
    return result


def get_jiangqian12(year_branch: str) -> list[str | None]:
    """Calculate 將前12神 markers."""
    mapping = {
        frozenset({'yin','wu','xu'}): 'wu',
        frozenset({'shen','zi','chen'}): 'zi',
        frozenset({'si','you','chou'}): 'you',
        frozenset({'hai','mao','wei'}): 'mao',
    }
    start = 'wu'
    for group, branch in mapping.items():
        if year_branch in group:
            start = branch
            break
    start_idx = branch_to_palace(start)

    seq = ['jiang_xing','pan_an','sui_yi','xi_shen2','hua_gai2','jie_sha',
           'zhai_sha','tian_sha','zhi_bei','xian_chi2','yue_sha','wang_shen']

    result = [None] * 12
    for i, name in enumerate(seq):
        result[fix_index(start_idx + i)] = name
    return result


def get_suiqian12(year_branch: str) -> list[str | None]:
    """Calculate 歲前12神 markers."""
    start_idx = branch_to_palace(year_branch)

    seq = ['sui_jian','hui_qi','sang_men','guan_suo','guan_fu2','xiao_hao2',
           'da_hao2','long_de','bai_hu','tian_de2','diao_ke','bing_fu2']

    result = [None] * 12
    for i, name in enumerate(seq):
        result[fix_index(start_idx + i)] = name
    return result


def get_adjective_stars(year_stem: str, year_branch: str,
                          lunar_month: int, lunar_day: int,
                          time_index: int, soul_index: int,
                          body_index: int, gender: str) -> list[list]:
    """Place adjective/miscellaneous stars."""
    stars = init_stars()

    def add(idx, code):
        stars[fix_index(idx)].append({'code': code, 'category': 'misc',
                                       'brightness': '', 'natal_transformation': None})

    # 紅鸞天喜 (by year branch)
    # 卯上起子逆數至生年支 = 紅鸞
    year_branch_full = EARTHLY_BRANCHES.index(year_branch)
    hong_luan_idx = fix_index(branch_to_palace('mao') - year_branch_full)
    tian_xi_idx = fix_index(hong_luan_idx + 6)
    add(hong_luan_idx, 'hong_luan')
    add(tian_xi_idx, 'tian_xi')

    # 天姚 (by lunar month): 丑宮起正月順
    tian_yao_idx = fix_index(branch_to_palace('chou') + (lunar_month - 1))
    add(tian_yao_idx, 'tian_yao')

    # 咸池 (by year branch)
    _, xian_chi_idx = _get_huagai_xianchi(year_branch)
    add(xian_chi_idx, 'xian_chi')

    # 月解/解神 (by lunar month)
    jie_shen_branches = ['shen','xu','zi','yin','chen','wu']
    jie_shen_idx = branch_to_palace(jie_shen_branches[(lunar_month - 1) // 2])
    add(jie_shen_idx, 'jie_shen')

    # 三台八座 (by lunar month and lunar day)
    chen_palace = branch_to_palace('chen')
    xu_palace = branch_to_palace('xu')
    # Re-calculate zuo/you indices for month
    zuo_for_day = fix_index(chen_palace + (lunar_month - 1))
    you_for_day = fix_index(xu_palace - (lunar_month - 1))
    # 文昌文曲 for day calculation
    chang_for_day = fix_index(xu_palace - fix_index(time_index))
    qu_for_day = fix_index(chen_palace + fix_index(time_index))
    day_idx = lunar_day - 1 if time_index < 12 else lunar_day  # fixLunarDayIndex
    san_tai_idx = fix_index((zuo_for_day + day_idx) % 12)
    ba_zuo_idx = fix_index((you_for_day - day_idx) % 12)
    en_guang_idx = fix_index(((chang_for_day + day_idx) % 12) - 1)
    tian_gui_idx = fix_index(((qu_for_day + day_idx) % 12) - 1)
    add(san_tai_idx, 'san_tai')
    add(ba_zuo_idx, 'ba_zuo')
    add(en_guang_idx, 'en_guang')
    add(tian_gui_idx, 'tian_gui')

    # 龍池鳳閣 (by year branch)
    long_chi_idx = fix_index(branch_to_palace('chen') + year_branch_full)
    feng_ge_idx = fix_index(branch_to_palace('xu') - year_branch_full)
    add(long_chi_idx, 'long_chi')
    add(feng_ge_idx, 'feng_ge')

    # 天才天壽 (by soul/body index + year branch)
    tian_cai_idx = fix_index(soul_index + year_branch_full)
    tian_shou_idx = fix_index(body_index + year_branch_full)
    add(tian_cai_idx, 'tian_cai')
    add(tian_shou_idx, 'tian_shou')

    # 台輔封誥 (by time index)
    tai_fu_idx = fix_index(branch_to_palace('wu') + fix_index(time_index))
    feng_gao_idx = fix_index(branch_to_palace('yin') + fix_index(time_index))
    add(tai_fu_idx, 'tai_fu')
    add(feng_gao_idx, 'feng_gao')

    # 天巫 (by lunar month): 正五九月在巳, 二六十月在申, 三七十一在寅, 四八十二在亥
    tian_wu_branches = ['si','shen','yin','hai']
    tian_wu_idx = branch_to_palace(tian_wu_branches[(lunar_month - 1) % 4])
    add(tian_wu_idx, 'tian_wu')

    # 華蓋 (by year branch)
    hua_gai_idx, _ = _get_huagai_xianchi(year_branch)
    add(hua_gai_idx, 'hua_gai')

    # 天官天福 (by year stem)
    tian_guan_branches = ['wei','chen','si','yin','mao','you','hai','you','xu','wu']
    tian_fu_branches =   ['you','shen','zi','hai','mao','yin','wu','si','wu','si']
    stem_idx = HEAVENLY_STEMS.index(year_stem)
    add(branch_to_palace(tian_guan_branches[stem_idx]), 'tian_guan')
    add(branch_to_palace(tian_fu_branches[stem_idx]), 'tian_fu_xing')

    # 天廚 (by year stem)
    tian_chu_branches = ['si','wu','zi','si','wu','shen','yin','wu','you','hai']
    add(branch_to_palace(tian_chu_branches[stem_idx]), 'tian_chu')

    # 天月 (by lunar month)
    tian_yue_branches = ['xu','si','chen','yin','wei','mao','hai','wei','yin','wu','xu','yin']
    add(branch_to_palace(tian_yue_branches[lunar_month - 1]), 'tian_yue_xing')

    # 天德月德 (by year branch)
    tian_de_idx = fix_index(branch_to_palace('you') + year_branch_full)
    yue_de_idx = fix_index(branch_to_palace('si') + year_branch_full)
    add(tian_de_idx, 'tian_de')
    add(yue_de_idx, 'yue_de')

    # 天空 (year branch + 1)
    tian_kong_idx = fix_index(branch_to_palace(year_branch) + 1)
    add(tian_kong_idx, 'tian_kong')

    # 旬空 (by year stem)
    # xunkong: year_branch_full + (9 - stem_idx) + 1, adjust yin-yang
    xun_kong_idx = fix_index(branch_to_palace(year_branch) + (9 - stem_idx) + 1)
    year_branch_yinyang = year_branch_full % 2  # 0=yang, 1=yin
    if year_branch_yinyang != xun_kong_idx % 2:
        xun_kong_idx = fix_index(xun_kong_idx + 1)
    add(xun_kong_idx, 'xun_kong')

    # 截路空亡 (by year stem)
    jie_lu_branches = ['shen','wu','chen','yin','zi']
    kong_wang_branches = ['you','wei','si','mao','chou']
    add(branch_to_palace(jie_lu_branches[stem_idx % 5]), 'jie_lu')
    add(branch_to_palace(kong_wang_branches[stem_idx % 5]), 'kong_wang')

    # 孤辰寡宿 (by year branch)
    gu_chen_idx, gua_su_idx = _get_gu_gua(year_branch)
    add(gu_chen_idx, 'gu_chen')
    add(gua_su_idx, 'gua_su')

    # 蜚廉 (by year branch)
    fei_lian_map = ['shen','you','xu','si','wu','wei','yin','mao','chen','hai','zi','chou']
    add(branch_to_palace(fei_lian_map[year_branch_full]), 'fei_lian')

    # 破碎 (by year branch)
    po_sui_map = ['si','chou','you']  # 子午卯酉->巳, 寅申巳亥->酉, 辰戌丑未->丑
    po_sui_group = year_branch_full % 3
    add(branch_to_palace(po_sui_map[po_sui_group]), 'po_sui')

    # 天刑 (by lunar month): 酉宮起正月順
    tian_xing_idx = fix_index(branch_to_palace('you') + (lunar_month - 1))
    add(tian_xing_idx, 'tian_xing')

    # 陰煞 (by lunar month)
    yin_sha_branches = ['yin','zi','xu','shen','wu','chen']
    add(branch_to_palace(yin_sha_branches[(lunar_month - 1) % 6]), 'yin_sha')

    # 天哭天虛 (by year branch): 午宮起子逆/順
    tian_ku_idx = fix_index(branch_to_palace('wu') - year_branch_full)
    tian_xu_idx = fix_index(branch_to_palace('wu') + year_branch_full)
    add(tian_ku_idx, 'tian_ku')
    add(tian_xu_idx, 'tian_xu')

    # 天使天傷 (standard, non-中州派)
    # 天傷居奴僕(friends=5), 天使居疾厄(health=7)
    tian_shang_idx = fix_index(PALACE_CODES.index('friends') + soul_index)
    tian_shi_idx = fix_index(PALACE_CODES.index('health') + soul_index)
    add(tian_shang_idx, 'tian_shang')
    add(tian_shi_idx, 'tian_shi')

    # 年解 (by year branch)
    # 從戌上起子逆數
    nian_jie_map = ['xu','you','shen','wei','wu','si','chen','mao','yin','chou','zi','hai']
    add(branch_to_palace(nian_jie_map[year_branch_full]), 'nian_jie')

    return stars


def _get_huagai_xianchi(year_branch: str) -> tuple[int, int]:
    """華蓋咸池 indices by year branch."""
    mapping = {
        frozenset({'yin','wu','xu'}): ('xu','mao'),
        frozenset({'shen','zi','chen'}): ('chen','you'),
        frozenset({'si','you','chou'}): ('chou','wu'),
        frozenset({'hai','mao','wei'}): ('wei','zi'),
    }
    for group, (hg, xc) in mapping.items():
        if year_branch in group:
            return branch_to_palace(hg), branch_to_palace(xc)
    return 0, 0


def _get_gu_gua(year_branch: str) -> tuple[int, int]:
    """孤辰寡宿 indices by year branch."""
    mapping = {
        frozenset({'yin','mao','chen'}): ('si','chou'),
        frozenset({'si','wu','wei'}): ('shen','chen'),
        frozenset({'shen','you','xu'}): ('hai','wei'),
        frozenset({'hai','zi','chou'}): ('yin','xu'),
    }
    for group, (gu, gua) in mapping.items():
        if year_branch in group:
            return branch_to_palace(gu), branch_to_palace(gua)
    return 0, 0
