# 高清下载地址
HdCARDS = {
    'CS2bC-093': "https://www.pokemon.cn/assets_c/2023/08/22ade522ed077954a43ab95d457e5e68a2d996c6-thumb-1000xauto-20619.png",
    'CS2.5C-057': "https://www.pokemon.cn/assets_c/2023/09/bd1b6cdbaeb4907ecf83aac17cc0aaaa4c77e9f9-thumb-868x1207-21040.png"
}

# 雪道和疾患社卡组编号转换
# key为疾患社编号，value为雪道对应卡图编号
CODE_TRANS = {
    'CSM2.1C-DAR': 'CSM2.1C-043',  # 恶能
    'CSM2.1C-GRA': 'CSM2.1C-037',  # 草能
    'CSMPaC-GRA': 'CSM2.1C-037',  # 草能
    'CS3DC-GRA': 'CSM2.1C-037',  # 草能
    'CSMPiC---sc.png~tplv-la29u1ii6m-compress.jpeg?v=13': 'CSM2.1C-037',  # 草能

    'CSM2.1C-MET': 'CSM2.1C-044',  # 钢能
    'CSM2.1C-FAI': 'CSM2.1C-045',  # 仙能
    'CSM2.1C-WAT': 'CSM2.1C-039',  # 水能
    'CSM2.1C-FIR': 'CSM2.1C-038',  # 火能
    'CSM2.1C-PSY': 'CSM2.1C-041',  # 超能
    'CSM2.1C-FIG': 'CSM2.1C-042',  # 斗能
    'CSM2.1C-LIG': 'CSM2.1C-040',  # 电能
    'CS3DC-LIG': 'CSM2.1C-040',  # 基本电能
    'CS3DC-PSY': 'CSM2.1C-041',  # 超
    'CSCC-013': 'CS3DC-158',
    'CSCC-014': 'CS3DC-160',
    'CSCC-017': 'CS3bC-121',
    'CSCC-002': 'CS3bC-020',
    'CS2DaC-043': 'CS3DC-140',
    'CSBC-019': 'CS3DC-168',
}

_CARD_NAMES_ENERGY = {
    '基本恶能量': {'CSM2.1C-043', 'CSM2.1C-DAR', 'CS1DC-DAR', 'CSMPiC--_15-sc.png~tplv-la29u1ii6m-compress.jpeg?v=13'},
    '基本草能量': {'CSM2.1C-037', 'CSM2.1C-GRA', 'CS1DC-GRA'},
    '基本钢能量': {'CSM2.1C-044', 'CSM2.1C-MET', 'CSMPhC-MET', 'CS1DC-MET'},
    '基本仙能量': {'CSM2.1C-045', 'CSM2.1C-FAI'},
    '基本水能量': {'CSM2.1C-039', 'CSM2.1C-WAT', 'CSMAC-WAT', 'CSMPcC-WAT', 'CS1DC-WAT'},
    '基本火能量': {'CSM2.1C-038', 'CSM2.1C-FIR', 'CSMPbC-FIR', 'CS1DC-FIR'},
    '基本斗能量': {'CSM2.1C-042', 'CSM2.1C-FIG', 'CSMAC-FIG', 'CS1DC-FIG'},
    '基本雷能量': {'CSM2.1C-040', 'CS3DC-LIG', 'CSM2.1C-LIG', 'CSMPdC-LIG'},
    '基本超能量': {'CSM2.1C-041', 'CSM2.1C-PSY', 'CS3DC-PSY', 'CSAC-PSY', 'CS1DC-PSY', 'CSM1DC-PSY'},
    "捕获能量": {'CSBC-019', 'CS3DC-168', 'CS1.5C-055'},
    "极光能量": {'CSAC-024', },
    "连击能量": {'CSCC-019', 'CS3DC-170', 'CS3bC-179', 'CS3bC-122'},
    "高速雷能量": {'CS1.5C-053', },
    "一击能量": {'CS3aC-125', 'CS3DC-166'},
    "抽取能量": {'CSM2bC-150', },
    "循环能量": {'CSM2aC-150', },
    "强力普能量": {'CS2aC-115', },
    "三重加速能量": {'CSM2cC-150', },
    '岩石斗能量': {'CS2aC-114', },
    '弱点防守能量': {'CSM2.5C-061', 'CSM2.5C-099', },
    '高温火能量': {'CS1.5C-052', },
    '反击能量': {'CSM1bC-204', 'CSM1bC-150', },
    '组合能量': {'CSM1.5C-088', },
    '涂层钢能量': {'CS2.5C-059', },
    '潜行恶能量': {'CS2bC-115', },


}

_CARD_NAMES_ITEM = {
    "连击卷轴 滔天之卷": {'CS3bC-111', },
    "连击卷轴 漩涡之卷": {'CS3bC-112', },
    "惊悚超能量": {'CS1.5C-054', },
    "大护符": {'CS1DC-185', 'CS1aC-216', 'CSAC-016', 'CS1aC-125'},
    '活力头带': {'CS1bC-126', },
    '望远镜': {'CS2bC-143', 'CS2bC-108'},
    '黑带': {'CSMPfC-014', 'CSM2bC-191'},
    '气球': {'CS1bC-197', 'CSAC-017', 'CS1bC-128'},
    '隐秘风帽': {'CSM2bC-132', },
    '回转滑板': {'CSM2aC-192', },
    '反击增幅器': {'CSM2DC-357', },
    '逃脱滑板': {'CSM1aC-209', 'CSM2DC-275'},
    '讲究头带': {'CSM1cC-129', 'CSMAC-010', },
    '钢铁平底锅': {'CSM2.1C-022', 'CSM1aC-131'},
}

CARD_NAMES = {i: k for k, v in dict(**_CARD_NAMES_ENERGY, **_CARD_NAMES_ITEM).items() for i in v}
