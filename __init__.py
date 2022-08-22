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

from .utils import *
from .config import Config

# 加载全局配置
global_config = nonebot.get_driver().config
leaf = Config.parse_obj(global_config.dict())

reply_type = leaf.leaf_reply_type
poke_rand = leaf.leaf_poke_rand

repeater_limit = leaf.leaf_repeater_limit
interrupt = leaf.leaf_interrupt

# 配置合法检测
if repeater_limit[0] < 2 or repeater_limit[0] > repeater_limit[1]:
    raise Exception('config error: repeater_limit')

# 权限判断
if leaf.leaf_permission == "GROUP":
    permission = GROUP
else:
    permission = None

# 优先级99，条件：艾特bot就触发

ai = on_message(rule = to_me(), permission = permission, priority=99, block=False)

@ai.handle()
async def _(event: MessageEvent):
    if reply_type > -1:
        # 获取消息文本
        msg = str(event.get_message())
        # 去掉带中括号的内容(去除cq码)
        msg = re.sub(r"\[.*?\]", "", msg)
        # 如果是光艾特bot(没消息返回)，就回复以下内容
        if (not msg) or msg.isspace():
            if reply_type > 1:
                await ai.finish(Message(random.choice(hello__reply)))
            else:
                await ai.finish()
        # 如果是打招呼的话，就回复以下内容
        if  msg in hello__bot:
            await ai.finish(Message(random.choice(hello__reply)))
        # 获取用户nickname
        if isinstance(event, GroupMessageEvent):
            nickname = event.sender.card or event.sender.nickname
        else:
            nickname = event.sender.nickname

        if len(nickname) > 10:
            nickname = nickname[:2] + random.choice(["酱","亲","ちゃん","同志","老师"])
        # 从个人字典里获取结果（优先）
        result = await get_chat_result_my(msg,  nickname)
        if result != None:
            await ai.finish(Message(result))
        # 从LeafThesaurus里获取结果
        result = await get_chat_result_leaf(msg,  nickname)
        if result != None:
            await ai.finish(Message(result))
        # 从AnimeThesaurus里获取结果
        result = await get_chat_result(msg,  nickname)
        if result != None:
            await ai.finish(Message(result))
        # 随机回复cant__reply的内容
        if reply_type > 0:
            await ai.finish(Message(random.choice(cant__reply)))

# 优先级10，不会向下阻断，条件：戳一戳bot触发

poke_ = on_notice(rule = to_me(), priority=10, block=False)

@poke_.handle()
async def _poke_event(event: PokeNotifyEvent):
    if poke_rand > -1 and event.is_tome:
        if poke_rand == 0:
            await asyncio.sleep(1.0)
            await poke_.finish(Message(f'[CQ:poke,qq={event.user_id}]'))
        else:
            if random.randint(1,poke_rand) == 1:
                await asyncio.sleep(1.0)
                await poke_.finish(Message(random.choice(poke__reply)))
            else:
                await asyncio.sleep(1.0)
                await poke_.finish(Message(f'[CQ:poke,qq={event.user_id}]'))



# 打断/复读姬

msg_last = {}
msg_times = {}
repeater_times = {}

repeater = on_message(permission=GROUP, priority=10, block=False)

interrupt_msg = ["打断！","打断复读！","[CQ:face,id=212]","[CQ:face,id=318][CQ:face,id=318]","[CQ:face,id=181]"]

@repeater.handle()
async def _(event: GroupMessageEvent):
    if interrupt > -1:
        global msg_last, msg_times,repeater_times,repeater_flag
        group_id = event.group_id
        repeater_times.setdefault(group_id,random.randint(repeater_limit[0], repeater_limit[1]) - 1)
        msg = messagePreprocess(event.message)
        if msg_last.get(group_id) != msg:
            msg_last[group_id] = msg
            msg_times[group_id] = 1
        elif msg_times[group_id] == repeater_times[group_id]:
            repeater_times[group_id] = random.randint(repeater_limit[0], repeater_limit[1]) - 1
            msg_times[group_id] += repeater_limit[1]
            if interrupt == 0:
                await repeater.finish(random.choice(interrupt_msg))
            else:
                if random.randint(1,interrupt) == 1:
                    await repeater.finish(random.choice(interrupt_msg))
                else:
                    await repeater.finish(event.message)
        else:
            msg_times[group_id] += 1
