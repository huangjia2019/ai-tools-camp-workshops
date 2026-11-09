# 04 MCP：查询交易参数并核对来源

| 文件 | 内容 |
|---|---|
| xm_lab_server.py | 只读的参数查询服务 xm-lab |
| xm_data.json | 服务用的数据 |
| inbox/ | 收到的通知 |
| test_server.py | 服务自测 |
| show_config.py | 按本机路径打印 MCP 配置 |
| 配置示例.json | 配置的样子，路径要换成本机的 |

## 先运行

```
python3 test_server.py
python3 show_config.py
```

## 接入服务

Qoder CN：设置 → MCP 服务 → 我的服务，点“添加”，Qoder 打开 `~/.qoder-cn/mcp.json`。把 show_config.py 输出里 `xm-lab` 这一项放进 `mcpServers`；文件里已经有别的服务时只加这一项，不要整段覆盖。保存后列表里出现 xm-lab，展开能看到四个工具。切到智能体模式再提问。

TRAE：设置 → MCP → 添加 → 手动配置，粘贴 show_config.py 打印的 JSON，确认。列表里出现 xm-lab，展开能看到四个工具。

## 提示词

1. `用 xm-lab 查询 XM2702 在 2027-01-05 的参数，并按结算价 20000 计算涨跌停价，列出来源。`
2. `用 xm-lab 查询 XM2703 在 2027-01-12 的一般持仓保证金，再读 inbox 里的通知，把两处信息对照列出来，不修改任何文件。`

检查：服务返回的值和通知是否一致；核对日期、适用范围和来源，不直接覆盖数据。
