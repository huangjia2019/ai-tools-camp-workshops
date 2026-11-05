"""组件三　信息嵌入：把文本变成向量。

为了不装任何依赖、断网也能跑，这里用“字符二元组 + TF-IDF”充当向量：
两段文字共有的二字片段越多、这些片段在知识库里越少见，余弦相似度就越高。
它只看字面，不懂近义词，这一点和真正的嵌入模型不同。换成 BGE 这类模型时，保持 fit 和 encode 两个接口不变即可。
"""
import math
from collections import Counter

from .utils import PUNCT


def grams(text):
    t = PUNCT.sub('', text).lower()
    return [t[i:i + 2] for i in range(len(t) - 1)]


class Embedder:
    def fit(self, texts):
        df = Counter()
        for t in texts:
            df.update(set(grams(t)))
        n = len(texts)
        self.idf = {g: math.log((n + 1) / (c + 1)) + 1 for g, c in df.items()}
        return self

    def encode(self, text):
        tf = Counter(grams(text))
        v = {g: c * self.idf.get(g, 1.0) for g, c in tf.items()}
        length = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {g: x / length for g, x in v.items()}


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(g, 0.0) for g, x in a.items())
