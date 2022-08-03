<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>
<div align="center">

# nonebot_plugin_kawaii_robot

使用[Kyomotoi / AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)的nonebot2的回复（文i）插件


</div>

## 安装
    pip install nonebot_plugin_kawaii_robot
## 使用
    nonebot.load_plugin('nonebot_plugin_kawaii_robot') 
## 配置
    # nonebot_plugin_kawaii_robot
    LEAF_REPLY_TYPE = 0 #配置仅at回复，如果是0则正常回复，1则关闭回复
    LEAF_POKE_RAND = 5  #配置戳一戳回复文字概率，例如 1就是每次戳一戳都回复文字，5就是1/5概率回复文字，4/5概率戳回去。

## 其他
~~抄~~改编自[nonebot_plugin_smart_reply](https://github.com/Special-Week/nonebot_plugin_smart_reply)：使用了青云客api的的智能~障~回复插件

~~所以是因为青云客私货太多于是咱删了api重新发了一个qwq~~

源里的leaf.json是咱自制的bot的词库   ~~WARMING：高二次元浓度警告~~
