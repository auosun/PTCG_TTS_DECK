import os.path
import re
import time
from io import BytesIO

import requests
from PIL import Image

# 高清下载地址
HdCARDS = {
    'CS2bC-093': "https://www.pokemon.cn/assets_c/2023/08/22ade522ed077954a43ab95d457e5e68a2d996c6-thumb-1000xauto-20619.png",
    'CS2.5C-057': "https://www.pokemon.cn/assets_c/2023/09/bd1b6cdbaeb4907ecf83aac17cc0aaaa4c77e9f9-thumb-868x1207-21040.png"
}

# 雪道和疾患社卡组编号转换
# key为疾患社编号，value为雪道对应卡图编号
CODE_TRANS = {
    'CSM2.1C-DAR': 'CSM2.1C-043'
}

CARD_SIZE = (600, 832)

CARD_URL = "https://636c-cloud1-9gd4kn3z06e5ac68-1309946562.tcb.qcloud.la/{number}/{code}.png"

DECK_URL = "https://api.jihuanshe.com/api/market/share/market-deck?market_deck_uuid={market_deck_uuid}&url=https://www.jihuanshe.com/app/userCardSet?marketDeckUuid={market_deck_uuid}%26gameKey=pkm%26language=sc"

DECK_UUID = open('uuid', 'r').read().strip()

# 卡组信息处理
deck_url = DECK_URL.format(market_deck_uuid=DECK_UUID)

resp = requests.get(deck_url)
resp.raise_for_status()

deck_json = resp.json()
deck_name = deck_json['title']

deck_cards = deck_json['market_deck_cards'][0]['cards']

cards = list()
for item in deck_cards:
    codes = re.search(r'\/([^\/]*\-[A-Za-z0-9]{3})[^\/]*(\.jpg|\.png)', item['image_url'])
    cards.append((codes.groups()[0], item['count']))

for code, count in cards:
    print(code, count)

if not os.path.exists('pic'):
    os.makedirs('pic')

pics = os.listdir('pic')

for card_code, _ in cards:
    card_name = f"{card_code}.png"
    if card_name in pics:
        print(f'{card_name} existed. continue.')
        continue

    if card_code in HdCARDS:
        card_url = HdCARDS[card_code]
    else:
        if card_code in CODE_TRANS:
            card_code = CODE_TRANS[card_code]

        card_url = CARD_URL.format(number=card_code.split('-', 1)[0], code=card_code)

    response = requests.get(card_url)
    response.raise_for_status()

    img = Image.open(BytesIO(response.content))
    img.save(f'pic/{card_name}')
    print(f'{card_name} download success.')
    time.sleep(1)

new_image = Image.new('RGBA', (CARD_SIZE[0] * 10, CARD_SIZE[1] * 6))

for i, card_img_path in enumerate([f"{card_code}.png" for card_code, card_num in cards for i in range(card_num)]):
    card_img = Image.open(f'pic/{card_img_path}').resize(CARD_SIZE)

    row = i // 10
    col = i % 10

    left = col * card_img.width
    top = row * card_img.height

    new_image.paste(card_img, (left, top))

new_image.save(f'{deck_name}.png')
