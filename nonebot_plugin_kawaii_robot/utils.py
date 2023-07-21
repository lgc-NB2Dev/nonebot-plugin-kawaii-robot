from typing import List, Optional

from .const import NICKNAME, ReplyDictType


def full_match_search(resource: ReplyDictType, text: str) -> Optional[List[str]]:
    """
    从 resource 中获取回应：精确查找
    """
    return resource.get(text, None)


def keyword_search(resource: ReplyDictType, text: str) -> Optional[List[str]]:
    """
    从 resource 中获取回应：关键词查找
    """
    if len(text) > 20:
        return None
    return next(
        (resource[key] for key in resource if key in text),
        None,
    )


def format_vars(string: str, user_id: str, username: str, **kwargs) -> str:
    return string.format(
        user_id=user_id,
        username=username,
        bot_nickname=NICKNAME,
        **kwargs,
    )
