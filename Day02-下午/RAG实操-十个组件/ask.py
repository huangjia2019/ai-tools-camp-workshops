"""问一个问题，看回答和检索到的块。

    python ask.py "XM2701 现在的涨跌停板幅度是多少？"
    python ask.py "会员服务系统每周什么时候停机维护？" --role staff
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag.pipeline import RAG  # noqa: E402

ap = argparse.ArgumentParser(description='问一个问题')
ap.add_argument('question')
ap.add_argument('--role', default='member', choices=['member', 'staff'])
a = ap.parse_args()
ans, hits, req = RAG().ask(a.question, a.role)
print(ans)
print('\n交给响应生成的块：')
for h in hits:
    print(f"  {h['id']}　相似度 {h['score']}　{h['text'][:70].replace(chr(10), ' ')}")
