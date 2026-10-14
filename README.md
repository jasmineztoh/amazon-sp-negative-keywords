# 亚马逊 SP 否词 Skill

为 Amazon Sponsored Products（SP）广告整理否定关键词，交付可审阅的 Excel 否词表。Skill 有两种任务：

- **投前否词**：根据当前 ASIN 商品页确认产品边界，寻找购买意图错配的词，优先提炼安全的词根做词组否定。
- **搜索词报表分析**：先找活动内持续空耗或表现差的完整搜索词，建议精准否定；再评估是否有安全的共同词根可做词组否定。保留广告主判断所需的投放数据。

Skill 的说明和输出要求均为中文。它只生成建议和表格，不会修改亚马逊广告设置；是否添加否词由广告主决定。

## 安装

### 推荐：用 Skills CLI 安装

电脑需有 Node.js 和 npm。在终端运行：

```bash
npx skills add jasmineztoh/amazon-sp-negative-keywords
```

安装器会让你选择 Agent 和安装范围。想让 Skill 在所有项目中可用，可直接使用下面的命令。`-g` 表示全局安装，`-a` 指定 Agent，`-y` 跳过交互确认。

| Agent | 全局安装命令 |
| --- | --- |
| Codex | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a codex -y` |
| Claude Code | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a claude-code -y` |
| Cursor | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a cursor -y` |
| OpenCode | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a opencode -y` |
| Gemini CLI | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a gemini-cli -y` |
| GitHub Copilot | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a github-copilot -y` |

只在当前项目使用时，进入项目目录运行对应命令并去掉 `-g`。`npx` 运行的是 [Vercel Skills CLI](https://github.com/vercel-labs/skills) 安装器，本仓库无需发布 npm 包。

### WorkBuddy

目前 Skills CLI 的[支持列表](https://github.com/vercel-labs/skills#supported-agents)没有 WorkBuddy，因此不要使用 `-a workbuddy`。把仓库放入 WorkBuddy 的用户级 Skills 目录即可。

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.workbuddy\skills" | Out-Null
git clone https://github.com/jasmineztoh/amazon-sp-negative-keywords.git "$HOME\.workbuddy\skills\amazon-sp-negative-keywords"
```

macOS / Linux：

```bash
mkdir -p ~/.workbuddy/skills
git clone https://github.com/jasmineztoh/amazon-sp-negative-keywords.git ~/.workbuddy/skills/amazon-sp-negative-keywords
```

若 WorkBuddy 未立即识别，重新加载 Skills 或重启 WorkBuddy。安装后应能找到 `amazon-sp-negative-keywords/SKILL.md`。

## 怎么使用

**投前否词**：提供 ASIN 和站点。Agent 需要能访问对应站点的亚马逊商品详情页，并能生成 Excel 文件。

```text
使用 amazon-sp-negative-keywords，为美国站 ASIN B0XXXXXXXX 搜集 SP 投放前否词，输出 Excel。
```

**搜索词报表分析**：上传 SP 搜索词报表；如有商品 ASIN、目标利润率等资料，可一并提供。没有的数据不会被编造。

```text
使用 amazon-sp-negative-keywords，分析这份 SP 搜索词报表，给出建议否定的搜索词和匹配方式，并保留判断所需的投放数据，输出 Excel。
```

每次只运行所需的一种任务。投前表聚焦否词、翻译、匹配方式和原因；报表分析表保留曝光、点击、花费、订单、ACOS 等关键数据。

## 更新

通过 Skills CLI 安装的版本：

```bash
npx skills update amazon-sp-negative-keywords
```

WorkBuddy 手动安装的版本：

```bash
git -C ~/.workbuddy/skills/amazon-sp-negative-keywords pull --ff-only
```

Windows PowerShell 可将上面的路径换成 `"$HOME\.workbuddy\skills\amazon-sp-negative-keywords"`。

## 仓库内容

- [SKILL.md](SKILL.md)：任务入口与共同规则
- [references/](references/)：投前否词、报表分析和 Excel 格式规则
- [scripts/check_prelaunch.py](scripts/check_prelaunch.py)：投前表格检查脚本，使用 Python 3 标准库，无需额外安装 Python 包

## 许可

[MIT License](LICENSE)

