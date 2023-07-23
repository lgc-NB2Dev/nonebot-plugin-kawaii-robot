import asyncio
import random
from typing import Iterable, List, Optional

from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.matcher import Matcher

from .config import config
from .const import NICKNAME, ReplyDictType


def full_to_half(text: str) -> str:
    """
    全角转半角
    """
    return "".join(
        chr(ord(char) - 0xFEE0) if "\uFF01" <= char <= "\uFF5E" else char
        for char in text
    )


def full_match_search(resource: ReplyDictType, text: str) -> Optional[List[str]]:
    """
    从 resource 中获取回应：精确查找
    """
    return resource.get(full_to_half(text.lower()), None)


def keyword_search(resource: ReplyDictType, text: str) -> Optional[List[str]]:
    """
    从 resource 中获取回应：关键词查找
    """
    if len(text) > 20:
        return None

    text = full_to_half(text.lower())
    return next(
        (resource[key] for key in resource if key in text),
        None,
    )


def format_vars(string: str, user_id: str, username: str, **kwargs) -> List[str]:
    return string.format(
        segment="\u0000",
        user_id=user_id,
        username=username,
        bot_nickname=NICKNAME,
        **kwargs,
    ).split("\u0000")


def choice_reply(
    reply_list: List[str],
    user_id: str,
    username: str,
    **kwargs,
) -> List[Message]:
    """
    从提供的回复列表中随机选择一条回复并格式化
    """
    raw_reply = random.choice(reply_list)
    return [Message(x) for x in format_vars(raw_reply, user_id, username, **kwargs)]


def format_sender_username(username: Optional[str]) -> str:
    """
    格式化发送者的昵称，如果昵称过长则截断
    """
    username = username or "你"
    if len(username) > 10:
        username = username[:2] + random.choice(["酱", "亲", "ちゃん", "同志", "老师"])
    return username


def format_username_from_event(event: MessageEvent) -> str:
    """
    从 MessageEvent 中获取发送者的昵称并格式化
    """
    return format_sender_username(event.sender.card or event.sender.nickname)


async def get_username_by_id(bot: Bot, user_id: int, group_id: Optional[int]) -> str:
    """
    根据用户 id 获取用户昵称
    """
    if group_id:
        info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
        return info["card"] or info["nickname"]

    info = await bot.get_stranger_info(user_id=user_id)
    return info["nickname"]


def transform_message(message: Message) -> Message:
    """
    将收到的消息中的特殊 segment（比如图片）转换为可以发送的 segment（把 `url` 改成 `file`）
    """
    for x in (x for x in message if (not x.is_text() and "url" in x.data)):
        x.data["file"] = x.data.pop("url")
    return message


def check_percentage(need_percent: int, percentage: Optional[int] = None) -> bool:
    """
    检查概率
    """
    if need_percent <= 0:
        return False
    if need_percent >= 100:
        return True

    if not percentage:
        percentage = random.randint(1, 100)
    return percentage <= need_percent


async def finish_multi_msg(matcher: Matcher, msg_list: List[Message]):
    first_msg = msg_list.pop(0)
    await matcher.send(first_msg)

    for msg in msg_list:
        await asyncio.sleep(random.uniform(*config.leaf_multi_reply_delay))
        await matcher.send(msg)

    await matcher.finish()


def flatten_list(li: Iterable[Iterable[str]]) -> List[str]:
    """
    展平二维列表
    """
    return [x for y in li for x in y]
