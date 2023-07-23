import asyncio
import random
from typing import Dict

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
from .utils import (
    check_percentage,
    choice_reply,
    format_sender_username,
    format_username_from_event,
    full_match_search,
    get_username_by_id,
    keyword_search,
    transform_message,
)

# region 词库回复


async def ignore_rule(event: MessageEvent) -> bool:
    msg = event.get_plaintext().strip()

    # 消息以忽略词开头
    if next(
        (x for x in config.leaf_ignore if msg.startswith(x)),
        None,
    ):
        return False

    # at 始终触发
    if event.is_tome():
        return True

    # 没 at，启用非 at 回复，并且概率满足
    if (
        # (not event.is_tome()) and
        (not config.leaf_at_mode)
        and check_percentage(config.leaf_trigger_percent)
    ):
        return True

    return False


async def talk_matcher_handler(matcher: Matcher, event: MessageEvent):
    # 获取消息文本
    msg = event.get_plaintext().strip()

    # 用户 id 和昵称处理
    user_id = event.get_user_id()
    username = format_username_from_event(event)

    # 如果是光艾特bot(没消息返回)，就回复以下内容
    if (not msg) and event.is_tome():
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


DICT_REPLY_PERM = GROUP if config.leaf_permission == "GROUP" else None
talk = on_message(
    rule=Rule(ignore_rule) & (to_me() if config.leaf_at_mode else None),
    permission=DICT_REPLY_PERM,
    priority=99,
    block=False,
)
if config.leaf_reply_type >= 0:
    talk.handle()(talk_matcher_handler)


# endregion


# region 戳一戳


async def poke_matcher_handler(bot: Bot, matcher: Matcher, event: PokeNotifyEvent):
    await asyncio.sleep(random.uniform(*config.leaf_poke_action_delay))

    if check_percentage(config.leaf_poke_rand):
        await matcher.finish(
            choice_reply(
                LOADED_POKE_REPLY,
                event.get_user_id(),
                format_sender_username(
                    await get_username_by_id(bot, event.user_id, event.group_id),
                ),
            ),
        )

    await matcher.finish(MessageSegment("poke", {"qq": event.user_id}))


poke_matcher = on_notice(rule=to_me(), priority=10, block=False)
if config.leaf_poke_rand >= 0:
    poke_matcher.handle()(poke_matcher_handler)


# endregion


# region 打断/复读姬

msg_last: Dict[int, Message] = {}  # 存储群内最后一条消息
msg_times: Dict[int, int] = {}  # 存储群内最后一条消息被复读的次数
repeater_times: Dict[int, int] = {}  # 存储随机生成的复读上限


async def repeat_rule(event: GroupMessageEvent) -> bool:
    group_id = event.group_id

    # 复读
    if msg_last.get(group_id) == event.message:
        if group_id not in msg_times:
            return False

        msg_times[group_id] += 1
        if group_id not in repeater_times:
            repeater_times[group_id] = random.randint(*config.leaf_repeater_limit)

        if msg_times[group_id] >= repeater_times[group_id]:
            del msg_times[group_id]  # del 掉防止继续复读
            del repeater_times[group_id]
            return True

        return False

    # 不同消息，未复读
    msg_last[group_id] = event.message
    msg_times[group_id] = 1
    return False


async def repeater_matcher_handler(matcher: Matcher, event: GroupMessageEvent):
    if check_percentage(config.leaf_interrupt):
        await matcher.finish(
            choice_reply(
                LOADED_INTERRUPT_MSG,
                event.get_user_id(),
                format_username_from_event(event),
            ),
        )
    await matcher.finish(transform_message(event.message))


repeater = on_message(rule=repeat_rule, permission=GROUP, priority=99, block=False)
if config.leaf_interrupt >= 0:
    repeater.handle()(repeater_matcher_handler)

# endregion
