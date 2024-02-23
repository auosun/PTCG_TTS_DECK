import json
import os.path
import random
import re
import time
from io import BytesIO

import requests
from PIL import Image

import settings
from constant import PDeckStatus
from template import PTCGTemplate


class PDeck:

    def __init__(self, deck_uuid, save_type):
        self.deck_uuid = deck_uuid
        self.deck_name = ""
        self.deck_cards = list()
        self.deck_png = ""
        self.error_msg = ""
        self.download_count = 0
        self.save_type = save_type or "img"

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

        jhs_cards = list()

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

                if card_code.startswith('S-P') or card_code.endswith('compress.jpeg?v=13'):
                    card_url = image_url
                else:
                    card_url = settings.CARD_URL.format(number=card_code.split('-', 1)[0], code=card_code)

            try:
                response = self.request_get(card_url)
            except Exception as e:
                if settings.DOWNLOAD_BLUR:
                    try:
                        card_name = f"{card_code}_jhs.png"
                        jhs_cards.append(card_code)
                        if card_name in pics:
                            continue

                        response = self.request_get(image_url)
                    except Exception as e:
                        self.error_msg = f'下载错误，可尝试 {image_url} 下载图片，并保存到{settings.CARD_PNG_LOCATION}中，文件名为: {card_name}'
                        raise e
                else:
                    self.error_msg = f'下载错误，可尝试 {image_url} 下载图片，并保存到{settings.CARD_PNG_LOCATION}中，文件名为: {card_name}'
                    raise e

            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(settings.CARD_PNG_LOCATION, card_name))

            print(f'{card_name} download success.')
            self.download_count += 1
            time.sleep(random.uniform(0.5, 1.5))

        if jhs_cards:
            new_deck_cards = list()
            for card_code, count, image_url in self.deck_cards:
                if card_code in jhs_cards:
                    card_code = f"{card_code}_jhs"

                new_deck_cards.append((card_code, count, image_url))

            self.deck_cards = new_deck_cards

    def request_get(self, card_url: str):
        response = requests.get(card_url)
        try:
            response.raise_for_status()
        except Exception as e:
            print(self.error_msg)
            raise e

        return response

    def save_img(self):
        new_image = Image.new('RGBA', (settings.CARD_SIZE[0] * 10, settings.CARD_SIZE[1] * 6))

        for i, card_img_path in enumerate(
                [f"{card_code}.png" for card_code, card_num, _ in self.deck_cards for _ in range(card_num)]):
            card_location = os.path.join(settings.CARD_PNG_LOCATION, card_img_path)
            card_img = Image.open(card_location).resize(settings.CARD_SIZE)

            row = i // 10
            col = i % 10

            left = col * card_img.width
            top = row * card_img.height

            new_image.paste(card_img, (left, top))

        self.deck_png = os.path.join(settings.DECK_PNG_LOCATION, f"{self.deck_uuid}.png")
        new_image.save(self.deck_png)

    def save_json(self):
        template = PTCGTemplate()
        template.set_deck_name(self.deck_name)
        cards = [
            (card_code, os.path.join(settings.CARD_PNG_LOCATION, f"{card_code}.png"))
            for card_code, count, image_url in self.deck_cards for _ in range(count)
        ]
        template.import_cards(cards)
        with open(os.path.join(settings.DECK_JSON_LOCATION, f"{self.deck_uuid}.json"), 'w') as file:
            json.dump(template.data, file, indent=2)

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
            save_method = getattr(self, "save_%s" % self.save_type)
            if not save_method:
                raise Exception("不存在当前保存方法")

            save_method()

        except Exception as e:
            print(str(e))
            self.error_msg = str(e)
            if settings.DEBUG:
                raise e
            else:
                return False

        return True


if __name__ == '__main__':
    for dir_name in [settings.CARD_PNG_LOCATION, settings.DECK_PNG_LOCATION]:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    PDeck('608ecb6e-9062-41e4-8e94-5baf6ddec925').execute()
