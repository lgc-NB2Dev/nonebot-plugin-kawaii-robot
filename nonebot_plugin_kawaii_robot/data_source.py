import asyncio
from pathlib import Path
from typing import List, Tuple

import anyio
from nonebot import get_driver
from nonebot.log import logger

from .utils import flatten_list, full_to_half

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .config import config
from .const import (
    BUILTIN_HELLO_REPLY,
    BUILTIN_INTERRUPT_MSG,
    BUILTIN_POKE_REPLY,
    BUILTIN_UNKNOWN_REPLY,
    ReplyDictType,
)

BUILTIN_REPLY_PATH = Path(__file__).parent / "resource"
ADDITIONAL_REPLY_PATH = Path.cwd() / "data" / "kawaii_robot"
ADDITIONAL_HELLO_REPLY_PATH = ADDITIONAL_REPLY_PATH / "_hello.json"
ADDITIONAL_POKE_REPLY_PATH = ADDITIONAL_REPLY_PATH / "_poke.json"
ADDITIONAL_UNKNOWN_REPLY_PATH = ADDITIONAL_REPLY_PATH / "_unknown.json"
ADDITIONAL_INTERRUPT_MSG_PATH = ADDITIONAL_REPLY_PATH / "_interrupt.json"

if not ADDITIONAL_REPLY_PATH.exists():
    ADDITIONAL_REPLY_PATH.mkdir(parents=True)
for _path in (
    ADDITIONAL_HELLO_REPLY_PATH,
    ADDITIONAL_POKE_REPLY_PATH,
    ADDITIONAL_UNKNOWN_REPLY_PATH,
    ADDITIONAL_INTERRUPT_MSG_PATH,
):
    if not _path.exists():
        _path.write_text("[]", encoding="u8")

LOADED_REPLY_DICT: ReplyDictType = {}
LOADED_HELLO_REPLY: List[str] = []
LOADED_POKE_REPLY: List[str] = []
LOADED_UNKNOWN_REPLY: List[str] = []
LOADED_INTERRUPT_MSG: List[str] = []


def sort_my_dict(my_dict: ReplyDictType):
    """
    按触发词长度倒序排序词库
    """
    sorted_dict = dict(
        sorted(my_dict.items(), key=lambda item: len(item[0]), reverse=True),
    )
    my_dict.clear()
    my_dict.update(sorted_dict)


def merge_reply_dict(target: ReplyDictType, source: ReplyDictType):
    """
    合并词库
    """
    for key in source:
        if key in target:
            target_list = target[key]
            target_list += [x for x in source[key] if x not in target_list]
        else:
            target.update({key: source[key]})


async def load_reply_json(load_path: Path) -> Tuple[int, int]:
    """
    载入词库
    """
    path = anyio.Path(load_path)
    success_count = 0
    fail_count = 0

    async for file in path.glob("*.json"):
        filename = file.name
        if filename.startswith("_"):
            continue

        try:
            loaded = json.loads(await file.read_text(encoding="u8"))
            assert isinstance(loaded, dict)

            data = {full_to_half(k.lower()): v for k, v in loaded.items()}
            merge_reply_dict(LOADED_REPLY_DICT, data)

            success_count += 1
            logger.opt(colors=True).success(f"回复词库 <y>{filename}</y> 加载成功~")

        except Exception:
            fail_count += 1
            logger.exception(f"回复词库 <y>{filename}</y> 加载失败")

    return success_count, fail_count


async def async_load_list_json(
    merge_target: List[str],
    json_path: Path,
) -> bool:
    """
    载入特殊回复列表
    """
    path = anyio.Path(json_path)
    try:
        data = json.loads(await path.read_text(encoding="u8"))
        merge_target.extend(x for x in data if x not in merge_target)
        logger.opt(colors=True).success(
            f"特殊回复词库 <y>{json_path.name}</y> 加载成功~",
        )
    except Exception:
        logger.exception(f"特殊回复词库 <y>{json_path.name}</y> 加载失败")
        return False
    return True


def clear_replies():
    LOADED_REPLY_DICT.clear()
    LOADED_HELLO_REPLY.clear()
    LOADED_POKE_REPLY.clear()
    LOADED_UNKNOWN_REPLY.clear()


async def reload_replies():
    """
    重新载入词库
    """

    clear_replies()

    logger.info("正在载入自定义词库...")
    await asyncio.gather(
        load_reply_json(ADDITIONAL_REPLY_PATH),
        async_load_list_json(LOADED_HELLO_REPLY, ADDITIONAL_HELLO_REPLY_PATH),
        async_load_list_json(LOADED_POKE_REPLY, ADDITIONAL_POKE_REPLY_PATH),
        async_load_list_json(LOADED_UNKNOWN_REPLY, ADDITIONAL_UNKNOWN_REPLY_PATH),
        async_load_list_json(LOADED_INTERRUPT_MSG, ADDITIONAL_INTERRUPT_MSG_PATH),
    )

    if config.leaf_load_builtin_dict:
        logger.info("正在载入内置回复词库...")
        await load_reply_json(BUILTIN_REPLY_PATH)

    if config.leaf_load_builtin_special:
        logger.info("正在载入内置特殊回复词库...")
        LOADED_HELLO_REPLY.extend(BUILTIN_HELLO_REPLY)
        LOADED_POKE_REPLY.extend(BUILTIN_POKE_REPLY)
        LOADED_UNKNOWN_REPLY.extend(BUILTIN_UNKNOWN_REPLY)
        LOADED_INTERRUPT_MSG.extend(BUILTIN_INTERRUPT_MSG)

    sort_my_dict(LOADED_REPLY_DICT)
    logger.success("已载入所有词库~")

    total_reply_key = len(LOADED_REPLY_DICT)
    total_reply_value = len(flatten_list(LOADED_REPLY_DICT.values()))
    total_special_reply = (
        len(LOADED_HELLO_REPLY)
        + len(LOADED_POKE_REPLY)
        + len(LOADED_UNKNOWN_REPLY)
        + len(LOADED_INTERRUPT_MSG)
    )
    logger.opt(colors=True).info(
        f"共计载入 <y>{total_reply_key}</y> 个触发词，及 <y>{total_reply_value}</y> 条对应回复；"
        f"共计载入 <y>{total_special_reply}</y> 条特殊回复",
    )


driver = get_driver()
driver.on_startup(reload_replies)
