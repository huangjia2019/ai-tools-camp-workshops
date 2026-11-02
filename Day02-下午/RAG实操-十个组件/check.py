"""十个实操的检查。

    python check.py             列出十个实操现在各过了几项
    python check.py 03          检查实操三
    python check.py 03 --看     看实操三要解决的现象（改之前、改之后都可以看）

每个检查只测本实操负责的那个文件，用固定的小例子，不受别的组件改没改的影响。
实操十例外：智能体式 RAG 建在整条流水线上，前面的实操做得越多，它越顺。
"""
import argparse
import contextlib
import importlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from rag.utils import norm, parse_front_matter, split_sentences  # noqa: E402

OK, NO = '√', '×'
CASES = [('01', '数据导入', 'rag/load.py'), ('02', '文本分块', 'rag/chunk.py'), ('03', '信息嵌入', 'rag/embed.py'),
         ('04', '向量存储', 'rag/store.py'), ('05', '检索前处理', 'rag/pre.py'), ('06', '索引优化', 'rag/index.py'),
         ('07', '检索后处理', 'rag/post.py'), ('08', '响应生成', 'rag/generate.py'), ('09', '系统评估', 'eval.py'),
         ('10', '复杂 RAG 范式', 'rag/agent.py')]
TODAY = '2026-12-30'
Q_AMOUNT = '1 月 4 日起，XM2701 结算价 20000 元/吨，持有 2 手套保持仓，交易保证金是多少？'


# ---------------------------------------------------------------- 固定的小例子：不经过学员改的组件
def base_docs():
    """按基础版的办法读文件：元数据 + 原样的正文（表格还是 Markdown）。"""
    docs = []
    for p in sorted((ROOT / 'docs').glob('*.md')):
        meta, body = parse_front_matter(p.read_text(encoding='utf-8'))
        docs.append({'id': meta['编号'], 'meta': meta, 'text': body})
    return docs


def para_chunks(docs):
    """按空行分段，每段一块，块前带文件标题；表格每行一块。只给检查用。"""
    out = []
    for d in docs:
        n = 0
        for para in re.split(r'\n\s*\n', d['text']):
            lines = [x.strip() for x in para.splitlines() if x.strip() and not x.startswith('>')]
            pieces = lines if lines and lines[0].startswith('|') else ([''.join(lines)] if lines else [])
            for p in pieces:
                out.append({'id': f"{d['id']}#{n}", 'doc': d['id'], 'text': f"{d['meta']['标题']}｜{p}", 'meta': d['meta']})
                n += 1
    return out


def meta():
    return {d['id']: d['meta'] for d in base_docs()}


def conclusion(ans):
    return next((ln[3:] for ln in ans.splitlines() if ln.startswith('结论：')), '')


def cites(ans):
    return set(re.findall(r'〔(.+?)〕', ans))


def ask(question, role='member'):
    from rag.pipeline import RAG
    ans, hits, req = RAG().ask(question, role)
    print(f'问：{question}')
    print('　　' + ans.replace('\n', '\n　　'))
    print('　　交给响应生成的块：' + '、'.join(h['id'] for h in hits))


# ---------------------------------------------------------------- 实操一　数据导入
def show01():
    from rag.load import load_docs
    d = next(x for x in load_docs(ROOT / 'docs') if x['id'] == '第95号')
    print('第95号读进来以后，附表这几行是这样：')
    for ln in d['text'].splitlines():
        if 'XM27' in ln or '手续费' in ln and ('|' in ln or '：' in ln):
            print('　　' + ln)
    print()
    ask('XM2703 合约平今仓的手续费是多少？')


def check01():
    from rag.load import load_docs
    docs = {d['id']: d for d in load_docs(ROOT / 'docs')}

    def line_with(doc, *words):
        return any(all(norm(w) in norm(ln) for w in words) for ln in docs[doc]['text'].splitlines())
    return [(line_with('第95号', 'XM2703', '平今仓手续费', '4元/手'), '第95号附表：XM2703 那一行写成一句，带着“平今仓手续费”和“4 元/手”'),
            (line_with('技术服务收费标准', '托管机柜', '8000元/月'), '收费标准表：托管机柜那一行带着“8000 元/月”'),
            (line_with('现行参数表', 'XM2702', '一般持仓交易保证金比例', '8%'), '现行参数表：XM2702 那一行带着列名和“8%”'),
            (not any(ln.strip().startswith('|') for d in docs.values() for ln in d['text'].splitlines()), '所有文件里不再有“|”开头的表格行'),
            (all(d['meta'].get('编号') and d['meta'].get('生效日期') for d in docs.values()), '元数据还在：每份文件都有编号和生效日期')]


