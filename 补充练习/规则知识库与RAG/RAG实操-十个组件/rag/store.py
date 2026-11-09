"""组件四　向量存储：向量、原文、元数据存在同一条记录里，检索时可以按元数据过滤。"""
from .embed import cosine


def match(meta, filters):
    """一块的元数据是否满足过滤条件。filters 是一个字典，可以有这几项：

        有效于   'YYYY-MM-DD'：只留那一天有效的文件。生效日期不晚于那一天；有失效日期的，失效日期要晚于那一天
        权限     允许的权限，比如会员是 ['公开']，交易所员工是 ['公开', '内部']
        状态     允许的状态，比如 ['现行']

    基础版还没有实现，什么都不过滤。
    """
    return True


class Store:
    def __init__(self, embedder):
        self.embedder = embedder
        self.rows = []

    def add(self, chunks):
        for c in chunks:
            self.rows.append(dict(c, vec=self.embedder.encode(c['text'])))

    def search(self, query, n=10, where=None, filters=None):
        """返回和 query 最相似的 n 块，按相似度从高到低。

        filters  元数据过滤条件，一个字典，写法见上面的 match
        where    也可以直接给一个函数：收到一块的元数据，返回 True 这块才参与检索
        两个都是 None 时不过滤。
        """
        q = self.embedder.encode(query)
        hits = []
        for r in self.rows:
            if where is not None and not where(r['meta']):
                continue
            if filters and not match(r['meta'], filters):
                continue
            h = {k: v for k, v in r.items() if k != 'vec'}
            h['score'] = round(cosine(q, r['vec']), 4)
            hits.append(h)
        hits.sort(key=lambda h: -h['score'])
        return hits[:n]

    def chunks_of(self, doc_id):
        """取出某份文件的全部块（不经过检索）。"""
        return [{k: v for k, v in r.items() if k != 'vec'} for r in self.rows if r['doc'] == doc_id]
