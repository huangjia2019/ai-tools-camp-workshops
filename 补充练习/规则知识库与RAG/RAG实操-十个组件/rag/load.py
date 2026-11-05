"""组件一　数据导入：把 docs/ 里的文件读成文档，每份文档有正文和元数据。

每份文件开头两行 --- 之间是元数据：编号、标题、类型、发布日期、生效日期、失效日期、状态、
取代 / 被取代、更正 / 被更正、权限。正文里可能有表格（Markdown 写法）。

返回的每份文档：{'id': 编号, 'meta': 元数据, 'text': 正文}
"""
from pathlib import Path

from .utils import parse_front_matter


def load_docs(folder):
    docs = []
    for path in sorted(Path(folder).glob('*.md')):
        meta, body = parse_front_matter(path.read_text(encoding='utf-8'))
        meta['文件'] = path.name
        docs.append({'id': meta['编号'], 'meta': meta, 'text': body})
    return docs
