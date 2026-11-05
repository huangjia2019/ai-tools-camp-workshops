# 模块二：Agent 扩展配置练习

01 到 06 按编号做，每次只打开当前这一个练习文件夹。规则、技能、子智能体、Hook 都按项目生效，打开“模块二”这一级，几个练习的配置会互相串。每个文件夹里的 README.md 写着文件清单、要运行的命令、要粘贴的提示词，以及 Qoder CN 和 TRAE 的入口。07-选型技能是选讲。

| 文件夹 | 练习 |
|---|---|
| [01-rules](01-rules/) | 用项目规则核对通知中的缺失信息 |
| [02-skills](02-skills/) | 安装参数复核技能，做触发测试 |
| [03-subagents](03-subagents/) | 只读子智能体检查价格取整代码 |
| [04-mcp](04-mcp/) | 接入只读参数服务，查询并核对来源 |
| [05-hooks](05-hooks/) | 按路径检查文件修改权限 |
| [06-testing](06-testing/) | 补边界用例，修正取整实现 |
| [07-选型技能](07-选型技能/) | 选讲：安装、调用工具选型技能 |

六个练习用同一份虚构数据：教学通知 LAB-104，XM2703 的一般持仓保证金自 2027-01-11 起由 9% 调整为 10%，涨跌停板幅度不变。它不代表任何交易所的规定。

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

每个文件夹里另有一份 README.md。

## 开始之前

- 代码练习只需要 Python 3，不装第三方包。Windows 上把命令里的 python3 换成 python，先运行 `python --version`。
- 打开文件夹时会问是否信任作者，选信任。Qoder CN 可以勾选“信任父文件夹中所有文件的作者”，后面几个文件夹就不再问。不信任时是受限模式，Hook 不会执行。
- Qoder CN：右侧会话框左下角选模式，“智能问答”只读，用来分析；“智能体”会改文件、运行命令。设置在账号菜单的“Qoder IDE 设置”（⇧⌘,）。改了技能、Hook 或 MCP 配置后，用命令面板（⇧⌘P）运行“开发人员: 重新加载窗口”。
- TRAE：规则、技能、MCP、Hooks 的入口都在“设置”里，各练习的 README 写了具体位置。

Qoder CN 的实测细节和版本说明见 [Qoder操作说明.md](Qoder操作说明.md)。
