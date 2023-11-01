import os.path
import re
import time
from io import BytesIO

import requests
from PIL import Image

import settings

# 卡组信息处理
deck_url = settings.DECK_URL.format(market_deck_uuid=settings.DECK_UUID)

resp = requests.get(deck_url)
resp.raise_for_status()

deck_json = resp.json()
deck_name = deck_json['title']

deck_cards = deck_json['market_deck_cards'][0]['cards']

cards = list()
for item in deck_cards:
    codes = re.search(r'\/([^\/]*\-[A-Za-z0-9]{3})[^\/]*(\.jpg|\.png)', item['image_url'])
    cards.append((codes.groups()[0], item['count'], item['image_url']))

if not os.path.exists('pic'):
    os.makedirs('pic')

pics = os.listdir('pic')

for card_code, _, image_url in cards:
    card_name = f"{card_code}.png"
    if card_name in pics:
        print(f'{card_name} existed. continue.')
        continue

    if card_code in settings.HdCARDS:
        card_url = settings.HdCARDS[card_code]
    else:
        if card_code in settings.CODE_TRANS:
            card_code = settings.CODE_TRANS[card_code]

        card_url = settings.CARD_URL.format(number=card_code.split('-', 1)[0], code=card_code)

    response = requests.get(card_url)
    try:
        response.raise_for_status()
    except Exception as e:
        print(f'下载错误，可尝试 {image_url} 下载图片，并保存到pic中，文件名为: {card_name}')
        raise e

    img = Image.open(BytesIO(response.content))
    img.save(f'pic/{card_name}')
    print(f'{card_name} download success.')
    time.sleep(1)

new_image = Image.new('RGBA', (settings.CARD_SIZE[0] * 10, settings.CARD_SIZE[1] * 6))

for i, card_img_path in enumerate([f"{card_code}.png" for card_code, card_num, _ in cards for i in range(card_num)]):
    card_img = Image.open(f'pic/{card_img_path}').resize(settings.CARD_SIZE)

    row = i // 10
    col = i % 10

    left = col * card_img.width
    top = row * card_img.height

    new_image.paste(card_img, (left, top))

new_image.save(f'{deck_name}.png')
