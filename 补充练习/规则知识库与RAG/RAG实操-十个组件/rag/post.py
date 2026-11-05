"""组件七　检索后处理：对候选块重排、过滤、补充，留下 TOP_K 块交给响应生成。

hits  候选块，按相似度从高到低；每块有 id、doc、text、meta、score
req   检索前处理给的请求（见 pre.py）
store 向量库；store.chunks_of(编号) 可以取出某份文件的全部块

基础版只取前 TOP_K 块。
"""
from .config import TOP_K


def postprocess(hits, req, store):
    return hits[:TOP_K]