# ---------------------------------------------------------------- 实操二　文本分块
def show02():
    from rag.chunk import make_chunks
    docs = [d for d in base_docs() if d['id'] in ('交易限额规定', '会员问答')]
    for c in make_chunks(docs)[:8]:
        print(f"　　{c['id']}　{c['text'].replace(chr(10), ' / ')}")
    print()
    ask('单个客户在一个合约上的投机持仓最多多少手？')


def check02():
    from rag.chunk import make_chunks
    docs = base_docs()
    chunks = make_chunks(docs)
    title = {d['id']: d['meta']['标题'] for d in docs}

    def of(doc):
        return [c['text'] for c in chunks if c['doc'] == doc]
    return [(any('第一条' in x and '3000' in x and '第二条' not in x for x in of('交易限额规定')), '交易限额规定：第一条完整地在一块里，不和第二条混在一起'),
            (any('平今是什么意思' in x and '当日新开' in x and '套保' not in x for x in of('会员问答')), '会员问答：一问一答在同一块里'),
            (any('三、' in x and norm('由 7% 调整为 9%') in norm(x) for x in of('第102号')), '第102号：第三条整句在一块里'),
            (all(title[c['doc']] in c['text'] for c in chunks), '每一块都带着文件标题'),
            (bool(chunks) and all(len(c['text']) <= 300 for c in chunks), '没有超过 300 字的大块')]


# ---------------------------------------------------------------- 实操三　信息嵌入
ROWS = ['合约 XM2701：开仓手续费 3 元/手，平今仓手续费 6 元/手，平昨仓手续费 3 元/手。',
        '合约 XM2702：开仓手续费 2 元/手，平今仓手续费 5 元/手，平昨仓手续费 2 元/手。',
        '合约 XM2703：开仓手续费 1 元/手，平今仓手续费 4 元/手，平昨仓手续费 1 元/手。']
ROW_QS = [('XM2702 平今多少钱一手？', 1), ('XM2703 合约平今仓的手续费是多少？', 2), ('XM2701 的开仓手续费是多少？', 0)]


def _row_scores():
    from rag.embed import Embedder, cosine
    e = Embedder().fit(ROWS + [c['text'] for c in para_chunks(base_docs())])
    vs = [e.encode(r) for r in ROWS]
    out = []
    for q, i in ROW_QS:
        qv = e.encode(q)
        s = [cosine(qv, v) for v in vs]
        out.append((q, i, s))
    return out


def show03():
    print('三行手续费只差合约代码。每个问题和三行的相似度：')
    for q, i, s in _row_scores():
        print(f'　　{q}　' + '　'.join(f'XM270{k + 1} {v:.3f}' for k, v in enumerate(s)))


def check03():
    items = []
    for q, i, s in _row_scores():
        gap = s[i] - max(v for k, v in enumerate(s) if k != i)
        items.append((gap >= 0.2, f'问“{q}”：XM270{i + 1} 那一行比另外两行至少高 0.2（现在高 {gap:.2f}）'))
    from rag.embed import Embedder, cosine
    e = Embedder().fit(['单个客户的投机持仓不得超过 3000 手。', '交易单位：5 吨/手。'])
    v = e.encode('交易单位：5 吨/手。')
    items.append((abs(cosine(v, v) - 1) < 1e-6, '向量仍然是单位长度：一段文字和自己的相似度是 1'))
    return items


# ---------------------------------------------------------------- 实操四　向量存储
def _store():
    from rag.embed import Embedder
    from rag.store import Store
    chunks = para_chunks(base_docs())
    st = Store(Embedder().fit([c['text'] for c in chunks]))
    st.add(chunks)
    return st


def show04():
    st = _store()
    q = 'XM2701 的开仓手续费是多少？'
    for name, f in (('不过滤', None), ('只留 12 月 30 日有效的公开文件', {'有效于': TODAY, '权限': ['公开']})):
        print(f'{name}，问“{q}”，前五块：')
        for h in st.search(q, n=5, filters=f):
            print(f"　　{h['id']}　{h['score']}　状态 {h['meta'].get('状态')}　{h['text'][-40:]}")


