# Ten Heavenly Stems (十天干)
HEAVENLY_STEMS = ['jia','yi','bing','ding','wu','ji','geng','xin','ren','gui']

# Twelve Earthly Branches (十二地支)
EARTHLY_BRANCHES = ['zi','chou','yin','mao','chen','si','wu','wei','shen','you','xu','hai']

# Palace codes in order starting from 命宮 counterclockwise (increasing palace index)
PALACE_CODES = ['life','parents','spirit','property','career','friends','travel','health','wealth','children','spouse','siblings']

# Traditional Chinese names
HEAVENLY_STEM_ZH = {'jia':'甲','yi':'乙','bing':'丙','ding':'丁','wu':'戊','ji':'己','geng':'庚','xin':'辛','ren':'壬','gui':'癸'}
EARTHLY_BRANCH_ZH = {'zi':'子','chou':'丑','yin':'寅','mao':'卯','chen':'辰','si':'巳','wu':'午','wei':'未','shen':'申','you':'酉','xu':'戌','hai':'亥'}
PALACE_ZH = {'life':'命宮','parents':'父母宮','spirit':'福德宮','property':'田宅宮','career':'事業宮','friends':'交友宮','travel':'遷移宮','health':'疾厄宮','wealth':'財帛宮','children':'子女宮','spouse':'夫妻宮','siblings':'兄弟宮'}

# Five Elements Bureau (五行局): key -> number
FIVE_ELEMENTS_CLASS = {'water2': 2, 'wood3': 3, 'metal4': 4, 'earth5': 5, 'fire6': 6}
FIVE_ELEMENTS_ZH = {'water2':'水二局','wood3':'木三局','metal4':'金四局','earth5':'土五局','fire6':'火六局'}
FIVE_ELEMENTS_EN = {'water2':'Water 2nd','wood3':'Wood 3rd','metal4':'Metal 4th','earth5':'Earth 5th','fire6':'Fire 6th'}
# lookup table: stem+branch sum index (1-5) -> five elements class key
# 1=wood3, 2=metal4, 3=water2, 4=fire6, 5=earth5
FIVE_ELEMENTS_TABLE = ['wood3','metal4','water2','fire6','earth5']

# Tiger Rule (五虎遁): year heavenly stem -> yin-palace heavenly stem
TIGER_RULE = {
    'jia':'bing','yi':'wu','bing':'geng','ding':'ren','wu':'jia',
    'ji':'bing','geng':'wu','xin':'geng','ren':'ren','gui':'jia'
}

# Yang earthly branches
YANG_BRANCHES = {'zi','yin','chen','wu','shen','xu'}

# Soul master (命主) by soul palace branch
SOUL_MASTER = {
    'zi':'tan_lang','chou':'ju_men','yin':'lu_cun','mao':'wen_qu',
    'chen':'lian_zhen','si':'wu_qu','wu':'po_jun','wei':'wu_qu',
    'shen':'lian_zhen','you':'wen_qu','xu':'lu_cun','hai':'ju_men'
}
SOUL_MASTER_ZH = {
    'zi':'貪狼','chou':'巨門','yin':'祿存','mao':'文曲',
    'chen':'廉貞','si':'武曲','wu':'破軍','wei':'武曲',
    'shen':'廉貞','you':'文曲','xu':'祿存','hai':'巨門'
}

# Body master (身主) by birth year branch
BODY_MASTER = {
    'zi':'huo_xing','chou':'tian_xiang','yin':'tian_liang','mao':'tian_tong',
    'chen':'wen_chang','si':'tian_ji','wu':'huo_xing','wei':'tian_xiang',
    'shen':'tian_liang','you':'tian_tong','xu':'wen_chang','hai':'tian_ji'
}
BODY_MASTER_ZH = {
    'zi':'火星','chou':'天相','yin':'天梁','mao':'天同',
    'chen':'文昌','si':'天機','wu':'火星','wei':'天相',
    'shen':'天梁','you':'天同','xu':'文昌','hai':'天機'
}

# Brightness display
BRIGHTNESS_ZH = {'miao':'廟','wang':'旺','de':'得','li':'利','ping':'平','bu':'不','xian':'陷','':''}
BRIGHTNESS_EN = {'miao':'Brilliant','wang':'Prosperous','de':'Favorable','li':'Beneficial','ping':'Neutral','bu':'Weak','xian':'Fallen','':''}

# Transformation display
TRANSFORM_ZH = {'lu':'化祿','quan':'化權','ke':'化科','ji':'化忌'}
TRANSFORM_EN = {'lu':'Prosperity','quan':'Authority','ke':'Elegance','ji':'Obstacle'}

# Yin-yang per earthly branch (yang=0, yin=1)
BRANCH_YINYANG = {'zi':0,'chou':1,'yin':0,'mao':1,'chen':0,'si':1,'wu':0,'wei':1,'shen':0,'you':1,'xu':0,'hai':1}

# Hour branch mapping: time_index (0-12) -> earthly branch
# 0=早子, 1=丑, 2=寅, 3=卯, 4=辰, 5=巳, 6=午, 7=未, 8=申, 9=酉, 10=戌, 11=亥, 12=晚子
HOUR_BRANCH = ['zi','chou','yin','mao','chen','si','wu','wei','shen','you','xu','hai','zi']
HOUR_ZH = ['子時','丑時','寅時','卯時','辰時','巳時','午時','未時','申時','酉時','戌時','亥時','子時']

# Time ranges for each hour index
TIME_RANGE = ['00:00-01:00','01:00-03:00','03:00-05:00','05:00-07:00','07:00-09:00','09:00-11:00',
              '11:00-13:00','13:00-15:00','15:00-17:00','17:00-19:00','19:00-21:00','21:00-23:00','23:00-00:00']

