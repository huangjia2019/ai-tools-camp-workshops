import json, re, sys

# 写 prod/ 的编辑一律拒绝，由人审批后发布（Qoder 以退出码 2 拦截）
tool_input = json.load(sys.stdin).get("tool_input", {})
paths = [v.replace("\\", "/") for v in tool_input.values()
         if isinstance(v, str) and "\n" not in v and re.search(r"\.(py|md|csv|json|jsonl)$", v)]

prod = [p for p in paths if re.search(r"(^|/)prod/", p)]
if prod:
    print("拒绝写入：生产参数要先看变更单里的原值、新值和依据，由人批准后发布，智能体不能直接写：" + "、".join(prod), file=sys.stderr)
    sys.exit(2)
sys.exit(0)
