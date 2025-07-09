<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-Kawaii-Robot

_✨ 使用 [Kyomotoi/AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus) 的 NoneBot2 的回复（文 i）插件 ✨_

<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<!-- <a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4778875-45a4-4688-8e1b-b8c844440abb">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4778875-45a4-4688-8e1b-b8c844440abb.svg" alt="wakatime">
</a> -->

<br />

<a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/pyd-v1-or-v2.json" alt="Pydantic Version 1 Or 2" >
</a>
<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/KarisAya/nonebot_plugin_kawaii_robot.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_kawaii_robot">
  <img src="https://img.shields.io/pypi/v/nonebot_plugin_kawaii_robot.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_kawaii_robot">
  <img src="https://img.shields.io/pypi/dm/nonebot_plugin_kawaii_robot" alt="pypi download">
</a>

<br />

<a href="https://registry.nonebot.dev/plugin/nonebot_plugin_kawaii_robot:nonebot_plugin_kawaii_robot">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot_plugin_kawaii_robot" alt="NoneBot Registry">
</a>
<a href="https://registry.nonebot.dev/plugin/nonebot_plugin_kawaii_robot:nonebot_plugin_kawaii_robot">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin-adapters%2Fnonebot_plugin_kawaii_robot" alt="Supported Adapters">
</a>

</div>

## 📖 介绍

**WARNING：高二次元浓度警告**

### 词库回复

当用户 @机器人 或者 提到机器人昵称时，会根据词库回复一条消息

### 戳一戳回复

当用户戳机器人的时候，机器人会戳回去，或者随机回复一条词库中消息

### 群聊（打断）复读姬

现在可以复读啦！~~谁不喜欢 +1 呢~~  
当然也可以打断复读...~~谁不喜欢打断复读呢~~

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot_plugin_kawaii_robot
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot_plugin_kawaii_robot
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot_plugin_kawaii_robot
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot_plugin_kawaii_robot
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot_plugin_kawaii_robot
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_kawaii_robot"
]
```

</details>

## ⚙️ 配置

### 插件

在 NoneBot2 项目的 `.env` 文件中按需添加下面的配置项

```properties
# 机器人昵称
NICKNAME=[]

# 词库回复权限，`ALL` 就是全部聊天都会触发回复，`GROUP` 就是仅群聊
LEAF_PERMISSION=ALL

# 忽略词，指令以本列表中的元素开头不会触发回复
# 例：[".", "#", "你好"]
LEAF_IGNORE=[]

# 回复模式，`-1` 关闭全部 at 回复，`0` 仅启用词库回复，`1` 开启所有回复
LEAF_REPLY_TYPE=1

# 戳一戳回复文字概率，范围 `0` ~ `100`，`-1` 关闭戳一戳回复，`0` 代表始终戳回去
LEAF_POKE_RAND=20

# 复读、打断复读时是否按复读的用户数计算次数
LEAF_FORCE_DIFFERENT_USER=True

# 触发复读或打断次数，群内复读 `{0}` ~ `{1}` 次数后触发复读或打断
LEAF_REPEATER_LIMIT=[2, 6]

# 复读后，群友继续复读达到指定次数时是否继续参与复读或打断
LEAF_REPEAT_CONTINUE=False

# 打断概率，范围 `0` ~ `100`，`0` 关闭打断
LEAF_INTERRUPT=20

# 打断复读后，群友继续复读达到指定次数时是否继续参与复读或打断
LEAF_INTERRUPT_CONTINUE=True

# 词库回复匹配模式，
# `0` 是整句话精确匹配关键词（不推荐）；
# `1` 是按从长到短的顺序遍历词库中的关键词，遇到匹配的就停止遍历并选取对应回复；
# `2` 与 `1` 的遍历方式相同，但是会遍历所有词库中的关键词，然后从匹配到的所有项目中随机选取一个回复
LEAF_MATCH_PATTERN=1

# 当 `LEAF_MATCH_PATTERN` >= 1 时，消息长度大于此数值则不从词库中匹配回复，设为 `0` 则禁用此功能
LEAF_SEARCH_MAX=20

# 词库回复是否需要 @机器人 或包含机器人昵称
LEAF_NEED_AT=True

# 当 `LEAF_NEED_AT` 为 `False` 时，非 @机器人 时的词库回复触发概率，范围 `0` ~ `100`
LEAF_TRIGGER_PERCENT=5

# 戳一戳回复延时，单位秒
LEAF_POKE_ACTION_DELAY=[0.5, 1.5]

# 当回复存在多条消息时，发送消息的间隔时间，单位秒
LEAF_MULTI_REPLY_DELAY=[1.0, 3.0]

# 是否载入内置回复词库
# 内置了 Kyomotoi/AnimeThesaurus 词库（data.json），还有咱自制的 bot 的词库（leaf.json）
LEAF_LOAD_BUILTIN_DICT=True

# 是否载入内置特殊回复词库
LEAF_LOAD_BUILTIN_SPECIAL=True

