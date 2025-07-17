import asyncio
import random
import re
from collections.abc import Iterable
from typing import Optional, TypedDict

from nonebot.matcher import current_bot, current_event, current_matcher
from nonebot_plugin_alconna.uniseg import At, Reply, UniMessage, get_message_id
from nonebot_plugin_userinfo import UserInfo, get_user_info

from .config import config
from .const import NICKNAME, ReplyDictType

SEG_SAMPLE = "{segment}"
SEG_REGEX = re.compile(r"(?P<h>[^\{])" + re.escape(SEG_SAMPLE) + r"(?P<t>[^\}])")

DEFAULT_USER_CALLING = "你"


def split_seg(text: str) -> list[str]:
    text = text.removeprefix(SEG_SAMPLE)
    text = text.removesuffix(SEG_SAMPLE)

    results = list(re.finditer(SEG_REGEX, text))
    if not results:
        return [text]

    parts = []
    last_index = 0
    for match in results:
        h = match.group("h")
        t = match.group("t")
        now_index = match.start() + (len(h) if h else 0)
        if now_index > last_index:
            parts.append(text[last_index:now_index])
        last_index = match.end() - (len(t) if t else 0)

    if last_index < len(text):
        parts.append(text[last_index:])

    return parts


def flatten_list(li: Iterable[Iterable[str]]) -> list[str]:
    """
    展平二维列表
    """
    return [x for y in li for x in y]


def full_to_half(text: str) -> str:
    """
    全角转半角
    """
    return "".join(
        chr(ord(char) - 0xFEE0) if "\uff01" <= char <= "\uff5e" else char
        for char in text
    )


def search_reply_dict(reply_dict: ReplyDictType, text: str) -> Optional[list[str]]:
    """
    在词库中搜索回复
    """
    text = full_to_half(text.lower())

    if config.leaf_match_pattern == 0:
        return reply_dict.get(text)

    if config.leaf_search_max > 0 and len(text) > config.leaf_search_max:
        return None

    generator = (reply_dict[key] for key in reply_dict if key in text)
    if config.leaf_match_pattern == 1:
        return next(generator, None)

    return flatten_list(list(generator)) or None


def format_sender_username(username: Optional[str]) -> str:
    """
    格式化发送者的昵称，如果昵称过长则截断
    """
    username = username or "你"
    if len(username) > 10:
        username = username[:2] + random.choice(["酱", "亲", "ちゃん", "同志", "老师"])
    return username


def get_username(info: UserInfo) -> str:
    return format_sender_username(info.user_displayname or info.user_name or "你")


class BuiltInVarDict(TypedDict):
    user_id: str
    username: str
    message_id: Optional[str]
    bot_nickname: str
    at: At
    reply: Optional[Reply]


def format_vars(
    string: str,
    builtin: BuiltInVarDict,
    **extra,
) -> list[UniMessage]:
    return [
        UniMessage.template(seg).format(**builtin, **extra) for seg in split_seg(string)
    ]


async def get_builtin_vars_from_ev() -> BuiltInVarDict:
    bot = current_bot.get()
    event = current_event.get()
    user_id = event.get_user_id()
    user_info = await get_user_info(bot, event, user_id)
    try:
        message_id = get_message_id(event=event, bot=bot)
    except Exception:
        message_id = None
    return {
        "user_id": user_id,
        "username": get_username(user_info) if user_info else DEFAULT_USER_CALLING,
        "message_id": message_id,
        "bot_nickname": NICKNAME,
        "at": At("user", user_id),
        "reply": Reply(message_id) if message_id else None,
    }


async def choice_reply_from_ev(reply_list: list[str], **kwargs) -> list[UniMessage]:
    """
    从提供的回复列表中随机选择一条回复并格式化
    """
    raw_reply = random.choice(reply_list)
    return format_vars(raw_reply, await get_builtin_vars_from_ev(), **kwargs)


def check_percentage(need_percent: float, percentage: Optional[float] = None) -> bool:
    """
    检查概率
    """
    if need_percent <= 0:
        return False
    if need_percent >= 100:
        return True

    if not percentage:
        percentage = random.random() * 100
    return percentage <= need_percent


async def finish_multi_msg(msg_list: list[UniMessage]):
    first_msg = msg_list.pop(0)
    await first_msg.send()

    for msg in msg_list:
        await asyncio.sleep(random.uniform(*config.leaf_multi_reply_delay))
        await msg.send()

    await current_matcher.get().finish()
