<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
</p>

# Nonebot-Plugin-Kawaii-Robot

_✨ 使用[Kyomotoi / AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)的 nonebot2 的回复（文 i）插件 ✨_

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<!-- <a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4778875-45a4-4688-8e1b-b8c844440abb">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4778875-45a4-4688-8e1b-b8c844440abb.svg" alt="wakatime">
</a> -->

<br />

<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/KarisAya/nonebot_plugin_kawaii_robot.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_kawaii_robot">
  <img src="https://img.shields.io/pypi/v/nonebot_plugin_kawaii_robot.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_kawaii_robot">
  <img src="https://img.shields.io/pypi/dm/nonebot_plugin_kawaii_robot" alt="pypi download">
</a>

</div>

## 📖 介绍

### 个性化词库

把你自己的词库（json 文件）扔到 resource 文件夹里就可以加载啦！

可以加载多个 json 文件。

如果扔进了奇怪的东西大概会加载失败，然后。。。跳过，继续加载下一个文件。

~~不要把奇怪的东西扔进资源里呀 kora~~

顺便一提，自己的词库是最优先的。

**注意：词库要符合 json 格式 如果报解码错误先检查自己的词库是不是 无 BOM 的 UTF-8 编码格式**

### 群聊复读姬

现在可以复读啦！~~谁不喜欢 +1 呢~~

当然也可以打断复读...~~谁不喜欢打断复读呢~~

具体详见配置条目

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

在 nonebot2 项目的 `.env` 文件中按需添加下面的配置项

```properties
# 机器人昵称
NICKNAME=[]

# 回复权限，`ALL` 就是全部聊天都会触发回复，`GROUP` 就是仅群聊
LEAF_PERMISSION=ALL

# 忽略词，指令以本列表中的元素开头不会触发回复
LEAF_IGNORE=[]

# 回复模式，`-1` 关闭全部 at 回复，`0` 仅启用字典，`1` 开启所有回复
LEAF_REPLY_TYPE=1

# 戳一戳回复文字概率，范围 `0` ~ `100`，`0` 代表始终戳回去，`-1` 关闭戳一戳回复
LEAF_POKE_RAND=20

# 触发复读次数，群内复读 `{0}` ~ `{1}` 次数后触发复读或打断
LEAF_REPEATER_LIMIT=[2,6]

# 打断概率，范围 `0` ~ `100`，`0` 关闭打断
LEAF_INTERRUPT=20

# 词库回复匹配模式，`0` 是精确匹配，`1` 是关键词匹配
LEAF_MATCH_PATTERN=1

# 是否需要 @机器人 或包含机器人昵称，`0` 是需要，`1` 是不需要
LEAF_AT_MODE=0
```

### 词库

## 🎉 使用

### 指令表

|  指令  | 权限 | 需要@ | 范围 |   说明   |
| :----: | :--: | :---: | :--: | :------: |
| 指令 1 | 主人 |  否   | 私聊 | 指令说明 |
| 指令 2 | 群员 |  是   | 群聊 | 指令说明 |

### 效果图

如果有效果图的话

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

如果有要鸣谢的人的话

## 💰 赞助

感谢大家的赞助！你们的赞助将是我继续创作的动力！

- [爱发电](https://afdian.net/@lgc2333)
- <details>
    <summary>赞助二维码（点击展开）</summary>

  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)

  </details>

## 📝 更新日志

芝士刚刚发布的插件，还没有更新日志的说 qwq~
