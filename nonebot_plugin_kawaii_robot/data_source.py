from pathlib import Path
from typing import List, Tuple

import anyio
from nonebot.log import logger

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

BUILTIN_REPLY_PATH = Path(__file__) / "resource"
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


def sorted_my_dict(my_dict: dict) -> dict:
    """
    排序词库
    """
    return dict(sorted(my_dict.items(), key=lambda item: len(item[0]), reverse=True))


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
            data = json.loads(await file.read_text(encoding="u8"))
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
        logger.opt(colors=True).success(f"特殊回复列表 <y>{json_path.name}</y> 加载成功~")
    except Exception:
        logger.exception(f"特殊回复列表 <y>{json_path.name}</y> 加载失败")
        return False
    return True


async def reload_replies():
    """
    重新载入词库
    """

    LOADED_REPLY_DICT.clear()
    LOADED_HELLO_REPLY.clear()
    LOADED_POKE_REPLY.clear()
    LOADED_UNKNOWN_REPLY.clear()
    LOADED_INTERRUPT_MSG.clear()

    if config.leaf_load_builtins:
        logger.info("正在载入内置词库...")
        await load_reply_json(BUILTIN_REPLY_PATH)
        LOADED_HELLO_REPLY.extend(BUILTIN_HELLO_REPLY)
        LOADED_POKE_REPLY.extend(BUILTIN_POKE_REPLY)
        LOADED_UNKNOWN_REPLY.extend(BUILTIN_UNKNOWN_REPLY)
        LOADED_INTERRUPT_MSG.extend(BUILTIN_INTERRUPT_MSG)

    logger.info("正在载入自定义词库...")
    await load_reply_json(ADDITIONAL_REPLY_PATH)
    await async_load_list_json(LOADED_HELLO_REPLY, ADDITIONAL_HELLO_REPLY_PATH)
    await async_load_list_json(LOADED_POKE_REPLY, ADDITIONAL_POKE_REPLY_PATH)
    await async_load_list_json(LOADED_UNKNOWN_REPLY, ADDITIONAL_UNKNOWN_REPLY_PATH)
    await async_load_list_json(LOADED_INTERRUPT_MSG, ADDITIONAL_INTERRUPT_MSG_PATH)

    logger.info("已载入所有词库~")