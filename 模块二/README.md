# 模块二：Agent 扩展配置练习

01、02、04 用同一份练习数据：通知 LAB-104，XM2703 的一般持仓保证金自 2027-01-11 起由 9% 调整为 10%，涨跌停板幅度不变。03、06 用同一份涨跌停价规则和实现（RULES.md、limits.py）。

| 文件夹 | 更新时间 |
|---|---|
| [01-rules](01-rules/) | 2026-11-09 16:08 |
| [02-skills](02-skills/) | 2026-11-09 16:08 |
| [03-subagents](03-subagents/) | 2026-11-09 16:08 |
| [04-mcp](04-mcp/) | 2026-11-09 16:08 |
| [05-hooks](05-hooks/) | 2026-11-09 16:08 |
| [06-testing](06-testing/) | 2026-11-09 16:08 |
| [07-选型技能](07-选型技能/) | 2026-11-09 16:08 |

```
模块二/
├── 01-rules/       notice.md、notice-incomplete.md、data.json、rule-template.md
├── 02-skills/      notice.md、notice-incomplete.md、data.json、skill-template/
├── 03-subagents/   RULES.md、limits.py、price-checker-template.md、.lingma/agents/price-checker.md
├── 04-mcp/         xm_lab_server.py、xm_data.json、inbox/、show_config.py、test_server.py、配置示例.json
├── 05-hooks/       app.py、tests/、.trae/hooks/protect_tests.py、configure.py、test_guard.py、
│                   guard.py、configure_qoder.py、test_qoder_guard.py（Qoder CN 用）
├── 06-testing/     RULES.md、limits.py、test_limits.py
└── 07-选型技能/    tool-selection/、推荐器.py
```

## 开始之前

- 代码练习只需要 Python 3，不装第三方包。Windows 上把命令里的 python3 换成 python，先运行 `python --version`。
- 不信任文件夹时是受限模式，Hook 不会执行。Qoder CN 可以勾选“信任父文件夹中所有文件的作者”，后面几个文件夹就不再问。
- Qoder CN：右侧会话框左下角选模式，“智能问答”只读，用来分析；“智能体”会改文件、运行命令。设置在账号菜单的“Qoder IDE 设置”（⇧⌘,）。改了技能、Hook 或 MCP 配置后，用命令面板（⇧⌘P）运行“开发人员: 重新加载窗口”。
- TRAE：规则、技能、MCP、Hooks 的入口都在“设置”里。

Qoder CN 的实测细节和版本说明见 [Qoder操作说明.md](Qoder操作说明.md)。
