import json, re, sys

tool_input = json.load(sys.stdin).get("tool_input", {})
paths = [v.replace("\\", "/") for v in tool_input.values()
         if isinstance(v, str) and "\n" not in v and re.search(r"\.(py|md|csv|json|jsonl)$", v)]

if any(re.search(r"(^|/)prod/", p) for p in paths):
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "要改生产参数：先看变更单里的原值、新值和依据，再决定是否允许"
    }}, sys.stdout, ensure_ascii=False)
sys.exit(0)