# 是否注册 重载词库 指令
LEAF_REGISTER_RELOAD_COMMAND=True
```

### 附加词库

#### 加载

把你自己的词库（json 文件）扔到 `data/kawaii_robot` 文件夹里就可以加载啦！  
可以加载多个 json 文件。  
会忽略文件名以 `_` 开头的文件。  
如果扔进了奇怪的东西大概会加载失败，然后。。。跳过，继续加载下一个文件。  
~~不要把奇怪的东西扔进资源里呀 kora~~  
~~顺便一提，自己的词库是最优先的。~~ 现在并到一起了

#### 编写

参考 [Kyomotoi/AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus) 的 json 字典格式，键是关键词字符串，值是回复列表

**注意：词库要符合 json 格式 如果报解码错误（`UnicodeDecodeError`）先检查自己的词库是不是 无 BOM 的 UTF-8 编码格式**

回复里可以写变量，目前用 `UniMessage.template().format()` 格式化；可以往里写 [Alconna 的扩展控制符](https://nonebot.dev/docs/best-practice/alconna/uniseg#%E4%BD%BF%E7%94%A8%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF)。  
如果回复中需要用到 `{` 或 `}`，请用 `{{` 或 `}}` 代替。  
插件内建的一些的变量：

- `{user_id}`：发送者 QQ 号
- `{username}`：发送者昵称（获取失败则默认为 `你`）
- `{bot_nickname}`：机器人昵称（没有设置则默认为 `可爱的咱`）
- `{message_id}`: 消息 ID，在戳一戳回复中为 None
- `{segment}`：用于分割消息，该变量前的文本将会单独为一条消息发送
- `{at}`: At 消息发送者，是 `{:At(user, user_id)}` 的简写
- `{reply}`: 回复发送者的消息，是 `{:Reply(message_id)}` 的简写，在戳一戳回复中为 None

示例：

```jsonc
{
  "呐": [
    "嗯？{bot_nickname}在哦～{username}有什么事吗？",
    "{at} 呐呐呐~",
    "{:Reply(message_id)} 呐？"
    // ...
  ]
}
```

#### 特殊词库

在 `data/kawaii_robot` 文件夹里有几个特殊的附加词库文件（在 `const.py` 中有对应的内置词库）：

- `_hello.json`：用户只 at 了机器人，没有带任何其他文本消息时回复的内容
- `_poke.json`：用户戳一戳机器人时回复的文本内容
- `_unknown.json`：用户发送的消息没有匹配到任何词库内容时回复的消息
- `_interrupt.json`：打断复读时回复的消息

这些词库的格式是一个文本数组，每个元素是一条回复，同样可以使用上面提到的变量

示例：

```jsonc
[
  "{username}你好～",
  "{bot_nickname}在哦～"
  // ...
]
```

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[168603371](https://qm.qq.com/q/EikuZ5sP4G)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

- 插件改编~~抄~~自 [nonebot_plugin_smart_reply](https://github.com/Special-Week/nonebot_plugin_smart_reply)：使用了青云客 api 的的智能~障~回复插件
- 复读姬借鉴~~抄~~自 [nonebot_plugin_repeater](https://github.com/ninthseason/nonebot-plugin-repeater)：群聊复读机

## 💰 赞助

**[赞助我](https://blog.lgc2333.top/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！

## 📝 更新日志

### 4.1.2

- 添加配置项 `LEAF_REGISTER_RELOAD_COMMAND`，注册 `重载词库` 指令用于词库热重载

### 4.1.1

- 修复戳一戳无法正常回复

### 4.1.0

- 适配 Pydantic V1 & V2
- 使用 alconna 支持多平台，词库变量写法变化，新增了几个变量，不再支持 CQ 码
- 重写了复读的逻辑，添加配置项 `LEAF_FORCE_DIFFERENT_USER`、`LEAF_REPEAT_CONTINUE`

### 4.0.0

- 完全重构插件代码，更改项目结构，使用 `pdm` 管理项目
- 词库优化（详见 [附加词库](#附加词库)）：
  - 加载：现在可以直接往 `data/kawaii_robot` 文件夹里扔你自己的 json 词库了
  - 编写：支持了一些变量
- 配置项的增加与修改（详见 [配置](#⚙️-配置)）：<!-- markdownlint-disable -->
  - 修改 `LEAF_IGNORE`：修改类型为 `Set[str]`，配置书写方式不变
  - 修改 `LEAF_MATCH_PATTERN`：新增模式 `2`
  - 修改 `LEAF_AT_MOD`：更名为 `LEAF_NEED_AT`，修改类型为 `bool`
  - 增加 `LEAF_INTERRUPT_CONTINUE`
  - 增加 `LEAF_SEARCH_MAX`
  - 增加 `LEAF_TRIGGER_PERCENT`
  - 增加 `LEAF_POKE_ACTION_DELAY`
  - 增加 `LEAF_LOAD_BUILTIN_DICT`
  - 增加 `LEAF_LOAD_BUILTIN_SPECIAL`
  - 增加 `LEAF_MULTI_REPLY_DELAY`
- 还有的可能没列出来，问就是我忘了，qwq