def check04():
    from rag.store import match
    M = meta()

    def f(day, perm=('公开',)):
        return {'有效于': day, '权限': list(perm)}
    items = [(match(M['第95号'], f(TODAY)) and not match(M['第88号'], f(TODAY)), '12 月 30 日：第95号有效；第88号 12 月 1 日起失效，不参与'),
             (not match(M['第102号'], f(TODAY)) and match(M['第102号'], f('2027-01-04')), '第102号 1 月 4 日生效：12 月 30 日不参与，1 月 4 日参与'),
             (not match(M['现行参数表'], f('2027-01-04')), '现行参数表 1 月 4 日失效：那一天起不参与'),
             (not match(M['运维手册'], f(TODAY)) and match(M['运维手册'], f(TODAY, ('公开', '内部'))), '运维手册是内部文件：会员看不到，员工看得到'),
             (match(M['第61号'], {'权限': ['公开']}) and match(M['第88号'], None), '不写“有效于”就不按日期过滤；filters 为空时什么都不过滤')]
    hits = _store().search('XM2701 的开仓手续费是多少？', n=10, filters=f(TODAY))
    items.append((bool(hits) and all(h['doc'] != '第88号' for h in hits) and any(h['doc'] == '第95号' for h in hits),
                  '带过滤条件检索：结果里没有第88号，有第95号'))
    return items


# ---------------------------------------------------------------- 实操五　检索前处理
PRE_QS = [('从 1 月 4 日起，XM2702 的一般持仓交易保证金比例是多少？', 'member'), ('XM2701 现在的涨跌停板幅度是多少？', 'member'),
          ('国庆期间 XM2610 合约的涨跌停板幅度调整到了多少？', 'member'), ('XM2702 平今多少钱一手？', 'member'),
          ('会员服务系统每周什么时候停机维护？', 'staff')]


def show05():
    from rag.pre import prepare
    for q, role in PRE_QS:
        r = prepare(q, role, TODAY)
        print(f'{q}（{role}）')
        print('　　' + '，'.join(f'{k}={v!r}' for k, v in r.items() if k not in ('question', 'where') and not callable(v)))


def check05():
    from rag.pre import prepare
    r = [prepare(q, role, TODAY) for q, role in PRE_QS]
    fl = [x.get('filters') or {} for x in r]
    return [(r[0]['as_of'] == '2027-01-04' and fl[0].get('有效于') == '2027-01-04', '“从 1 月 4 日起”：as_of 和过滤条件里的“有效于”都是 2027-01-04'),
            (r[1]['as_of'] == TODAY and fl[1].get('有效于') == TODAY, '“现在”：按今天 2026-12-30 过滤'),
            (r[2]['history'] is True and '有效于' not in fl[2], '问国庆期间：history 为 True，不按日期过滤'),
            (set(fl[0].get('权限', [])) == {'公开'} and '内部' in fl[4].get('权限', []), '会员只看公开文件；员工（staff）也能看内部文件'),
            ('平今仓' in r[3]['query'], '口语改写：“平今”扩展成文件里的“平今仓手续费”')]


# ---------------------------------------------------------------- 实操六　索引优化
IDX_QS = ['哪些通知从 1 月 4 日起生效？', '哪些通知已经失效了？']


def _index():
    from rag.embed import Embedder
    from rag.index import build_index
    from rag.store import Store
    docs = base_docs()
    chunks = para_chunks(docs)
    nodes = build_index(chunks, docs)
    st = Store(Embedder().fit([n['text'] for n in nodes]))
    st.add(nodes)
    return docs, chunks, nodes, st


def show06():
    docs, chunks, nodes, st = _index()
    s = next((n for n in nodes if n.get('kind') == '摘要' and n['doc'] == '第102号'), None)
    print('第102号的摘要节点：' + (s['text'] if s else '还没有'))
    for q in IDX_QS:
        print(f'\n问“{q}”，前五块：')
        for h in st.search(q, n=5):
            print(f"　　{h['id']}　{h['score']}　{h['text'][:56]}")


