from nonebot.adapters.onebot.v11 import Message, MessageSegment
from pathlib import Path

import nonebot
import os
import random

from nonebot.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json



Bot_NICKNAME: str = list(nonebot.get_driver().config.nickname)[0]      # bot的nickname,可以换成你自己的
Bot_MASTER: str = list(nonebot.get_driver().config.superusers)[0]      # bot的主人名称,也可以换成你自己的

path = os.path.join(os.path.dirname(__file__), "resource")

def sorted_my_dict(my_dict:dict) -> dict:
    """
    排序词库
    """
    return dict(sorted(my_dict.items(), key = lambda item:len(item[0]), reverse = True))

# 载入个人词库
lst = os.listdir(Path(path))
lst.remove("leaf.json")
lst.remove("data.json")
MyThesaurus = {}
for i in lst:
    try:
        tmp = json.load(open(Path(path) / i, "r", encoding="utf8"))
        logger.info(f"{i} 加载成功~")
        for key in tmp.keys():
            if not key in MyThesaurus.keys():
                MyThesaurus.update({key:[]})
            if type(tmp[key]) == list:
                MyThesaurus[key] += tmp[key]
            else:
                logger.info(f"\t文件 {i} 内 {key} 词条格式错误。")
    except UnicodeDecodeError:
        logger.info(f"{i} utf8解码出错！！！")
    except Exception as error:
        logger.info(f"错误：{error} {i} 加载失败...")

MyThesaurus = sorted_my_dict(MyThesaurus)

# 载入首选词库
LeafThesaurus = json.load(open(Path(path) / "leaf.json", "r", encoding="utf8"))

LeafThesaurus = sorted_my_dict(LeafThesaurus)

# 载入词库(这个词库有点涩)
AnimeThesaurus = json.load(open(Path(path) / "data.json", "r", encoding="utf8"))

AnimeThesaurus = sorted_my_dict(AnimeThesaurus)

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
unknow_reply = [
    f"{Bot_NICKNAME}不懂...",
    "呜喵？",
    "没有听懂喵...",
    "装傻（",
    "呜......",
    "喵喵？",
    "(,,• ₃ •,,)",
    "没有理解呢...",
]

# 打断复读
interrupt_msg = [
    "打断！",
    "打断复读！",
    MessageSegment.face(212),
    MessageSegment.face(318) + MessageSegment.face(318),
    MessageSegment.face(181),
]

def keyword_search(resource: dict, text: str) -> str:
    """
    从 resource 中获取回应：关键词查找
    """
    if len(text) < 21:
        keys = resource.keys()
        for key in keys:
            if text.find(key) != -1:
                return random.choice(resource[key])

def is_CQ_Code(msg:str) -> bool:
    '''
    判断参数是否为CQ码
    '''
    if len(msg) > 4 and msg[0] == '[' and msg[1:4] == "CQ:" and msg[-1] == ']':
        return True
    else:
        return False

def messagePreprocess(msg: Message):
    '''
    对CQ码返回文件名（主要是处理CQ:image）
    '''
    msg = str(msg)
    if is_CQ_Code(msg):
        data = msg.split(',')
        for x in data:
            if "file=" in x:
                return x
    return msg