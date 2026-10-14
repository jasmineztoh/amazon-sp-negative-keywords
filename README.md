# 亚马逊 SP 否词 Skill

让广告预算尽量花在**可能购买这件商品**的人身上。

买家搜索吸尘器时，亚马逊可能展示扫地机器人等相邻商品。平台是在提供选择；对明确销售某款商品的广告主，错配点击却可能消耗预算。反过来，否词过宽也会挡住订单。这个 Skill 帮广告主在投放前找出值得否定的购物意图，并在投放后用搜索词报表找出持续空耗的词。目标是**提高利润，而非单纯压低花费**。

它只生成可审阅的 Excel 建议表；是否把词加入广告活动，由广告主决定。

## 两种任务

| 任务 | 什么时候用 | 先看什么 | 通常建议的否定方式 |
| --- | --- | --- | --- |
| **投前搜集否词**（主要任务） | 准备为一个 ASIN 投放 SP 广告 | 当前亚马逊商品页与买家的购买意图 | 安全词根的词组否定 |
| **搜索词报表分析** | 已有 SP 搜索词报表，想找新增否词 | 每个广告活动中完整搜索词的花费与订单 | 先精准否定完整搜索词，再考虑词组否定 |

每次只做用户需要的一种任务。两种任务的判断顺序不同，不能把投前的“词根优先”套到报表分析上。

## 判断流程（SOP）

### 一、投前搜集否词

1. **先认清商品。** 用 ASIN 打开对应站点的亚马逊前台详情页，核实商品形态、功能、适用场景和包装内容。旧活动名称、参考否词表和历史报表只提供线索；与当前页面冲突时，以当前商品页为准。页面未说明的功能先记为未知。
2. **从多个角度找错配意图。** 检查其他完整商品、功能或工作方式、只买配件或耗材、租赁维修等服务、使用场景、品牌型号兼容性，以及站点语言中的同义表达。参考表用于扩展搜索范围，不直接照搬结论。
3. **保护可能成交的需求。** 商品品类大词、主要功能、已成交需求，以及“购买附带配件的整机”不能因为含有配件名称就被否掉。广告主判断某类词仍有过半机会出单，或有合理购买路径但证据不足时，先留待测试；Skill 不编造精确成交概率。
4. **把候选词压缩成安全词根。** 若多条“只买配件”的词都含 `replacement`，先评估能否用这一条词组否定覆盖；`filter`、`battery` 等修饰词只有独立出现也主要表示无效意图时，才另做否定。不能为了缩短词而扩大到有价值的查询。
5. **检查商品大词与重复项。** 否词里不保留 `vacuum`、`light/lights` 这类直接描述本商品的词。比如 `pool vacuum`，先评估能否只否定 `pool`；`floor lamp` 去掉 `lamp` 后的 `floor` 若仍可能是有效场景，就不能直接否定。导出后运行仓库中的检查脚本，再交付 Excel。

**相邻商品不自动否定。** 例如卖无线立式吸尘器时，`robot vacuum` 可能是明显不同的购买意图，也可能值得低预算测试。是否否定 `robot`，要结合商品替代性和广告主策略判断。

### 二、搜索词报表分析

1. **按广告活动和完整搜索词汇总。** 按天报表的曝光、点击、花费、订单和销售额相加；CTR、CPC、CVR、CPA、ACOS、ROAS 用汇总值重算。先识别已经否定的词，并核对商品、站点、币种与订单归因时间。
2. **先找低绩效词。** 重点看持续花费、点击多而零单，或在可靠利润口径下持续亏损的完整搜索词。相关性可以解释表现，但不是筛选的第一道门槛。商品核心词若在某个活动中长期吃掉花费却不出单，也可以建议**在该活动精准否定这个完整词**。
3. **先给精准建议，再找词根。** 每条完整搜索词先展示自己的投放数据。只有多条建议否定的词共享安全的错误意图，且不会挡住其他有价值的搜索词时，才额外提出词组否定词根。没有安全词根，就只给精准否定。
4. **让广告主看得到依据。** Excel 保留竞价、ABA 日排名、曝光、点击、CTR、CPC、花费、订单、销售额、CVR、CPA、ACOS、ROAS 等关键数据；缺失值留空，不编造利润、风险等级或未来可节省金额。

例如，卖鼠标的广泛投放活动里，完整搜索词 `mouse` 若累积二十多次成熟点击、持续花费且零订单，可以考虑在**这个活动**精准否定 `mouse`，继续观察其他搜索词。二十次点击只是示例，不是所有商品的统一阈值。