def check06():
    docs, chunks, nodes, st = _index()
    summ = {n['doc']: n['text'] for n in nodes if n.get('kind') == '摘要'}
    s = summ.get('第102号', '')
    d1 = {h['doc'] for h in st.search(IDX_QS[0], n=5)}
    d2 = {h['doc'] for h in st.search(IDX_QS[1], n=5)}
    return [(len(summ) == len(docs), f'每份文件一个摘要节点（现在 {len(summ)}/{len(docs)}）'),
            (len(nodes) - len(summ) == len(chunks), '原来的块一块不少'),
            (all(w in s for w in ('第102号', 'XM2701', '现行', '第103号')) and ('1 月 4 日' in s or '1月4日' in s),
             '第102号的摘要写了编号、合约、“1 月 4 日”生效、状态和更正关系'),
            ('第103号' in d1, f'问“{IDX_QS[0]}”：前五块里有第103号（它的正文没写哪天生效，只有元数据里有）'),
            ({'第61号', '第88号'} <= d2, f'问“{IDX_QS[1]}”：前五块里有第61号和第88号（正文里都没写“失效”）')]


# ---------------------------------------------------------------- 实操七　检索后处理
def _post_cases():
    from rag.post import postprocess
    M = meta()
    pc = para_chunks(base_docs())

    class FakeStore:
        def chunks_of(self, doc):
            return [dict(c) for c in pc if c['doc'] == doc]
    n = [0]

    def H(doc, text, score):
        n[0] += 1
        return {'id': f'{doc}#例{n[0]}', 'doc': doc, 'text': text, 'meta': M[doc], 'score': score}

    def R(q, role='member'):
        return {'question': q, 'query': q, 'role': role, 'as_of': TODAY, 'history': False, 'filters': None, 'where': None}
    fee = [H('第88号', '合约 XM2701：开仓手续费 5 元/手', 0.62), H('第95号', '合约 XM2701：开仓手续费 3 元/手', 0.61),
           H('会员问答', '答：以最近一次发布的手续费通知为准，被取代的旧通知不再适用。', 0.40)]
    fix = [H('第102号', '三、上述合约套期保值持仓交易保证金比例由 7% 调整为 9%。', 0.55),
           H('规则摘录', '4. 一般持仓和套期保值持仓分别适用各自的交易保证金比例。', 0.40)]
    inner = [H('运维手册', '三、测试环境的地址只在内部值班表中提供，不得对外发送。', 0.50),
             H('会员问答', '答：以当年发布的节假日交易安排通知为准。', 0.30)]
    rows = [H('第95号', '合约 XM2701：平今仓手续费 6 元/手', 0.50), H('第95号', '合约 XM2702：平今仓手续费 5 元/手', 0.49),
            H('第95号', '合约 XM2703：平今仓手续费 4 元/手', 0.48)]
    st = FakeStore()
    return {'fee': postprocess(fee, R('XM2701 的开仓手续费是多少？'), st),
            'fix': postprocess(fix, R('1 月 4 日起，套期保值持仓的保证金比例是多少？'), st),
            'member': postprocess(inner, R('测试环境的地址在哪里能查到？'), st),
            'staff': postprocess(inner, R('测试环境的地址在哪里能查到？', 'staff'), st),
            'rows': postprocess(rows, R('XM2703 平今仓手续费是多少？'), st)}


def show07():
    for k, hits in _post_cases().items():
        print(f'{k}：' + '、'.join(f"{h['doc']}「{h['text'][:22]}」" for h in hits))


def check07():
    from rag.config import TOP_K
    o = _post_cases()
    docs = {k: [h['doc'] for h in v] for k, v in o.items()}
    return [('第88号' not in docs['fee'] and '第95号' in docs['fee'], '新旧两份都在候选里：去掉被取代的第88号，留下第95号'),
            ('第103号' in docs['fix'], '第102号被更正过：把第103号的块一起交给响应生成'),
            ('运维手册' not in docs['member'] and '运维手册' in docs['staff'], '运维手册：会员提问时去掉，员工提问时保留'),
            (bool(o['rows']) and 'XM2703' in o['rows'][0]['text'], '问 XM2703：XM2703 那一块排第一'),
            (all(len(v) <= TOP_K for v in o.values()), f'每次最多留 TOP_K（{TOP_K}）块')]


