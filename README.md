<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>
<div align="center">

# nonebot_plugin_kawaii_robot

使用[Kyomotoi / AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)的nonebot2的回复（文i）插件


</div>

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
    LEAF_REPLY_TYPE = 0 #配置仅at回复，如果是0则正常回复，1则关闭回复
    LEAF_POKE_RAND = 5  #配置戳一戳回复文字概率，例如 1就是每次戳一戳都回复文字，5就是1/5概率回复文字，4/5概率戳回去。
    LEAF_PERMISSION = "ALL" #配置回复权限，"ALL"就是全部聊天都会触发回复，"GROUP"就是仅群聊。

## 其他
~~抄~~改编自[nonebot_plugin_smart_reply](https://github.com/Special-Week/nonebot_plugin_smart_reply)：使用了青云客api的的智能~障~回复插件

~~所以是因为青云客私货太多于是咱删了api重新发了一个qwq~~

源里的leaf.json是咱自制的bot的词库   ~~WARMING：高二次元浓度警告~~
