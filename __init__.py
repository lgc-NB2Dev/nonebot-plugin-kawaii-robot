from nonebot.plugin.on import on_message,on_notice
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
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

# 为上面不做阻断的at触发提供全局配置开关
global_config = nonebot.get_driver().config
leaf = Config.parse_obj(global_config.dict())

# 优先级99, 条件: 艾特bot就触发
ai = on_message(rule=to_me(), priority=99, block=False)
# 优先级10, 不会向下阻断, 条件: 戳一戳bot触发
poke_ = on_notice(rule=to_me(), priority=10, block=False)


@ai.handle()
async def _(event: MessageEvent):
    # 获取消息文本
    msg = str(event.get_message())
    # 去掉带中括号的内容(去除cq码)
    msg = re.sub(r"\[.*?\]", "", msg)

    
    # 如果是光艾特bot(没消息返回)，就回复以下内容
    if (not msg) or msg.isspace():
        if leaf.leaf_reply_type == 0:
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
    await ai.finish(Message(random.choice(cant__reply)))

@poke_.handle()
async def _poke_event(event: PokeNotifyEvent):
    if event.is_tome:
        if random.randint(1,leaf.leaf_poke_rand) == 1:
            await poke_.finish(Message(random.choice(poke__reply)))
        else:
            poke_msg = f'[CQ:poke,qq={event.user_id}]'
            await asyncio.sleep(1.0)
            await poke_.finish(Message(poke_msg))