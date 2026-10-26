# Capsule Cast Director

[English](README.md)

一套用于圆润卡通人物设计和短片规划的 agent skill。五种风格共用实心身体、宽厚四肢和胶囊眼，同时各自保留服装、配色与场景。

它交付人物设定、图片提示词、分镜及可独立使用的镜头提示词。实际生成依赖宿主提供的工具；仓库没有绑定图片或视频服务，也没有用旧样片充当新版效果。

## 五种风格、七个分支

| 风格 | 分支 | 保留特色 |
|---|---|---|
| 经典黑白 | 白底 / 黑底 | 黑白人物、平面画布、简洁图形道具 |
| 现代风 | 科技棚 / 电影场景 | 红帽、黄 T 恤、深色短裤；青蓝界面或全彩场景 |
| 史前风 | 单一类别 | 兽皮、深色头发和四肢、土色世界、可选反讽节奏 |
| 治愈风 | 单一类别 | 白色头身、深色四肢、指定日常衣装、温暖生活空间 |
| 历史风 | 单一类别 | 人物肤色、时代服饰、工具和建筑 |

完整规则见[人物与风格指南](skills/directing-capsule-casts/references/looks.md)，可直接阅读[七个完整视觉提示词](examples/visual-prompts.md)。用户指定的服装和颜色优先于默认值。

## 安装和调用

下载仓库后，在项目根目录执行。安装工具需要 Python 3.10 或更新版本，无第三方 Python 依赖：

```sh
python3 tools/install.py
```

默认复制到 `~/.agents/skills/directing-capsule-casts`，包含完整 skill 和许可文本。目标已存在时会停止，避免覆盖。其他客户端目录可用 `--dest /path/to/skills` 指定。[Codex 官方文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)说明了加载位置；如果客户端没有显示新技能，可重新加载或重启。

目标目录需位于技能源目录之外。复制错误或键盘中断会清理本次未完成的安装，便于重试；已有安装会保留。

调用示例：

```text
用 $directing-capsule-casts 做一个 35 秒、9:16 的治愈故事。
全片都在同一家面包店，主角穿绿色围裙，拿着一个米白纸袋。
只要环境和动作声，直接交付最终镜头提示词。
```

支持读取文件的其他 agent 可以直接使用 [SKILL.md](skills/directing-capsule-casts/SKILL.md)。纯文字工作流不需要 Python。只做人物时，不会要求先回答视频时长或配音问题。

## 可检查的镜头包

可选 JSON 格式把共用人物、画法、声音描述存一份，再记录每段的时间和道具状态。渲染工具会将完整描述展开到各段，减少遗漏和缩写。

画幅支持自定义正数比例，包括 `4:5`、`21:9` 和 `2.39:1`。每段可用 `visible_props` 指定画面内道具，画外物品仍保留在连续性记录中。导出时不会对镜头与动作的时间值额外舍入。

```sh
python3 skills/directing-capsule-casts/scripts/package.py check examples/lantern-home.json
python3 skills/directing-capsule-casts/scripts/package.py render examples/lantern-home.json
```

[35 秒灯笼故事](examples/lantern-home.json)包含中文旁白、两个人物、道具交接和手部特写，分段为 12、9、8、6 秒。无需运行 Python 即可阅读[展开后的镜头提示词](examples/lantern-home.md)。这些是剪辑目标，实际生成时需适配所选服务。另有七个十秒示例，覆盖全部风格分支，见 [examples/](examples/)。

检查工具会拒绝时长不符、时间空隙或重叠、未知人物或说话者、声音模式冲突，以及没有说明的道具状态跳变。它不能判断实际画面、接触动作、史实、语速或成片质量。字段详见[格式说明](skills/directing-capsule-casts/references/package-format.md)。

## 验证与协作

```sh
python3 -m unittest discover -s tests -v
```

测试只使用临时目录，不调用媒体服务或网络。GitHub Actions 在推送和拉取请求中运行同一套测试。[验证记录](docs/validation.md)区分本地检查、独立文字试用和未验证的媒体效果。参与修改请看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 开源许可与来源

本项目新写的内容采用 [MIT 许可](LICENSE)，署名为 2026 Capsule Cast Director contributors。代码、说明、示例和项目身份均重新编写；[来源说明](PROVENANCE.md)如实交代此前研究、视觉启发和第三方材料的边界。项目与 xAI 或所引用作者没有官方关联。
