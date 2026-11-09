import json, re, sys

# 工作坊里还要让 TRAE 写 .trae/ 下的文件；正式使用时把 ".trae/" 去掉
ALLOWED = ("draft/", "notes/", "logs/", "sim/", "prod/", "cases/", ".trae/")
tool_input = json.load(sys.stdin).get("tool_input", {})
paths = [v.replace("\\", "/") for v in tool_input.values()
         if isinstance(v, str) and "\n" not in v and re.search(r"\.(py|md|csv|json|jsonl)$", v)]
outside = [p for p in paths if not any(re.search(r"(^|/)" + re.escape(a), p) for a in ALLOWED)]

if outside:
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "只能写 draft/、notes/、logs/、sim/、prod/、cases/：" + "、".join(outside)
    }}, sys.stdout, ensure_ascii=False)
sys.exit(0)
