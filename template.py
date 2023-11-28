import copy
import hashlib
import os.path
import typing

from settings import DECK_TEMPLATE, CARD_BACK_URL, CARD_NAMES, CARD_URI


class TTSTemplate(object):

    def __init__(self, template=None):
        self.template = copy.deepcopy(DECK_TEMPLATE) if template is None else template

    def set_deck_name(self, deck_name):
        self.template['ObjectStates'][0]['Name'] = deck_name

    def _custom_deck(self):
        return self.template['ObjectStates'][0]['CustomDeck']

    def _contained_object(self):
        return self.template['ObjectStates'][0]['ContainedObjects']

    @property
    def data(self):
        return self.template


class PTCGTemplate(TTSTemplate):
    back_card = CARD_BACK_URL

    def import_cards(self, cards: typing.List[typing.Tuple[str, str]]):
        """
        :param cards: [(card_code, card_url), ]
        :return:
        """
        if len(cards) != 60:
            raise Exception("PTCG牌组至少要60张")

        cards_dict = {str(index): card_obj for index, card_obj in enumerate(cards, start=1)}

        for k, v in self._custom_deck().items():
            card_code, card_url = cards_dict.get(k)
            v['FaceURL'] = os.path.join(CARD_URI, card_url)
            v['BackURL'] = self.back_card

        for obj in self._contained_object():
            card_code, card_url = None, None
            for k, v in obj['CustomDeck'].items():
                card_code, card_url = cards_dict.get(k)
                v['FaceURL'] = os.path.join(CARD_URI, card_url)
                v['BackURL'] = self.back_card

            card_name = CARD_NAMES.get(card_code, self.md5(card_code))
            obj['Nickname'] = card_name

    @staticmethod
    def md5(card_code):
        # 创建一个MD5哈希对象
        md5_hash = hashlib.md5()

        # 使用update()方法将字符串的字节表示添加到哈希对象中
        md5_hash.update(card_code.encode())

        # 获取MD5哈希值的十六进制表示
        md5_hex = md5_hash.hexdigest()

        return str(md5_hex)
