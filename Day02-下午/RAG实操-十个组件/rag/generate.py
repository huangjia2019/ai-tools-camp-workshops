"""组件八　响应生成：根据检索到的块写回答。

练习系统不调用大模型，用抽取的办法作答：从块里挑出最贴近问题的一句，原样照抄。回答格式固定：
    结论：<一句话>
    依据：〔文件编号〕<原文一句>        依据可以有多行，每行一份文件
资料里找不到依据时，只写一行：结论：资料中没有依据，不能回答

基础版按字面重合挑句子，只引一份文件，从不拒答。
"""
from .utils import overlap, split_sentences

REFUSE = '资料中没有依据，不能回答'


def answer(req, hits):
    if not hits:
        return f'结论：{REFUSE}'
    best, doc = max(((s, h['doc']) for h in hits for s in split_sentences(h['text'])), key=lambda x: overlap(req['question'], x[0]))
    return f"结论：{best}\n依据：〔{doc}〕{best}"
