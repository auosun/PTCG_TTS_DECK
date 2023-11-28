import json
import os

DEBUG = os.environ.get('DEBUG', "false").upper() == "TRUE"

from card_settings import *

CARD_SIZE = (600, 832)

CARD_URL = "https://636c-cloud1-9gd4kn3z06e5ac68-1309946562.tcb.qcloud.la/{number}/{code}.png"

DECK_URL = "https://api.jihuanshe.com/api/market/share/market-deck?market_deck_uuid={market_deck_uuid}&url=https://www.jihuanshe.com/app/userCardSet?marketDeckUuid={market_deck_uuid}%26gameKey=pkm%26language=sc"

DECK_UUID = '67c44874-f2bd-4235-8393-7661264f4a5e'

DECK_PNG_LOCATION = 'static/decks/'

CARD_PNG_LOCATION = 'static/cards/'

DECK_JSON_LOCATION = 'static/json/'

FLASK_HOST = os.environ.get('HOST', '0.0.0.0')
FLASK_PORT = os.environ.get('PORT', 3000)

CARD_BACK_URL = "http://cloud-3.steamusercontent.com/ugc/2160099523430329011/9BE66430CD3C340060773E321DDD5FD86C1F2703/"

CARD_URI = os.environ.get("CARD_URI", "http://127.0.0.1:3000")

DECK_TEMPLATE_FILE = "./tts_template.json"

with open(DECK_TEMPLATE_FILE, 'r') as file:
    # 使用 json.load() 将文件内容加载为 Python 字典
    DECK_TEMPLATE = json.load(file)

REMAKE_DECK_TIME = 60 * 3
