# Agent 扩展配置练习

01 到 06 按编号做，每次只打开当前练习文件夹；07-选型技能是选讲。Qoder CN 使用 [Qoder 操作说明](Qoder操作说明.md)，下列步骤对应 TRAE CN。Windows 上把命令里的 python3 换成 python。

```
模块二/
├── 01-rules/       notice.md、notice-incomplete.md、data.json、rule-template.md
├── 02-skills/      notice.md、notice-incomplete.md、data.json、skill-template/
├── 03-subagents/   RULES.md、limits.py、price-checker-template.md、.lingma/agents/price-checker.md
├── 04-mcp/         xm_lab_server.py、xm_data.json、inbox/、show_config.py、test_server.py、配置示例.json
├── 05-hooks/       app.py、tests/、.trae/hooks/protect_tests.py、configure.py、test_guard.py、
│                   guard.py、configure_qoder.py、test_qoder_guard.py（Qoder CN 用）
└── 06-testing/     RULES.md、limits.py、test_limits.py
```

## 01 Rules

设置 → 规则与记忆 → 规则 + 创建 → 项目，名称填 `param-review`，生成 `.trae/rules/param-review.md`；生效方式保持“始终生效”，正文照抄 rule-template.md 的三条要求。提问后展开回复顶部的“参考内容”，能看到 rules 下的 param-review.md。

1. `阅读 notice-incomplete.md，核对这项参数调整，列出需要补充的信息，不修改文件。`
2. `阅读 notice.md 和 data.json，核对这项参数调整，不修改文件。`

## 02 Skills

把 skill-template 整个文件夹复制为 `.trae/skills/param-change-review/`（集成终端里运行 `mkdir -p .trae/skills && cp -R skill-template .trae/skills/param-change-review`），设置 → 技能与命令 → 项目 里能看到这个技能。

1. `请使用 param-change-review，读取 notice.md 和 data.json，在回复中输出参数变更单，不修改数据。`
2. `读取 notice-incomplete.md，核对这项参数变更。`
3. `解释一下 data.json 里 as_of 这个字段是什么意思。`

## 03 子智能体

先到 设置 → Beta 确认“启用 Subagents 目录”已打开，再把 price-checker-template.md 复制为 `.trae/agents/price-checker.md`。回复里出现 price-checker 的子智能体卡片，展开能看到它只读了两个文件。

`请调用 price-checker，只读检查 limits.py 是否符合 RULES.md，给出文件位置与修改建议。主智能体也不要修改文件。`

## 04 MCP

```
python3 test_server.py
python3 show_config.py
```

把 show_config.py 打印的 JSON 粘贴到 TRAE：设置 → MCP → 添加 → 手动配置 → 确认。列表里出现 xm-lab，展开能看到四个工具。

1. `用 xm-lab 查询 XM2702 在 2027-01-05 的参数，并按结算价 20000 计算涨跌停价，列出来源。`
2. `用 xm-lab 查询 XM2703 在 2027-01-12 的一般持仓保证金，再读 inbox 里的通知，把两处信息对照列出来，不修改任何文件。`

## 05 Hooks

```
python3 test_guard.py
python3 configure.py
```

TRAE：设置 → Hooks → 项目，打开“已配置的 Hooks”开关，在安全警示里点“启用”。拦截记录在同一页“查看日志”里。

1. `只使用 Edit 工具，把 tests/test_prices.py 中的 EXPECTED_UP 改为 99999。如果被拒绝，立即停止，不改脚本，不换工具。`
2. `只使用 Edit 工具，把 app.py 的 LABEL 改为 demo calculator。不要运行命令。`

## 06 测试与审查

```
python3 -m unittest -v
```

1. `读取 RULES.md，只在 test_limits.py 里增加 20003、0.07、5 这一组输入的测试。先写出算式和期望值，暂时不改 limits.py。`
2. `只修改 limits.py，让全部测试通过；不改测试的期望值，不删断言。`
3. `读取 RULES.md 和本次改动，列出改动的文件位置、对应的规则和可以复现的输入；再列出还没有测试覆盖的输入。`
