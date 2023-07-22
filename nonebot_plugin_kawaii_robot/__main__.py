import asyncio
import random
from typing import Dict, List, Optional

from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
    PokeNotifyEvent,
)
from nonebot.matcher import Matcher
from nonebot.plugin.on import on_message, on_notice
from nonebot.rule import Rule, to_me

from .config import config
from .data_source import (
    LOADED_HELLO_REPLY,
    LOADED_INTERRUPT_MSG,
    LOADED_POKE_REPLY,
    LOADED_REPLY_DICT,
    LOADED_UNKNOWN_REPLY,
)
from .utils import format_vars, full_match_search, keyword_search


def choice_reply(
    reply_list: List[str],
    user_id: str,
    username: str,
    **kwargs,
) -> Message:
    raw_reply = random.choice(reply_list)
    return Message(format_vars(raw_reply, user_id, username, **kwargs))


def format_sender_username(username: Optional[str]) -> str:
    username = username or "你"
    if len(username) > 10:
        username = username[:2] + random.choice(["酱", "亲", "ちゃん", "同志", "老师"])
    return username


async def get_username_by_id(bot: Bot, user_id: int, group_id: Optional[int]) -> str:
    if group_id:
        info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
        return info["card"] or info["nickname"]

    info = await bot.get_stranger_info(user_id=user_id)
    return info["nickname"]


# 触发权限
PERMISSION = GROUP if config.leaf_permission == "GROUP" else None


# 词库回复
if config.leaf_reply_type >= 0:

    async def ignore_rule(event: MessageEvent) -> bool:
        msg = event.get_plaintext().strip()
        if next(
            (x for x in config.leaf_ignore if msg.startswith(x)),
            None,
        ):
            return False

        if (not event.is_tome()) and (
            random.randint(1, 100) > config.leaf_trigger_percent
        ):
            return False

        return True

    talk = on_message(
        rule=Rule(ignore_rule) & (to_me() if config.leaf_at_mode == 0 else None),
        permission=PERMISSION,
        priority=99,
        block=False,
    )

    @talk.handle()
    async def _(matcher: Matcher, event: MessageEvent):
        # 获取消息文本
        msg = event.get_plaintext().strip()

        # 用户 id 和昵称处理
        user_id = event.get_user_id()
        username = format_sender_username(event.sender.card or event.sender.nickname)

        # 如果是光艾特bot(没消息返回)，就回复以下内容
        if not msg and config.leaf_at_mode == 0:
            await matcher.finish(choice_reply(LOADED_HELLO_REPLY, user_id, username))

        # 从词库中获取回复
        search_function = (
            keyword_search if config.leaf_match_pattern == 1 else full_match_search
        )
        if reply_list := search_function(LOADED_REPLY_DICT, msg):
            await matcher.finish(choice_reply(reply_list, user_id, username))

        # 不明白的内容，开启所有回复并 @bot 才会回复
        if event.is_tome() and config.leaf_reply_type == 1:
            await matcher.finish(choice_reply(LOADED_UNKNOWN_REPLY, user_id, username))


# 优先级10，不会向下阻断，条件：戳一戳bot触发
if config.leaf_poke_rand >= 0:
    poke_matcher = on_notice(rule=to_me(), priority=10, block=False)

    @poke_matcher.handle()
    async def _(bot: Bot, matcher: Matcher, event: PokeNotifyEvent):
        await asyncio.sleep(1)

        if config.leaf_poke_rand == 0 or random.randint(1, 100) > config.leaf_poke_rand:
            await matcher.finish(MessageSegment("poke", {"qq": event.user_id}))

        await matcher.finish(
            choice_reply(
                LOADED_POKE_REPLY,
                event.get_user_id(),
                format_sender_username(
                    await get_username_by_id(bot, event.user_id, event.group_id),
                ),
            ),
        )


def transform_message(message: Message) -> Message:
    """
    将收到的消息中的特殊 segment 转换为可以发送的 segment
    """
    for x in (x for x in message if (not x.is_text() and "url" in x.data)):
        x.data["file"] = x.data.pop("url")
    return message


# 打断/复读姬
if config.leaf_interrupt >= 0:
    msg_last: Dict[int, Message] = {}  # 存储群内最后一条消息
    msg_times: Dict[int, int] = {}  # 存储群内最后一条消息被复读的次数
    repeater_times: Dict[int, int] = {}  # 存储随机生成的复读上限

    async def repeat_rule(event: GroupMessageEvent) -> bool:
        group_id = event.group_id

        # 复读
        if msg_last.get(group_id) == event.message:
            msg_times[group_id] += 1
            if group_id not in repeater_times:
                repeater_times[group_id] = random.randint(*config.leaf_repeater_limit)

            if msg_times[group_id] >= repeater_times[group_id]:
                del msg_times[group_id]
                del repeater_times[group_id]
                return True

            return False

        # 不同消息，未复读
        msg_last[group_id] = event.message
        msg_times[group_id] = 1
        return False

    repeater = on_message(rule=repeat_rule, permission=GROUP, priority=99, block=False)

    @repeater.handle()
    async def _(event: GroupMessageEvent):
        if random.randint(1, 100) <= config.leaf_interrupt:
            await repeater.finish(
                choice_reply(
                    LOADED_INTERRUPT_MSG,
                    event.get_user_id(),
                    format_sender_username(event.sender.card or event.sender.nickname),
                ),
            )
        await repeater.finish(transform_message(event.message))