# ---------------------------------------------------------------- 实操八　响应生成
def _gen_cases():
    from rag.generate import answer
    M = meta()

    def H(doc, text):
        return {'id': doc + '#例', 'doc': doc, 'text': text, 'meta': M[doc], 'score': 0.5}

    def R(q):
        return {'question': q, 'query': q, 'role': 'member', 'as_of': TODAY, 'history': False}
    return [('XM2702 明天会涨停吗？', answer(R('XM2702 明天会涨停吗？'), [H('现行参数表', '合约 XM2702：涨跌停板幅度 6%，一般持仓交易保证金比例 8%。')])),
            ('XM 合约的交割手续费是多少？', answer(R('XM 合约的交割手续费是多少？'), [
                H('第95号', '合约 XM2701：开仓手续费 3 元/手，平今仓手续费 6 元/手，平昨仓手续费 3 元/手。'),
                H('会员问答', '问：手续费标准以哪份通知为准？\n答：以最近一次发布的手续费通知为准，被取代的旧通知不再适用。')])),
            ('1 月 4 日起，XM2703 套期保值持仓的交易保证金比例是多少？', answer(R('1 月 4 日起，XM2703 套期保值持仓的交易保证金比例是多少？'), [
                H('第102号', '三、上述合约套期保值持仓交易保证金比例由 7% 调整为 9%。'),
                H('第103号', '第 102 号通知第三条中，套期保值持仓交易保证金比例“由 7% 调整为 9%”更正为“由 7% 调整为 8%”。第 102 号通知其余内容不变。')])),
            ('托管机柜每个月的收费标准是多少？', answer(R('托管机柜每个月的收费标准是多少？'), [
                H('技术服务收费标准', '为规范会员技术服务收费，现将收费标准公布如下，自 2026 年 10 月 1 日起执行。会员可以按需申请，费用按月结算。'),
                H('技术服务收费标准', '服务项目 托管机柜（每个）：收费标准 8000 元/月，说明 含电力与基础运维。')])),
            ('平今是什么意思？', answer(R('平今是什么意思？'), [
                H('会员问答', '问：平今是什么意思？\n答：平今指平掉当日新开的仓位，按手续费附表中的“平今仓手续费”收取；平掉以前交易日的持仓，按“平昨仓手续费”收取。')]))]


def show08():
    for q, a in _gen_cases():
        print(f'问：{q}\n　　' + a.replace('\n', '\n　　'))


def check08():
    a = [x[1] for x in _gen_cases()]
    return [('不能回答' in conclusion(a[0]) and not cites(a[0]), '问明天会不会涨停：拒答，不写依据'),
            ('不能回答' in conclusion(a[1]) and not cites(a[1]), '问交割手续费，资料里没有：拒答'),
            ('8%' in conclusion(a[2]) and {'第102号', '第103号'} <= cites(a[2]), '更正过的比例：结论用 8%，依据同时引第102号和第103号'),
            ('8000' in conclusion(a[3]), '问收费标准：挑带数值的那一句（8000 元/月）'),
            ('当日新开' in conclusion(a[4]) and '？' not in conclusion(a[4]), '问什么意思：结论用答句，不用问句')]


# ---------------------------------------------------------------- 实操九　系统评估
RA = {'Q1': ('时点', True), 'Q2': ('时点', True), 'Q3': ('表格', False), 'Q4': ('表格', False), 'Q5': ('拒答', True)}
RB = {'Q1': ('时点', False), 'Q2': ('时点', True), 'Q3': ('表格', True), 'Q4': ('表格', True), 'Q5': ('拒答', True)}


def _res(d):
    return {k: {'题型': t, '通过': ok, '检索': ok, '回答': ok, '原因': [] if ok else ['回答：结论里没有标准答案'], '问题': k}
            for k, (t, ok) in d.items()}


def show09():
    E = importlib.import_module('eval')
    E.report(E.run('public'))
    print('\n上面的“按题型”是这一次的结果。两次结果对比时，总分可能涨了，某一类题却退步了。')


def check09():
    E = importlib.import_module('eval')
    if not hasattr(E, 'compare_by_type'):
        return [(False, 'eval.py 里还没有 compare_by_type(ra, rb)'), (False, '--compare 还没有按题型列出变化')]
    r = dict(E.compare_by_type(_res(RA), _res(RB)))
    items = [(r.get('时点') == (2, 1, 2) and r.get('表格') == (0, 2, 2) and r.get('拒答') == (1, 1, 1),
              'compare_by_type 按题型数对：时点 2 → 1，表格 0 → 2，拒答 1 → 1')]
    res = ROOT / 'results'
    res.mkdir(exist_ok=True)
    a, b = res / '_检查前.json', res / '_检查后.json'
    a.write_text(json.dumps(_res(RA), ensure_ascii=False), encoding='utf-8')
    b.write_text(json.dumps(_res(RB), ensure_ascii=False), encoding='utf-8')
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            E.compare('_检查前', '_检查后')
    finally:
        a.unlink()
        b.unlink()
    lines = buf.getvalue().splitlines()
    items.append((any('时点' in ln and '退步' in ln for ln in lines) and not any('表格' in ln and '退步' in ln for ln in lines),
                  '--compare 按题型列出变化，退步的那一类标“退步”'))
    return items


