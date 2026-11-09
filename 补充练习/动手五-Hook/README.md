# 动手五：Hook

## .trae/hooks.json

```json
{
  "version": 1,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python3 .trae/hooks/guard_tests.py", "timeout": 10 }
        ]
      }
    ]
  }
}
```

## 让 Agent 建好脚本

```
在当前项目创建文件 .trae/hooks/guard_tests.py，内容如下（照抄，不要改动）：

import json, re, sys

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})
text = json.dumps(tool_input, ensure_ascii=False)
paths = [v for v in tool_input.values() if isinstance(v, str) and re.search(r"\.(py|js|ts|html|md|json)$", v)]

if any("test" in p.lower() for p in paths) and "依据" not in text:
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "修改测试文件，必须在改动里写明依据，例如：# 依据：6 月 30 日通知"
    }}, sys.stdout, ensure_ascii=False)
sys.exit(0)
```

## 试一下

```
新建一个文件 test_limits.md，写一条用例：结算价 80000、幅度 9%、最小变动价位 10，涨停价 87200，跌停价 72800。
```

Windows 上把 python3 换成 python。
