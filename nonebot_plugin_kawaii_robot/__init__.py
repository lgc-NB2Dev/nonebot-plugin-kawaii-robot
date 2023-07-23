from nonebot.plugin import PluginMetadata

from . import __main__ as __main__
from .config import ConfigModel

__version__ = "4.0.0"
__plugin_meta__ = PluginMetadata(
    name="KawaiiRobot",
    description="使用 Kyomotoi/AnimeThesaurus 的 NoneBot2 的回复（文i）插件",
    usage="Ciallo～(∠・ω< )⌒★",
    type="application",
    homepage="https://github.com/KarisAya/nonebot_plugin_kawaii_robot/",
    config=ConfigModel,
    supported_adapters={"~onebot.v11"},
    extra={},
)
