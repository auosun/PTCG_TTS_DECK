# 高清下载地址
import os

HdCARDS = {
    'CS2bC-093': "https://www.pokemon.cn/assets_c/2023/08/22ade522ed077954a43ab95d457e5e68a2d996c6-thumb-1000xauto-20619.png",
    'CS2.5C-057': "https://www.pokemon.cn/assets_c/2023/09/bd1b6cdbaeb4907ecf83aac17cc0aaaa4c77e9f9-thumb-868x1207-21040.png"
}

# 雪道和疾患社卡组编号转换
# key为疾患社编号，value为雪道对应卡图编号
CODE_TRANS = {
    'CSM2.1C-DAR': 'CSM2.1C-043',
    'CSM2.1C-GRA': 'CSM2.1C-037'
}

CARD_SIZE = (600, 832)

CARD_URL = "https://636c-cloud1-9gd4kn3z06e5ac68-1309946562.tcb.qcloud.la/{number}/{code}.png"

DECK_URL = "https://api.jihuanshe.com/api/market/share/market-deck?market_deck_uuid={market_deck_uuid}&url=https://www.jihuanshe.com/app/userCardSet?marketDeckUuid={market_deck_uuid}%26gameKey=pkm%26language=sc"

DECK_UUID = open('uuid', 'r').read().strip()

DECK_PNG_LOCATION = 'static/decks/'

CARD_PNG_LOCATION = 'static/cards/'

FLASK_HOST = os.environ.get('HOST', '0.0.0.0')
FLASK_PORT = os.environ.get('PORT', 3000)
DEBUG = os.environ.get('DEBUG', True)
