"""组件二　文本分块：把每份文档切成块。

基础版按固定长度切，不管句子、条款和表格在哪里断开。
每块：{'id': '第102号#0', 'doc': 文档编号, 'text': 块的文字, 'meta': 文档的元数据}
"""
SIZE = 80   # 每块多少个字符


def make_chunks(docs):
    chunks = []
    for d in docs:
        text = d['text']
        n = 0
        for i in range(0, len(text), SIZE):
            piece = text[i:i + SIZE].strip()
            if piece:
                chunks.append({'id': f"{d['id']}#{n}", 'doc': d['id'], 'text': piece, 'meta': d['meta']})
                n += 1
    return chunks
