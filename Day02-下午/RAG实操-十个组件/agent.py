"""智能体式 RAG：一次查不全就再查，看每一轮查了什么。

    python agent.py "1 月 4 日起，XM2701 结算价 20000 元/吨，持有 2 手套保持仓，交易保证金是多少？"
    python agent.py "12 月 31 日晚上有夜盘吗？"
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag.agent import run  # noqa: E402
from rag.pipeline import RAG  # noqa: E402

ap = argparse.ArgumentParser(description='智能体式 RAG')
ap.add_argument('question')
ap.add_argument('--role', default='member', choices=['member', 'staff'])
a = ap.parse_args()
ans, pool, trace = run(RAG(), a.question, a.role)
for r, what, why, got in trace:
    print(f'第 {r} 轮　{why}：{what}')
    print('    拿到：' + ('、'.join(got) or '没有新的块'))
print()
print(ans)
