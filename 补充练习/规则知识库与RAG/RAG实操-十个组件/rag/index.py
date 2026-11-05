"""组件六　索引优化：在普通的块之外，再建一些专门用来检索的节点。

常见做法有两种。一种是每份文件建一个摘要节点，写上编号、标题、合约范围、生效时点、状态、取代与更正关系，
问“哪份通知、什么时候生效、被谁更正”时先找到文件；另一种是小块检索、大块作答（句子窗口、父子块）。

摘要节点和普通块一样进向量库，多一个键 'kind': '摘要'。检索到摘要节点以后，
expand() 把这份文件的正文块排进候选：摘要用来找文件，回答仍然引用正文。

基础版不加任何节点，原样返回。
"""
from .embed import cosine


def build_index(chunks, docs):
    return chunks


def expand(hits, store, query):
    """检索结果里有摘要节点时，把这份文件的正文块按和问题的相似度排进候选，摘要节点本身拿掉：
    摘要用来找到文件，回答仍然引用正文。"""
    if not any(h.get('kind') == '摘要' for h in hits):
        return hits
    q = store.embedder.encode(query)
    out = {h['id']: h for h in hits if h.get('kind') != '摘要'}
    for h in hits:
        if h.get('kind') != '摘要':
            continue
        for c in store.chunks_of(h['doc']):
            if c.get('kind') != '摘要' and c['id'] not in out:
                out[c['id']] = dict(c, score=round(cosine(q, store.embedder.encode(c['text'])), 4), via='摘要')
    return sorted(out.values(), key=lambda h: -h['score'])
