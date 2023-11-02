from enum import Enum


class PDeckStatus(Enum):
    NOT_START = "尚未开始"
    DOWNLOADING = "下载卡片中……"
    MAKING = "生成TTS牌堆……"
    END = "生成完毕"
    ERROR = "错误"
