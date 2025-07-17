from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_userinfo")
require("nonebot_plugin_session")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "4.1.3"
__plugin_meta__ = PluginMetadata(
    name="KawaiiRobot",
    description="使用 Kyomotoi/AnimeThesaurus 的 NoneBot2 的回复（文i）插件",
    usage="Ciallo～(∠・ω< )⌒★",
    type="application",
    homepage="https://github.com/KarisAya/nonebot_plugin_kawaii_robot/",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
        "nonebot_plugin_userinfo",
        "nonebot_plugin_session",
    ),
    extra={},
)