## 交付什么

- **投前：** 一个 Excel 工作簿，工作表名为`否词表`，只放`站点`、`前置否词`、`中文翻译`、`否定匹配方式`、`原因`。原因用一句日常语言说明买家想买什么、为何当前商品不适合。内部研究线索、待定词和来源不塞进表格。
- **报表分析：** 每个广告活动一张工作表，活动名称写在表头下方。主表先列完整搜索词的精准否定建议、简短原因和关键投放数据；如有安全词根，再在同一工作表下方列词组否定建议。广告主能据此逐条决定是否执行。

完整判断规则和字段格式见 [投前规则](references/prelaunch.md)、[报表规则](references/report-analysis.md)及 [Excel 格式](references/workbook-schema.md)。

## 安装

### Codex、Claude Code、Cursor 等 Agent

安装了 Node.js 和 npm 后，在终端运行：

```bash
npx skills add jasmineztoh/amazon-sp-negative-keywords
```

按提示选择 Agent 与安装范围。以下命令可直接全局安装，供所有项目使用：

| Agent | 命令 |
| --- | --- |
| Codex | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a codex -y` |
| Claude Code | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a claude-code -y` |
| Cursor | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a cursor -y` |
| OpenCode | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a opencode -y` |
| Gemini CLI | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a gemini-cli -y` |
| GitHub Copilot | `npx skills add jasmineztoh/amazon-sp-negative-keywords -g -a github-copilot -y` |

`-g` 表示全局安装；去掉它即安装到当前项目。`npx` 运行的是 [Skills CLI](https://github.com/vercel-labs/skills)，本仓库无需发布 npm 包。安装器需要访问 GitHub；若克隆时遇到连接重置或 502，可稍后重试，或下载本仓库 ZIP 后从本地安装。

### WorkBuddy

**直接把下面这段话发送给 WorkBuddy**，不要粘贴到 PowerShell：

```text
请帮我从 GitHub 安装这个 Skill：
仓库地址：https://github.com/jasmineztoh/amazon-sp-negative-keywords
安装到用户级目录：~/.workbuddy/skills/amazon-sp-negative-keywords

如果 git 克隆失败，请从 https://api.github.com/repos/jasmineztoh/amazon-sp-negative-keywords/zipball 下载仓库 ZIP，解压后去掉自动生成的顶层文件夹。确认目标目录直接包含 SKILL.md、references 和 scripts；完成后检查 WorkBuddy 是否识别到 amazon-sp-negative-keywords，并告诉我结果。
```

这是给 WorkBuddy 的自然语言安装指令。当前 [Skills CLI 的支持列表](https://github.com/vercel-labs/skills#supported-agents)没有 WorkBuddy，因此 README 不提供未经支持的 `-a workbuddy` 命令。

## 怎么使用

**投前：** 给出商品 ASIN 和站点。Agent 需能访问该站点的亚马逊商品页，并能生成 Excel。

```text
使用 amazon-sp-negative-keywords，为美国站 ASIN B0XXXXXXXX 搜集 SP 投放前否词，输出 Excel。
```

**报表：** 上传 SP 搜索词报表；若报表无法确认广告商品，再提供 ASIN 与活动的对应关系。利润或目标成本资料有则提供，没有也可以分析，但不能据此断言盈利或亏损。

```text
使用 amazon-sp-negative-keywords，分析这份 SP 搜索词报表，找出建议新增的否词，保留每条建议的关键投放数据，输出 Excel。
```

Skill 不会直接改动线上广告设置，也不会把未经核实的商品信息或缺失数据当作事实。

## 更新

通过 Skills CLI 安装：

```bash
npx skills update amazon-sp-negative-keywords
```

通过 WorkBuddy 安装：在 WorkBuddy 中说“请更新 `amazon-sp-negative-keywords` Skill，来源仍是 `https://github.com/jasmineztoh/amazon-sp-negative-keywords`，保留用户级安装位置”，然后检查它是否仍能识别该 Skill。

## 仓库内容

- [SKILL.md](SKILL.md)：任务入口与共同规则
- [references/](references/)：投前、报表和 Excel 的详细规则
- [scripts/check_prelaunch.py](scripts/check_prelaunch.py)：投前表格检查脚本，使用 Python 3 标准库

## 许可

[MIT License](LICENSE)

