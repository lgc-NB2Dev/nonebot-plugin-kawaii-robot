from typing import Literal, Set, Tuple

from nonebot import get_driver
from pydantic import BaseModel, Extra, validator

ReplyPermType = Literal["ALL", "GROUP"]


class ConfigModel(BaseModel, extra=Extra.ignore):
    nickname: Set[str]
    superusers: Set[str]

    leaf_permission: ReplyPermType = "ALL"
    """回复权限，`ALL` 就是全部聊天都会触发回复，`GROUP` 就是仅群聊。"""

    leaf_ignore: Set[str] = set()
    """忽略词，指令以本 Set 中的元素开头不会触发回复"""

    leaf_reply_type: Literal[-1, 0, 1] = 1
    """回复模式，`-1` 关闭全部 at 回复，`0` 仅启用字典，`1` 开启所有回复"""

    leaf_poke_rand: int = 20
    """戳一戳回复文字概率，范围 `0` ~ `100`，`-1` 关闭戳一戳回复"""

    leaf_repeater_limit: Tuple[int, int] = (2, 6)
    """触发复读次数，群内复读 `{0}` ~ `{1}` 次数后触发复读或打断"""

    leaf_interrupt: int = 20
    """打断概率，范围 `0` ~ `100`"""

    leaf_match_pattern: Literal[0, 1] = 1
    """匹配模式，`0` 是精确匹配，`1` 是关键词匹配"""

    leaf_at_mode: Literal[0, 1] = 0
    """是否需要 `to_me`，`0` 是需要，`1` 是不需要"""

    leaf_trigger_percent: int = 100
    """非 `to_me` 时的触发概率，范围 `0` ~ `100`"""

    leaf_load_builtins: bool = True
    """是否载入内置词库"""

    @validator("leaf_repeater_limit")
    def check_repeater_limit(cls, v):  # noqa: N805
        min_c, max_c = v
        if min_c < 2 or min_c > max_c:
            raise ValueError("复读次数范围不正确")
        return v


config: ConfigModel = ConfigModel.parse_obj(get_driver().config.dict())
