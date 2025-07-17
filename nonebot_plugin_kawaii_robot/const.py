from .config import config

ReplyDictType = dict[str, list[str]]

NICKNAME = next(iter(config.nickname)) if config.nickname else "可爱的咱"

# hello之类的回复
BUILTIN_HELLO_REPLY = [
    "你好喵~",
    "呜喵..？！",
    "你好OvO",
    "喵呜 ~ ，叫{bot_nickname}做什么呢☆",
    "怎么啦qwq",
    "呜喵 ~ ，干嘛喵？",
    "呼喵 ~ 叫可爱的咱有什么事嘛OvO",
]

# 戳一戳消息
BUILTIN_POKE_REPLY = [
    "嗯？",
    "戳我干嘛qwq",
    "呜喵？",
    "喵！",
    "呜...不要用力戳咱...好疼>_<",
    "请不要戳{bot_nickname} >_<",
    "放手啦，不给戳QAQ",
    "喵 ~ ！ 戳{bot_nickname}干嘛喵！",
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
BUILTIN_UNKNOWN_REPLY = [
    "{bot_nickname}不懂...",
    "呜喵？",
    "没有听懂喵...",
    "装傻（",
    "呜......",
    "喵喵？",
    "(,,• ₃ •,,)",
    "没有理解呢...",
]

# 打断复读
BUILTIN_INTERRUPT_MSG = [
    "打断！",
    "打断复读！",
    # "[CQ:face,id=212]",
    # "[CQ:face,id=318][CQ:face,id=318]",
    # "[CQ:face,id=181]",
]
