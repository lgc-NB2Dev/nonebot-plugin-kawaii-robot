from nonebot.plugin.on import on_message,on_notice
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    GROUP,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
    PokeNotifyEvent,
)

import nonebot
import asyncio
import re
import random

from .utils import (
    MyThesaurus,
    LeafThesaurus,
    AnimeThesaurus,
    get_chat_result,
    hello__bot,
    hello__reply,
    poke__reply,
    unknow_reply,
    interrupt_msg,
    messagePreprocess
    )

from .config import Config

# 加载全局配置
global_config = nonebot.get_driver().config
leaf = Config.parse_obj(global_config.dict())

reply_type = leaf.leaf_reply_type
poke_rand = leaf.leaf_poke_rand

repeater_limit = leaf.leaf_repeater_limit
interrupt = leaf.leaf_interrupt

ignore = leaf.leaf_ignore

# 配置合法检测

if repeater_limit[0] < 2 or repeater_limit[0] > repeater_limit[1]:
    raise Exception('config error: repeater_limit')

# 权限判断

if leaf.leaf_permission == "GROUP":
    permission = GROUP
else:
    permission = None

# 优先级99，条件：艾特bot就触发

if reply_type > -1:
    talk = on_message(rule = to_me(), permission = permission, priority=99, block=False)

    @talk.handle()
    async def _(event: MessageEvent):
        # 获取消息文本
        msg = str(event.get_message())
        # 去掉带中括号的内容(去除cq码)
        msg = re.sub(r"\[.*?\]", "", msg)

        # 如果是光艾特bot(没消息返回)，就回复以下内容
        if (not msg) or msg.isspace():
            await talk.finish(Message(random.choice(hello__reply)))

        # 如果是打招呼的话，就回复以下内容
        if  msg in hello__bot:
            await talk.finish(Message(random.choice(hello__reply)))

        # 如果是已配置的忽略项，直接结束事件
        for i in range(len(ignore)):
            if msg.startswith(ignore[i]):
                await talk.finish()

        # 获取用户nickname
        if isinstance(event, GroupMessageEvent):
            nickname = event.sender.card or event.sender.nickname
        else:
            nickname = event.sender.nickname

        if len(nickname) > 10:
            nickname = nickname[:2] + random.choice(["酱","亲","ちゃん","同志","老师"])

        # 从个人字典里获取结果
        if result := get_chat_result(MyThesaurus, msg):
            await talk.finish(Message(result))

        result = get_chat_result(MyThesaurus, msg)
        if result:
            await talk.finish(Message(result))


        # 从 LeafThesaurus 里获取结果
        if result := get_chat_result(LeafThesaurus,msg):
            await talk.finish(Message(result.replace("name", nickname)))

        # 从 AnimeThesaurus 里获取结果
        if result := get_chat_result(AnimeThesaurus,msg):
            await talk.finish(Message(result.replace("你", nickname)))

        # 不明白的内容
        if reply_type == 1:
            await talk.finish(Message(random.choice(unknow_reply)))

# 优先级10，不会向下阻断，条件：戳一戳bot触发

if poke_rand > -1:
    poke_ = on_notice(rule = to_me(), priority=10, block=False)
    @poke_.handle()
    async def _poke_event(event: PokeNotifyEvent):
        if event.is_tome:
            if poke_rand == 0:
                await asyncio.sleep(1.0)
                await poke_.finish(Message(f'[CQ:poke,qq={event.user_id}]'))
            else:
                if random.randint(1,100) <= poke_rand:
                    await asyncio.sleep(1.0)
                    await poke_.finish(Message(random.choice(poke__reply)))
                else:
                    await asyncio.sleep(1.0)
                    await poke_.finish(Message(f'[CQ:poke,qq={event.user_id}]'))

# 打断/复读姬

if interrupt > -1:
    global msg_last,msg_times,repeater_times
    msg_last = {}
    msg_times = {}
    repeater_times = {}

    async def repeat(event: GroupMessageEvent) -> bool:
        global msg_last, msg_times,repeater_times
        group_id = event.group_id
        msg = messagePreprocess(event.message)
        if msg_last.get(group_id) == msg:
            repeater_times.setdefault(group_id,random.randint(repeater_limit[0], repeater_limit[1]))
            msg_times[group_id] += 1
            if msg_times[group_id] == repeater_times[group_id]:
                repeater_times[group_id] = random.randint(repeater_limit[0], repeater_limit[1])
                msg_times[group_id] += repeater_limit[1]
                return True
            else:
                return False
        else:
            msg_last[group_id] = msg
            msg_times[group_id] = 1
            return False

    repeater = on_message(rule=repeat, permission=GROUP, priority=99, block=False)

    @repeater.handle()
    async def _(event: GroupMessageEvent):
        if random.randint(1,100) <= interrupt:
            await repeater.finish(random.choice(interrupt_msg))
        else:
            await repeater.finish(event.message)
