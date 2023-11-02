import os
import threading
import time

from flask import Flask, render_template, request

import settings
from constant import PDeckStatus
from p_deck import PDeck

app = Flask(__name__)

decks = list()
error_deck = dict()


def exec_make_deck():
    while True:
        if decks:
            deck_obj = decks[0]
            result = deck_obj.execute()
            if not result:
                error_deck[deck_obj.deck_uuid] = deck_obj.error_msg

            decks.pop(0)

        time.sleep(10)


@app.route('/', methods=['GET'])
def convert_deck():
    deck_uuid = request.args.get('deck_uuid')
    if deck_uuid is None:
        return render_template('index.html')

    if deck_uuid in error_deck:
        return render_template('index.html', execute_msg=f"{deck_uuid}卡组制作错误了，{error_deck[deck_uuid]}")

    png_uuids = [os.path.splitext(i)[0] for i in os.listdir(settings.DECK_PNG_LOCATION)]
    if deck_uuid in png_uuids:
        return render_template('index.html', execute_msg="制作完成", deck_png=os.path.join(settings.DECK_PNG_LOCATION, f"{deck_uuid}.png"))

    g_decks = [d.deck_uuid for d in decks]
    if deck_uuid in g_decks:
        location = g_decks.index(deck_uuid)
        if location == 0:
            execute_status = decks[0].execute_status
        else:
            execute_status = PDeckStatus.NOT_START

        msg = f"{deck_uuid}卡组已在队列中，当前状态{execute_status.value}。"
        if location == 0:
            msg += f"下载进度 {decks[0].download_count}/60"
        else:
            msg += f"当前排位 {location}"

        return render_template('index.html', execute_msg=msg)

    decks.append(PDeck(deck_uuid))
    return render_template('index.html', execute_msg=f"{deck_uuid}卡组制作进入队列，当前排位{len(decks)}")


if __name__ == '__main__':
    for dir_name in [settings.CARD_PNG_LOCATION, settings.DECK_PNG_LOCATION]:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    threading.Thread(target=exec_make_deck, args=()).start()
    app.run()
