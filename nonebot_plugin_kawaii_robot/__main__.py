import asyncio
import random
from typing import Dict

from nonebot.adapters import Bot as BaseBot, Event as BaseEvent
from nonebot.permission import Permission
from nonebot.plugin.on import on_message, on_notice
from nonebot.rule import Rule, to_me
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot_plugin_session import (
    SessionId,
    SessionIdType,
    SessionLevel,
    extract_session,
)

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
    choice_reply_from_ev,
    finish_multi_msg,
    search_reply_dict,
)


async def group_perm(bot: BaseBot, event: BaseEvent) -> bool:
    ss = extract_session(bot, event)
    return ss.level >= SessionLevel.LEVEL2


GROUP = Permission(group_perm)

# region 词库回复


async def ignore_rule(event: BaseEvent) -> bool:
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
        (not config.leaf_need_at) and check_percentage(config.leaf_trigger_percent)
    ):
        return True

    return False


async def talk_matcher_handler(event: BaseEvent):
    msg = event.get_plaintext().strip()

    # 如果是光艾特 bot (没消息返回)，就回复以下内容
    if (not msg) and event.is_tome():
        await finish_multi_msg(await choice_reply_from_ev(LOADED_HELLO_REPLY))

    # 从词库中获取回复
    if reply_list := search_reply_dict(LOADED_REPLY_DICT, msg):
        await finish_multi_msg(await choice_reply_from_ev(reply_list))

    # 不明白的内容，开启所有回复并 @bot 才会回复
    if event.is_tome() and config.leaf_reply_type == 1:
        await finish_multi_msg(await choice_reply_from_ev(LOADED_UNKNOWN_REPLY))


if config.leaf_reply_type >= 0:
    DICT_REPLY_PERM = GROUP if config.leaf_permission == "GROUP" else None
    talk = on_message(
        rule=Rule(ignore_rule) & (to_me() if config.leaf_need_at else None),
        permission=DICT_REPLY_PERM,
        priority=99,
        block=False,
    )
    talk.handle()(talk_matcher_handler)


# endregion


# region 戳一戳

try:
    from nonebot.adapters.onebot.v11 import (
        Bot as OBV11Bot,
        MessageSegment as OBV11Seg,
        PokeNotifyEvent,
    )
except ImportError:
    pass
else:

    async def send_poke(bot: OBV11Bot, event: PokeNotifyEvent):
        if config.is_lagrange:
            if event.group_id:
                await bot.group_poke(group_id=event.group_id, user_id=event.user_id)
            else:
                await bot.friend_poke(user_id=event.user_id)
        else:
            await bot.send(event, OBV11Seg("poke", {"qq": event.user_id}))

    async def poke_matcher_handler(bot: OBV11Bot, event: PokeNotifyEvent):
        await asyncio.sleep(random.uniform(*config.leaf_poke_action_delay))

        if check_percentage(config.leaf_poke_rand):
            await finish_multi_msg(
                await choice_reply_from_ev(LOADED_POKE_REPLY),
            )

        await send_poke(bot, event)

    if config.leaf_poke_rand >= 0:
        poke_matcher = on_notice(rule=to_me(), priority=10, block=False)
        poke_matcher.handle()(poke_matcher_handler)


# endregion


# region 打断/复读姬

msg_last: Dict[str, str] = {}  # 存储群内最后一条消息
msg_times: Dict[str, int] = {}  # 存储群内最后一条消息被复读的次数
repeater_times: Dict[str, int] = {}  # 存储随机生成的复读上限


async def repeat_rule(
    bot: BaseBot,
    event: BaseEvent,
    group_id: str = SessionId(SessionIdType.GROUP),
) -> bool:
    try:
        event.get_message()
    except ValueError:
        return False
    message = await UniMessage.generate(bot=bot, event=event)
    message_str = repr(message)

    # 复读
    if msg_last.get(group_id) == message_str:
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
    msg_last[group_id] = message_str
    msg_times[group_id] = 1
    return False


async def repeater_matcher_handler(
    bot: BaseBot,
    event: BaseEvent,
    group_id: str = SessionId(SessionIdType.GROUP),
):
    try:
        event.get_message()
    except ValueError:
        return

    if check_percentage(config.leaf_interrupt):
        if config.leaf_interrupt_continue:
            # 让下次复读计入次数统计，以便再次打断或复读
            msg_times[group_id] = 0

        await finish_multi_msg(await choice_reply_from_ev(LOADED_INTERRUPT_MSG))

    await (await UniMessage.generate(bot=bot, event=event)).send()


if config.leaf_interrupt >= 0:
    repeater = on_message(rule=repeat_rule, permission=GROUP, priority=99, block=False)
    repeater.handle()(repeater_matcher_handler)

# endregion
