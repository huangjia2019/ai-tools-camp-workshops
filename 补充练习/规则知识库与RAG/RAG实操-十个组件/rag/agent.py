"""组件十　复杂 RAG 范式：智能体式 RAG（Agentic RAG）。

普通 RAG 查一次就作答。有的问题一次查不全：原通知被更正过，要再取更正通知；
问保证金金额，要比例、交易单位和计算公式，分散在三份文件里。
智能体式 RAG 每查完一轮，先看手里的资料还缺什么，缺就再查，直到不缺、或者查满 MAX_ROUNDS 轮；
要算的数交给计算工具，不让模型心算。

基础版的 missing() 什么都不缺，所以只查一轮，和 pipeline 一样。
"""
import re

from .config import TODAY
from .generate import answer
from .pre import prepare
from .utils import parse_date, split_sentences

MAX_ROUNDS = 3


def missing(question, pool, req):
    """看已经拿到的块（pool），判断还缺什么。返回要做的事，每件是 (动作, 内容, 为什么)：

        ('文件', '第103号', '第102号被第103号更正')        取出这份文件的全部块
        ('检索', '交易单位 吨/手', '算金额要交易单位')      用这段文字再检索一次

    pool 里每块有 id、doc、text、meta；meta 里有“被更正”“取代”这些关系。返回空列表表示资料够了。
    基础版认为一次就够。
    """
    return []


def is_amount(question):
    """问的是不是保证金金额：问题里给了结算价和手数。"""
    return bool(re.search(r'结算价\s*\d', question) and re.search(r'\d+\s*手', question))


def _valid(meta, day):
    if meta.get('生效日期', '') > day:
        return False
    return not (meta.get('失效日期') and meta['失效日期'] <= day)


def compute_amount(question, pool, docs, today=TODAY):
    """计算工具：交易保证金 = 结算价 × 交易单位 × 持仓手数 × 交易保证金比例（规则摘录第 3 条）。

    只读手里已有的文件（pool 里出现过的文件，读全文）。比例只从那一天有效的文件里取；
    原通知被更正、更正通知也在手里时，用更正后的数。缺哪样就说缺哪样，不猜。返回回答文字，格式和 generate.py 相同。
    """
    day = parse_date(question, today) or today
    price = float(re.search(r'结算价\s*(\d+(?:\.\d+)?)', question).group(1))
    lots = int(re.search(r'(\d+)\s*手', question).group(1))
    kind = '套期保值' if re.search(r'套保|套期保值', question) else '一般持仓'
    texts = {d['id']: d['text'] for d in docs}
    docs = {h['doc']: h['meta'] for h in pool}
    ratio = unit = None
    cites = []
    fixed = {m.get('更正') for m in docs.values()} - {None}           # 手里有更正通知的原通知
    for d, m in docs.items():
        if not _valid(m, day):
            continue
        for s in split_sentences(texts[d]):
            if kind in s and '%' in s and '比例' in s:
                if d in fixed and not m.get('更正'):
                    cites.append((d, s))                            # 原通知照样引用，比例以更正通知为准
                    continue
                ratio = float(re.findall(r'(\d+(?:\.\d+)?)\s*%', s)[-1])
                cites.append((d, s))
            if '交易单位' in s and re.search(r'\d+\s*吨/手', s):
                unit = float(re.search(r'(\d+)\s*吨/手', s).group(1))
                cites.append((d, s))
            if '交易保证金' in s and '=' in s:
                cites.append((d, s))
    lack = [n for n, v in (('交易保证金比例', ratio), ('交易单位', unit)) if v is None]
    if lack:
        return '结论：资料不全，不能计算：缺少' + '、'.join(lack)
    amount = price * unit * lots * ratio / 100
    fmt = lambda x: f'{x:g}'
    head = f'结论：交易保证金 = {fmt(price)} × {fmt(unit)} × {lots} × {fmt(ratio)}% = {fmt(amount)} 元（计算工具算出）'
    seen, lines = set(), [head]
    for d, s in cites:
        if (d, s) not in seen:
            seen.add((d, s))
            lines.append(f'依据：〔{d}〕{s}')
    return '\n'.join(lines)


def run(rag, question, role='member', today=TODAY):
    """返回 (回答, 用到的块, 过程)。过程每轮一行：(第几轮, 查了什么, 为什么, 新拿到的块)。"""
    req = prepare(question, role, today)
    pool = rag.retrieve(req)
    trace = [(1, question, '普通检索', [h['id'] for h in pool])]
    done = set()
    for r in range(2, MAX_ROUNDS + 1):
        todo = [t for t in missing(question, pool, req) if (t[0], t[1]) not in done]
        if not todo:
            break
        for act, what, why in todo:
            done.add((act, what))
            if act == '文件':
                got = rag.store.chunks_of(what)
            else:
                got = rag.store.search(what, n=2, where=req.get('where'), filters=req.get('filters'))
            have = {h['id'] for h in pool}
            new = [dict(h, score=h.get('score', 0)) for h in got if h['id'] not in have and h.get('kind') != '摘要']
            pool += new
            trace.append((r, what, why, [h['id'] for h in new]))
    ans = compute_amount(question, pool, rag.docs, today) if is_amount(question) else answer(req, pool)
    return ans, pool, trace
