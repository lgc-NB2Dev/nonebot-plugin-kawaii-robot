from pathlib import Path
import os
import random
import nonebot
try:
    import ujson as json
except ModuleNotFoundError:
    import json
from httpx import AsyncClient
import re

Bot_NICKNAME: str = list(nonebot.get_driver().config.nickname)[0]      # bot的nickname,可以换成你自己的
Bot_MASTER: str = list(nonebot.get_driver().config.superusers)[0]      # bot的主人名称,也可以换成你自己的

# 载入词库(这个词库有点涩)
AnimeThesaurus = json.load(open(Path(os.path.join(os.path.dirname(__file__), "resource")) / "data.json", "r", encoding="utf8"))
# 载入备用词库
LeafThesaurus = json.load(open(Path(os.path.join(os.path.dirname(__file__), "resource")) / "leaf.json", "r", encoding="utf8"))

# 向bot打招呼
hello__bot = [
    "你好啊",
    "你好",
    "在吗",
    "在不在",
    "您好",
    "您好啊",
    "你好",
    "在",
    "早",
]

# hello之类的回复
hello__reply = [
    "你好喵~",
    "呜喵..？！",
    "你好OvO",
    f"喵呜 ~ ，叫{Bot_NICKNAME}做什么呢☆",
    "怎么啦qwq",
    "呜喵 ~ ，干嘛喵？",
    "呼喵 ~ 叫可爱的咱有什么事嘛OvO"
]

# 戳一戳消息
poke__reply = [
    "嗯？",
    "戳我干嘛qwq",
    "呜喵？",
    "喵！",
    "呜...不要用力戳咱...好疼>_<",
    f"请不要戳{Bot_NICKNAME} >_<",
    "放手啦，不给戳QAQ",
    f"喵 ~ ！ 戳{Bot_NICKNAME}干嘛喵！",
    "戳坏了，你赔！",
    "呜......戳坏了",
    "呜呜......不要乱戳",
    "喵喵喵？OvO",
    "(。´・ω・)ん?",
    "怎么了喵？",
    "呜喵！......不许戳 (,,• ₃ •,,)",
    "有什么吩咐喵？",
    "啊呜 ~ ",
    "呼喵 ~ 叫可爱的咱有什么事嘛OvO",
]

# 不明白的消息
cant__reply = [
    f"{Bot_NICKNAME}不懂...",
    "呜喵？",
    "没有听懂喵...",
    "装傻（",
    "呜......",
    "喵喵？",
    "(,,• ₃ •,,)",
    "没有理解呢...",
]

# 从字典里返还消息
async def get_chat_result(text: str, nickname: str) -> str:
    if len(text) < 70:
        keys = AnimeThesaurus.keys()
        for key in keys:
            if text.find(key) != -1:
                return random.choice(AnimeThesaurus[key]).replace("你", nickname)

# 从备用字典里返还消息
async def get_chat_result2(text: str, nickname: str) -> str:
    if len(text) < 70:
        keys = LeafThesaurus.keys()
        for key in keys:
            if text.find(key) != -1:
                return random.choice(LeafThesaurus[key]).replace("name", nickname)