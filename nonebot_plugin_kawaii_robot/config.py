from typing import Any, Iterable, Literal, Set, Tuple

from cookit.pyd import field_validator
from nonebot import get_plugin_config
from pydantic import BaseModel, Field, validator

ReplyPermType = Literal["ALL", "GROUP"]


class ConfigModel(BaseModel):
    nickname: Set[str]

    is_lagrange: bool = False

    leaf_permission: ReplyPermType = "ALL"
    """词库回复权限，`ALL` 就是全部聊天都会触发回复，`GROUP` 就是仅群聊"""

    leaf_ignore: Set[str] = set()
    """忽略词，指令以本 Set 中的元素开头不会触发词库回复"""

    leaf_reply_type: Literal[-1, 0, 1] = 1
    """回复模式，`-1` 关闭全部 at 回复，`0` 仅启用词库回复，`1` 开启所有回复"""

    leaf_poke_rand: int = Field(20, ge=0, le=100)
    """戳一戳回复文字概率，范围 `0` ~ `100`，`-1` 关闭戳一戳回复"""

    leaf_force_different_user: bool = True
    """复读、打断复读时是否按复读的用户数计算次数"""

    leaf_repeater_limit: Tuple[int, int] = (2, 6)
    """触发复读或打断次数，群内复读 `{0}` ~ `{1}` 次数后触发复读或打断"""

    leaf_repeat_continue: bool = False
    """复读后，群友继续复读达到指定次数时是否继续参与复读或打断"""

    leaf_interrupt: int = Field(20, ge=0, le=100)
    """打断复读概率，范围 `0` ~ `100`"""

    leaf_interrupt_continue: bool = True
    """打断复读后，群友继续复读达到指定次数时是否继续参与复读或打断"""

    leaf_match_pattern: Literal[0, 1, 2] = 1
    """
    词库回复匹配模式，
    `0` 是整句话精确匹配关键词（不推荐）；
    `1` 是按从长到短的顺序遍历词库中的关键词，遇到匹配的就停止遍历并选取对应回复；
    `2` 与 `1` 的遍历方式相同，但是会遍历所有词库中的关键词，然后从匹配到的所有项目中随机选取一个回复
    """

    leaf_search_max: int = 20
    """当 `LEAF_MATCH_PATTERN` >= 1 时，消息长度大于此数值则不从词库中匹配回复，设为 `0` 则禁用此功能"""

    leaf_need_at: bool = True
    """词库回复是否需要 `to_me`"""

    leaf_trigger_percent: int = Field(5, ge=0, le=100)
    """词库回复非 `to_me` 时的触发概率，范围 `0` ~ `100`"""

    leaf_poke_action_delay: Tuple[float, float] = (0.5, 1.5)
    """戳一戳回复延时，单位秒"""

    leaf_multi_reply_delay: Tuple[float, float] = (1.0, 3.0)
    """当回复存在多条消息时，发送消息的间隔时间，单位秒"""

    leaf_load_builtin_dict: bool = True
    """是否载入内置回复词库"""

    leaf_load_builtin_special: bool = True
    """是否载入内置特殊回复词库"""

    @field_validator(
        "leaf_repeater_limit",
        "leaf_poke_action_delay",
        "leaf_multi_reply_delay",
        mode="before",
    )
    def check_interval(cls, v: Any):  # noqa: N805
        if isinstance(v, (int, float)):
            v = (v, v)
        else:
            if not isinstance(v, Iterable):
                raise TypeError("区间必须是 int, float 或 Iterable")
            v = tuple(v)
            if len(v) != 2:
                raise ValueError("区间长度必须为 2")
            if v[0] > v[1]:
                raise ValueError("区间左边界必须小于或等于右边界")
        return v

    @validator("leaf_repeater_limit")
    def check_repeater_limit(cls, v: Tuple[int, int]):  # noqa: N805
        if v[0] < 2:
            raise ValueError("触发复读或打断次数左边界必须大于 2")
        return v


config = get_plugin_config(ConfigModel)