# ---------------------------------------------------------------- 实操十　复杂 RAG 范式
def show10():
    from rag.agent import run
    from rag.pipeline import RAG
    ans, pool, trace = run(RAG(), Q_AMOUNT)
    print(f'问：{Q_AMOUNT}')
    for r, what, why, got in trace:
        print(f'　　第 {r} 轮　{why}：{what}\n　　　　拿到：' + ('、'.join(got) or '没有新的块'))
    print('　　' + ans.replace('\n', '\n　　'))


def check10():
    from rag.agent import missing, run
    from rag.pipeline import RAG
    from rag.pre import prepare
    M = meta()

    def H(doc, text):
        return {'id': doc + '#例', 'doc': doc, 'text': text, 'meta': M[doc], 'score': 0.5}
    q102 = H('第102号', '三、上述合约套期保值持仓交易保证金比例由 7% 调整为 9%。')
    q103 = H('第103号', '第 102 号通知第三条中，套期保值持仓交易保证金比例“由 7% 调整为 9%”更正为“由 7% 调整为 8%”。')
    full = [q102, q103, H('第99号', '一、交易单位：5 吨/手。'), H('规则摘录', '3. 交易保证金 = 结算价 × 交易单位 × 持仓手数 × 交易保证金比例。')]
    night = '12 月 31 日晚上有夜盘吗？'
    t1 = missing(Q_AMOUNT, [q102], prepare(Q_AMOUNT, 'member', TODAY))
    t2 = missing(Q_AMOUNT, [q102, q103], prepare(Q_AMOUNT, 'member', TODAY))
    t3 = missing(Q_AMOUNT, full, prepare(Q_AMOUNT, 'member', TODAY))
    t4 = missing(night, [H('第101号', '二、2026 年 12 月 31 日（星期四）为节前最后一个交易日，当晚不进行夜盘交易。')], prepare(night, 'member', TODAY))
    ans, pool, trace = run(RAG(), Q_AMOUNT)
    return [(any(t[0] == '文件' and t[1] == '第103号' for t in t1), '手里只有第102号：要去取更正它的第103号'),
            (sum(t[0] == '检索' for t in t2) >= 2, '金额题缺计算公式和交易单位：各检索一次'),
            (t3 == [] and t4 == [], '资料齐了就停；问夜盘这种一次就够的题，不再多查'),
            ({'第102号', '第103号', '第99号', '规则摘录'} <= cites(ans), '跑一遍金额题：依据里有第102号、第103号、第99号和规则摘录'),
            ('16000' in conclusion(ans), '结论是 20000 × 5 × 2 × 8% = 16000 元')]


# ----------------------------------------------------------------
def run_check(no):
    try:
        return globals()['check' + no]()
    except Exception as e:                 # 学员改出错时也要给出可读的提示
        return [(False, f'运行出错：{type(e).__name__}: {e}')]


def main():
    ap = argparse.ArgumentParser(description='十个实操的检查')
    ap.add_argument('no', nargs='?', help='实操编号，01—10')
    ap.add_argument('--看', dest='show', action='store_true', help='看这个实操要解决的现象')
    a = ap.parse_args()
    if not a.no:
        for no, name, f in CASES:
            items = run_check(no)
            print(f'实操{no}　{name}（{f}）　{sum(ok for ok, _ in items)}/{len(items)}')
        return
    no = a.no.zfill(2)
    name, f = next((n, p) for x, n, p in CASES if x == no)
    print(f'实操{no}　{name}　{f}\n')
    if a.show:
        globals()['show' + no]()
        return
    items = run_check(no)
    for ok, msg in items:
        print(f'  {OK if ok else NO} {msg}')
    n = sum(ok for ok, _ in items)
    print(f'\n{n}/{len(items)} 项通过' + ('。做完了，再跑 python eval.py 看看二十道题。' if n == len(items) else ''))


if __name__ == '__main__':
    main()
