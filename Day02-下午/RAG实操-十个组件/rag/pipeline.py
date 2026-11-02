"""把组件串起来。

建库：数据导入 → 文本分块 → 索引优化 → 信息嵌入 → 向量存储
提问：检索前处理 → 检索 → 检索后处理 → 响应生成
系统评估在 eval.py，复杂 RAG 范式（智能体式 RAG）在 rag/agent.py。
"""
from pathlib import Path

from .chunk import make_chunks
from .config import DOCS, TODAY, TOP_N
from .embed import Embedder
from .generate import answer
from .index import build_index, expand
from .load import load_docs
from .post import postprocess
from .pre import prepare
from .store import Store

ROOT = Path(__file__).resolve().parents[1]


class RAG:
    def __init__(self, docs_dir=None):
        self.docs = load_docs(docs_dir or ROOT / DOCS)
        self.chunks = build_index(make_chunks(self.docs), self.docs)
        self.store = Store(Embedder().fit([c['text'] for c in self.chunks]))
        self.store.add(self.chunks)

    def retrieve(self, req):
        hits = self.store.search(req['query'], n=TOP_N, where=req.get('where'), filters=req.get('filters'))
        hits = expand(hits, self.store, req['query'])
        return postprocess(hits, req, self.store)

    def ask(self, question, role='member', today=TODAY):
        req = prepare(question, role, today)
        hits = self.retrieve(req)
        return answer(req, hits), hits, req
