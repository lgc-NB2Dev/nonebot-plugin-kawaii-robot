from typing import Literal, Set, Tuple

from nonebot import get_driver
from pydantic import BaseModel, Extra, validator

ReplyPermType = Literal["ALL", "GROUP"]


class ConfigModel(BaseModel, extra=Extra.ignore):
    nickname: Set[str]

    leaf_permission: ReplyPermType = "ALL"
    """词库回复权限，`ALL` 就是全部聊天都会触发回复，`GROUP` 就是仅群聊"""

    leaf_ignore: Set[str] = set()
    """忽略词，指令以本 Set 中的元素开头不会触发词库回复"""

    leaf_reply_type: Literal[-1, 0, 1] = 1
    """回复模式，`-1` 关闭全部 at 回复，`0` 仅启用词库回复，`1` 开启所有回复"""

    leaf_poke_rand: int = 20
    """戳一戳回复文字概率，范围 `0` ~ `100`，`-1` 关闭戳一戳回复"""

    leaf_repeater_limit: Tuple[int, int] = (2, 6)
    """触发复读或打断次数，群内复读 `{0}` ~ `{1}` 次数后触发复读或打断"""

    leaf_interrupt: int = 20
    """打断复读概率，范围 `0` ~ `100`"""

    leaf_match_pattern: Literal[0, 1] = 1
    """词库回复匹配模式，`0` 是精确匹配，`1` 是关键词匹配"""

    leaf_at_mode: bool = True
    """词库回复是否需要 `to_me`"""

    leaf_trigger_percent: int = 5
    """词库回复非 `to_me` 时的触发概率，范围 `0` ~ `100`"""

    leaf_load_builtin_dict: bool = True
    """是否载入内置回复词库"""

    leaf_load_builtin_special: bool = True
    """是否载入内置特殊回复词库"""

    @validator("leaf_repeater_limit")
    def check_repeater_limit(cls, v):  # noqa: N805
        min_c, max_c = v
        if min_c < 2 or min_c > max_c:
            raise ValueError("复读次数范围不正确")
        return v


config: ConfigModel = ConfigModel.parse_obj(get_driver().config.dict())
