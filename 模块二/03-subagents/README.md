# 03 子智能体：只读检查价格取整代码

用 Qoder CN 或 TRAE 打开本文件夹（菜单“文件 → 打开文件夹”），只打开这一个文件夹；问是否信任作者时选信任。

| 文件 | 内容 |
|---|---|
| RULES.md | 涨跌停价的计算规则 |
| limits.py | 计算涨跌停价的实现 |
| price-checker-template.md | 子智能体模板（TRAE 用） |
| .lingma/agents/price-checker.md | 已经配好的子智能体（Qoder CN 用），只配 Read、Grep、Glob |

## 准备子智能体

Qoder CN：直接使用文件夹里的 `.lingma/agents/price-checker.md`。会话里输入 `/price`，列表里出现 price-checker，选中它再发提示词。

TRAE：先到 设置 → Beta，确认“启用 Subagents 目录”已打开；把 price-checker-template.md 复制为 `.trae/agents/price-checker.md`。新建任务，发下面的提示词。

## 提示词

`请调用 price-checker，只读检查 limits.py 是否符合 RULES.md，给出文件位置与修改建议。主智能体也不要修改文件。`

检查：调用记录里有 price-checker 的子智能体卡片；它只用了读取和搜索工具；报告有源码位置和规则依据；文件没有被修改。
