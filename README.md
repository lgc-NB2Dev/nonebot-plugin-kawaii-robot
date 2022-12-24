<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>
<div align="center">

# nonebot_plugin_kawaii_robot

使用[Kyomotoi / AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)的nonebot2的回复（文i）插件


</div>

本插件更新到3.0版本，配置项较2.x前有改动，建议升级后重新配置。

## 群聊复读姬

现在可以复读啦！~~谁不喜欢+1呢~~

当然也可以打断复读...~~谁不喜欢打断复读呢~~

具体详见配置条目

## 个性化词库

把你自己的词库（json文件）扔到resource文件夹里就可以加载啦！

可以加载多个json文件。

如果扔进了奇怪的东西大概会加载失败，然后。。。跳过，继续加载下一个文件。

~~不要把奇怪的东西扔进资源里呀kora~~

顺便一提，自己的词库是最优先的。

__注意：词库要符合json格式 如果报解码错误先检查自己的词库是不是 无 BOM 的 UTF-8 编码格式__

### 词库格式

参考[Kyomotoi / AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)
json字典格式，键是字符串，值是列表
    
    {
        "key":[
            "value"
            ]
    }

## 安装
    pip install nonebot_plugin_kawaii_robot
## 使用
    nonebot.load_plugin('nonebot_plugin_kawaii_robot') 
## 配置
    # nonebot_plugin_kawaii_robot
    LEAF_PERMISSION = "ALL"     # 配置回复权限，"ALL"就是全部聊天都会触发回复，"GROUP"就是仅群聊。
    LEAF_IGNORE = ()            # 配置忽略词，元素为str。
    LEAF_REPLY_TYPE = 1         # 配置at回复
    LEAF_POKE_RAND = 5          # 配置戳一戳回复文字概率
    LEAF_REPEATER_LIMIT = [3,6] # 配置复读次数
    LEAF_INTERRUPT = 6          # 配置打断概率

****

`LEAF_PERMISSION` __配置回复权限__

`"ALL"` 全部聊天

`"GROUP"` 仅群聊。

****
`LEAF_IGNORE` __配置忽略词__

指令以`LEAF_IGNORE`中的元素开头不会触发回复。

元素为str

    # 例如忽略 .指令 #指令 你好
    LEAF_IGNORE = (".","#","你好")

****

`LEAF_REPLY_TYPE` __配置at回复__

`-1` 关闭全部at回复

`0` 仅启用字典

`1` 开启所有回复

****
  
`LEAF_POKE_RAND` __配置戳一戳回复__

`-1` 关闭戳一戳回复

`0` 戳一戳回复戳一戳

`1` 戳一戳回复文字

`5` 配置戳一戳回复文字概率（5就是1/5概率回复文字，4/5概率戳回去）

****

`LEAF_REPEATER_LIMIT` __配置复读次数__

`[3,6]` 群内复读3~6次数后触发复读或打断

****

`LEAF_INTERRUPT` __配置打断概率__

`-1` 关闭复读/打断

`0` 全部复读

`1` 全部打断

`6` 配置打断概率（6就是1/6概率打断，5/6概率复读）

****

## 其他

改编~~抄~~自[nonebot_plugin_smart_reply](https://github.com/Special-Week/nonebot_plugin_smart_reply)：使用了青云客api的的智能~障~回复插件

复读姬借鉴~~抄~~自[nonebot_plugin_repeater](https://github.com/ninthseason/nonebot-plugin-repeater)：群聊复读机

源里的leaf.json是咱自制的bot的词库

__WARMING：高二次元浓度警告__
