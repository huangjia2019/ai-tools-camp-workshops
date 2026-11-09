# 05 Hooks：文件修改权限检查

Hook 只在信任的文件夹里执行。

| 文件 | 内容 |
|---|---|
| app.py | 一个小程序，只有 LABEL 一个字符串 |
| tests/ | 测试，期望值由人维护，智能体不许改 |
| .trae/hooks/protect_tests.py、configure.py、test_guard.py | TRAE 用的检查脚本、配置脚本和自测 |
| guard.py、configure_qoder.py、test_qoder_guard.py | Qoder CN 用的检查脚本、配置脚本和自测 |

## 配置 Hook

Qoder CN：

```
python3 test_qoder_guard.py
python3 configure_qoder.py
```

配置写进本文件夹的 `.lingma/settings.json`，已有配置时脚本停下，不覆盖。命令面板运行“开发人员: 重新加载窗口”。

TRAE：

```
python3 test_guard.py
python3 configure.py
```

配置写进 `.trae/hooks.json`。设置 → Hooks → 项目，打开“已配置的 Hooks”开关，在安全警示里点“启用”。拦截记录在同一页的“查看日志”里。

## 提示词

每一句都新建一个会话。

1. `只使用 Edit 工具，把 tests/test_prices.py 中的 EXPECTED_UP 改为 99999。如果被拒绝，立即停止，不改脚本，不换工具。`
2. `只使用 Edit 工具，把 app.py 的 LABEL 改为 demo calculator。不要运行命令。`

检查：第 1 句是否被拒绝、第 2 句是否放行，对照工具日志和文件差异。这个检查只管配置的编辑事件，不等于完整的文件系统沙箱。
