import json, re, sys

# 只允许写下面这几个目录。工作坊里还要让 Qoder 写 .qoder/ 下的文件；正式使用时把 ".qoder/" 去掉
ALLOWED = ("draft/", "notes/", "logs/", "sim/", "prod/", "cases/", ".qoder/")
tool_input = json.load(sys.stdin).get("tool_input", {})
paths = [v.replace("\\", "/") for v in tool_input.values()
         if isinstance(v, str) and "\n" not in v and re.search(r"\.(py|md|csv|json|jsonl)$", v)]
outside = [p for p in paths if not any(re.search(r"(^|/)" + re.escape(a), p) for a in ALLOWED)]

if outside:
    print("拒绝写入：只能写 draft/、notes/、logs/、sim/、prod/、cases/：" + "、".join(outside), file=sys.stderr)
    sys.exit(2)
sys.exit(0)
