from typing import Tuple
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    leaf_permission: str = "ALL"                        # 配置回复权限，"ALL"就是全部聊天都会触发回复，"GROUP"就是仅群聊。
    leaf_ignore = tuple()                               # 配置忽略词，元素为str。
    leaf_reply_type: int = 1                            # 配置回复模式
    leaf_poke_rand: int = 20                            # 配置戳一戳回复文字概率
    leaf_repeater_limit: Tuple[int, int] = (2, 6)       # 配置触发复读次数
    leaf_interrupt: int = 20                            # 配置打断概率
    leaf_match_pattern: int = 1                         # 配置匹配模式,0是精确匹配,1是关键词匹配
    leaf_at_mod: int = 0                                # 配置是否需要to_me,0是需要,1是不需要