import os.path
import random
import re
import time
from io import BytesIO

import requests
from PIL import Image

import settings
from constant import PDeckStatus


class PDeck:

    def __init__(self, deck_uuid):
        self.deck_uuid = deck_uuid
        self.deck_name = ""
        self.deck_cards = list()
        self.deck_png = ""
        self.error_msg = ""
        self.download_count = 0

    def request_deck(self):
        deck_url = settings.DECK_URL.format(market_deck_uuid=self.deck_uuid)
        resp = requests.get(deck_url)
        resp.raise_for_status()
        deck_json = resp.json()
        self.deck_name = deck_json['title']

        deck_cards = deck_json['market_deck_cards'][0]['cards']

        cards = list()
        for item in deck_cards:
            codes = re.search(r'\/([^\/]*\-[A-Za-z0-9]{3})[^\/]*(\.jpg|\.png)', item['image_url'])
            if not codes:
                cards.append((os.path.basename(item['image_url']), item['count'], item['image_url']))
            else:
                cards.append((codes.groups()[0], item['count'], item['image_url']))

        self.deck_cards = cards

    def download_cards(self):
        pics = os.listdir(settings.CARD_PNG_LOCATION)

        for card_code, _, image_url in self.deck_cards:
            card_name = f"{card_code}.png"
            if card_name in pics:
                print(f'{card_name} existed. continue.')
                self.download_count += 1
                continue

            if card_code in settings.HdCARDS:
                card_url = settings.HdCARDS[card_code]
            else:
                if card_code in settings.CODE_TRANS:
                    card_code = settings.CODE_TRANS[card_code]

                if card_code.startswith('S-P'):
                    card_url = image_url
                else:
                    card_url = settings.CARD_URL.format(number=card_code.split('-', 1)[0], code=card_code)

            response = requests.get(card_url)
            try:
                response.raise_for_status()
            except Exception as e:
                self.error_msg = f'下载错误，可尝试 {image_url} 下载图片，并保存到{settings.CARD_PNG_LOCATION}中，文件名为: {card_name}'
                print(self.error_msg)
                raise e

            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(settings.CARD_PNG_LOCATION, card_name))

            print(f'{card_name} download success.')
            self.download_count += 1
            time.sleep(random.uniform(0.5,1.5))

    def save_img(self):
        new_image = Image.new('RGBA', (settings.CARD_SIZE[0] * 10, settings.CARD_SIZE[1] * 6))

        for i, card_img_path in enumerate(
                [f"{card_code}.png" for card_code, card_num, _ in self.deck_cards for _ in range(card_num)]):
            card_img = Image.open(os.path.join(settings.CARD_PNG_LOCATION, card_img_path)).resize(settings.CARD_SIZE)

            row = i // 10
            col = i % 10

            left = col * card_img.width
            top = row * card_img.height

            new_image.paste(card_img, (left, top))

        self.deck_png = os.path.join(settings.DECK_PNG_LOCATION, f"{self.deck_uuid}.png")
        new_image.save(self.deck_png)

    @property
    def execute_status(self):

        if self.error_msg:
            return PDeckStatus.ERROR

        if not self.deck_name or not self.deck_cards:
            return PDeckStatus.NOT_START
        elif len(self.deck_cards) < 60:
            return PDeckStatus.DOWNLOADING
        elif not self.deck_png:
            return PDeckStatus.MAKING
        else:
            return PDeckStatus.END

    def execute(self):
        try:
            self.request_deck()
            self.download_cards()
            self.save_img()
        except Exception as e:
            print(str(e))
            self.error_msg = str(e)
            return False

        return True


if __name__ == '__main__':
    for dir_name in [settings.CARD_PNG_LOCATION, settings.DECK_PNG_LOCATION]:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    PDeck(settings.DECK_UUID).execute()