# 四化 mutagens per year heavenly stem: [lu, quan, ke, ji]
MUTAGENS = {
    'jia': ['lian_zhen','po_jun','wu_qu','tai_yang'],
    'yi':  ['tian_ji','tian_liang','zi_wei','tai_yin'],
    'bing':['tian_tong','tian_ji','wen_chang','lian_zhen'],
    'ding':['tai_yin','tian_tong','tian_ji','ju_men'],
    'wu':  ['tan_lang','tai_yin','you_bi','tian_ji'],
    'ji':  ['wu_qu','tan_lang','tian_liang','wen_qu'],
    'geng':['tai_yang','wu_qu','tai_yin','tian_tong'],
    'xin': ['ju_men','tai_yang','wen_qu','wen_chang'],
    'ren': ['tian_liang','zi_wei','zuo_fu','wu_qu'],
    'gui': ['po_jun','ju_men','tai_yin','tan_lang'],
}

# Star canonical codes -> Traditional Chinese names
STAR_ZH = {
    # 14 major stars
    'zi_wei':'紫微','tian_ji':'天機','tai_yang':'太陽','wu_qu':'武曲',
    'tian_tong':'天同','lian_zhen':'廉貞','tian_fu':'天府','tai_yin':'太陰',
    'tan_lang':'貪狼','ju_men':'巨門','tian_xiang':'天相','tian_liang':'天梁',
    'qi_sha':'七殺','po_jun':'破軍',
    # 14 minor stars
    'zuo_fu':'左輔','you_bi':'右弼','wen_chang':'文昌','wen_qu':'文曲',
    'tian_kui':'天魁','tian_yue':'天鉞','lu_cun':'祿存','tian_ma':'天馬',
    'di_kong':'地空','di_jie':'地劫','huo_xing':'火星','ling_xing':'鈴星',
    'qing_yang':'擎羊','tuo_luo':'陀羅',
    # Adjective / misc stars
    'hong_luan':'紅鸞','tian_xi':'天喜','tian_yao':'天姚','xian_chi':'咸池',
    'jie_shen':'解神','san_tai':'三台','ba_zuo':'八座','en_guang':'恩光',
    'tian_gui':'天貴','long_chi':'龍池','feng_ge':'鳳閣','tian_cai':'天才',
    'tian_shou':'天壽','tai_fu':'台輔','feng_gao':'封誥','tian_wu':'天巫',
    'hua_gai':'華蓋','tian_guan':'天官','tian_fu_xing':'天福','tian_chu':'天廚',
    'tian_yue_xing':'天月','tian_de':'天德','yue_de':'月德','tian_kong':'天空',
    'xun_kong':'旬空','gu_chen':'孤辰','gua_su':'寡宿','fei_lian':'蜚廉',
    'po_sui':'破碎','tian_xing':'天刑','yin_sha':'陰煞','tian_ku':'天哭',
    'tian_xu':'天虛','tian_shi':'天使','tian_shang':'天傷','nian_jie':'年解',
    'jie_lu':'截路','kong_wang':'空亡',
    # Changsheng 12
    'chang_sheng':'長生','mu_yu':'沐浴','guan_dai':'冠帶','lin_guan':'臨官',
    'di_wang':'帝旺','shuai':'衰','bing':'病','si':'死','mu':'墓',
    'jue':'絕','tai':'胎','yang':'養',
    # Boshi 12
    'bo_shi':'博士','li_shi':'力士','qing_long':'青龍','xiao_hao':'小耗',
    'jiang_jun':'將軍','zou_shu':'奏書','fei_lian_b':'飛廉','xi_shen':'喜神',
    'bing_fu':'病符','da_hao':'大耗','fu_bing':'伏兵','guan_fu':'官府',
    # Jiangqian 12
    'jiang_xing':'將星','pan_an':'攀鞍','sui_yi':'歲驛','xi_shen2':'息神',
    'hua_gai2':'華蓋','jie_sha':'劫煞','zhai_sha':'災煞','tian_sha':'天煞',
    'zhi_bei':'指背','xian_chi2':'咸池','yue_sha':'月煞','wang_shen':'亡神',
    # Suiqian 12
    'sui_jian':'歲建','hui_qi':'晦氣','sang_men':'喪門','guan_suo':'貫索',
    'guan_fu2':'官符','xiao_hao2':'小耗','da_hao2':'大耗','long_de':'龍德',
    'bai_hu':'白虎','tian_de2':'天德','diao_ke':'弔客','bing_fu2':'病符',
}

# Star English names
STAR_EN = {
    'zi_wei':'Purple Star','tian_ji':'Heavenly Mechanism','tai_yang':'Sun',
    'wu_qu':'Military Melody','tian_tong':'Heavenly Unity','lian_zhen':'Integrity',
    'tian_fu':'Heavenly Store','tai_yin':'Moon','tan_lang':'Greedy Wolf',
    'ju_men':'Great Gate','tian_xiang':'Heavenly Minister','tian_liang':'Heavenly Roof',
    'qi_sha':'Seven Killings','po_jun':'Dissolution',
    'zuo_fu':'Left Assistant','you_bi':'Right Supporter','wen_chang':'Literary Prosperity',
    'wen_qu':'Literary Grace','tian_kui':'Heavenly Opening','tian_yue':'Heavenly Halberd',
    'lu_cun':'Prosperity Essence','tian_ma':'Heavenly Horse',
    'di_kong':'Earthly Emptiness','di_jie':'Earthly Robbery',
    'huo_xing':'Fire Star','ling_xing':'Bell Star',
    'qing_yang':'Ram Blade','tuo_luo':'Spinning Rope',
}
