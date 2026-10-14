# 亚马逊 SP 否词 Skill

帮助广告主为 Amazon Sponsored Products 广告整理否定关键词，包含两种任务：

- **投前否词**：核实当前商品页，寻找购买意图错配的词，优先用安全词根做词组否定，输出 Excel 否词表。
- **搜索词报表分析**：先根据活动内的投放表现建议对完整搜索词精准否定，再检查能否提炼安全的词组否定词根。表格保留判断所需的投放数据。

本 Skill 使用中文说明。生成的是建议，由广告主决定是否应用到广告活动。

## 安装

将本仓库克隆到 Agent 的 Skills 目录。例如，在 PowerShell 中安装到 Codex：

```powershell
git clone https://github.com/zhangyanhua574-commits/amazon-sp-negative-keywords.git "$HOME\.codex\skills\amazon-sp-negative-keywords"
```

也可以把仓库放在项目的 `.agents/skills/amazon-sp-negative-keywords/` 下。仓库根目录就是 Skill 目录，入口文件为 [SKILL.md](SKILL.md)。

## 使用示例

```text
使用 $amazon-sp-negative-keywords，为美国站 ASIN B0XXXXXXXX 搜集 SP 投放前否词，输出 Excel。
```

```text
使用 $amazon-sp-negative-keywords，分析这份 SP 搜索词报表，建议应否定的搜索词并保留关键投放数据。
```

投前任务需要能访问对应站点的 Amazon 商品详情页；报表任务需要用户提供报表。缺少利润数据时不会编造利润或节省金额。

投前结果的检查脚本使用 Python 3 标准库，无须另装 Python 包：

```powershell
python scripts/check_prelaunch.py 否词表.xlsx --core light lights solar
```

## 目录

- `SKILL.md`：任务入口与总规则
- `references/`：投前、报表分析和 Excel 格式规则
- `scripts/check_prelaunch.py`：投前否词表的结构和商品大词检查

## 许可

[MIT License](LICENSE)
