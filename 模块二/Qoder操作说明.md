# Qoder CN IDE 练习说明

练习在本目录的六个文件夹里（01-rules 到 06-testing），每次打开对应的文件夹。只使用课程材料，不连接真实交易系统。Windows 命令中的 `python3` 可换成 `python`。

## 开始之前

- 打开文件夹时，Qoder 先问“是否信任此文件夹中的文件的作者?”，选“是，我信任此作者”；可以勾选“信任父文件夹中所有文件的作者”，后面五个文件夹就不再问。随后如果问“为此项目建立代码库索引?”，选“建立索引”。不信任时是受限模式，Hook 不会执行。
- 右侧会话输入框左下角是模式：“智能问答”只读，用来分析；“智能体”会改文件、运行命令。讲义里的 Ask、Agent 就是这两个模式。
- 设置用账号菜单里的“Qoder IDE 设置”（⇧⌘,）打开。改了技能、Hook 或 MCP 配置后，用命令面板（⇧⌘P）运行“开发人员: 重新加载窗口”。

## Rules

打开 `01-rules`。设置 → 规则 → 添加 → 项目级规则，名称填 `param-review`，回车。Qoder 新建 `.qoder/rules/param-review.md` 并打开，顶部“类型”选“手动引入”。把 `rule-template.md` 正文里的三条要求粘贴进去，开头 `---`、`alwaysApply: true`、`---` 这三行是 TRAE 的写法，不要复制。保存。

新建会话，输入 `@`，选“规则”，再选 `param-review.md`，然后提问：先让 Qoder 阅读 `notice-incomplete.md` 并列出缺失信息；再阅读 `notice.md` 和 `data.json`，核对参数和生效条件。两次都不修改文件。

对照：新建会话，不引入规则再问一次。智能体有时会自己去读规则文件或模板，所以对照不能只看回复格式，要展开回复里的“已处理 N 个操作”，看它读了哪些文件。

## Skills

打开 `02-skills`，将 `skill-template` 整个目录复制到 `.qoder/skills/param-change-review/`（放 `.lingma/skills/param-change-review/` 也能读），保留 `SKILL.md` 与 `templates/`。重新加载窗口，在会话里输入 `/param` 确认技能出现在列表里。

输入 `/param-change-review`，要求读取 `notice.md` 和 `data.json`，在回复中输出参数变更单，不改数据。然后不点名技能，只说“读取 notice-incomplete.md，核对这项参数变更”，检查调用记录中是否出现 Skill；没有触发时，再用 `/param-change-review` 显式调用。2026-11-04 实测这一句触发了技能，并停下来列出待确认项。最后单独询问 `as_of` 字段的含义，这时调用记录里不应出现 Skill。它可能把 `skill-template` 里的文件当普通文件读，回答里引用 SKILL.md，这不算调用技能；判断以调用记录为准。

## 子智能体

打开 `03-subagents`，使用已提供的 `.lingma/agents/price-checker.md`。

输入 `/price-checker`，要求只读检查 `limits.py` 是否符合 `RULES.md`，给出函数位置、规则依据和反例，并写明“主智能体也不要修改文件”。确认调用记录里出现 price-checker 的子智能体卡片，检查文件没有被修改。

这是只读审查：子智能体只配置读取和搜索工具，主会话也要求不修改文件，检查结束后核对文件差异。子智能体的工具限制只约束它自己，如果只说“顺手把取整也改了”，主智能体会接过去自己改。

## MCP

打开 `04-mcp`，在集成终端（⌃`）运行：

```sh
python3 test_server.py
python3 show_config.py
```

设置 → MCP 服务 → 我的服务，在“全部”或“用户级”标签下点“添加”，Qoder 直接打开 `~/.qoder-cn/mcp.json`。把 `show_config.py` 输出里 `xm-lab` 这一项放进 `mcpServers`；文件里已经有别的服务时只加这一项，不要整段覆盖。保存后列表里出现 `xm-lab`，展开能看到四个工具。

切到智能体模式，查询 XM2703 在 2027-01-12 的一般持仓保证金，和 `inbox/` 通知对照。记录工具输入、结果和来源，解释差异，不修改参数文件。

## Hooks

打开 `05-hooks`，运行：

```sh
python3 test_qoder_guard.py
python3 configure_qoder.py
```

配置脚本只写项目目录（`.lingma/settings.json`），不写用户级设置；已有配置时停止。重新加载窗口后，仅用编辑工具请求修改 `tests/test_prices.py`，应被拒绝；再请求修改 `app.py` 的 LABEL，应被允许。请求里写明：如果被拒绝，立即停止，不改拦截脚本，不换工具。

Qoder 传给 Hook 的编辑工具名是 `SearchReplace`。配置里的 matcher 写 `Edit|Write` 也能匹配到它，`guard.py` 按 `SearchReplace` 等名字判断，`test_qoder_guard.py` 里有对应的检查。这个练习只检查编辑工具的文件目标，不覆盖终端等其他写入方式。

## 测试与审查

打开 `06-testing`，先运行 `python3 -m unittest -v`。先在智能问答模式读取规则、实现和测试，确认后切到智能体模式：补充输入 `20003、0.07、5` 的边界测试，先列出算式与期望值，再修改实现。检查旧断言没有被删除或改成当前错误结果。

## 版本参考

以上步骤在 2026-11-04 用 Qoder CN IDE 1.34.0（基于 VS Code 1.106.3）实测。在设置页或用内置技能新建的规则、技能、子智能体、指令写在项目的 `.qoder/` 下；本练习提供的 `.lingma/` 下的文件同样会被读取。官方说明见 [Qoder CN IDE 文档](https://docs.qoder.cn/user-guide/rules)，Skills、子智能体和 Hooks 分别参见同站的 `skills`、`custom-agent`、`hooks` 页面。
