"""组件九　系统评估：每改一处，用同一套题检查一遍。

    python eval.py                       跑全部公开题，打印每道题的结果和按题型的统计
    python eval.py --save 基线            同时把结果存成 results/基线.json
    python eval.py --compare 基线 改法一   对比两次存下的结果：哪些题改好了，哪些题改坏了
    python eval.py --show Q05             细看一道题：检索请求、交给响应生成的块、回答、哪一项没过

每道题查两项，两项都过才算通过：
    检索  标准文件都在交给响应生成的块里；不该用的文件一份都不在
    回答  结论里有标准答案；依据引用了标准文件，没有引用不该用的文件；该拒答的题拒答，不该拒答的题不拒答
"""
import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from rag.pipeline import RAG  # noqa: E402
from rag.utils import norm  # noqa: E402

SETS = {'public': ROOT / 'eval' / 'questions.jsonl', 'holdout': ROOT / 'eval' / 'holdout.jsonl'}
OK, NO = '√', '×'


def load_questions(name):
    path = SETS[name]
    if not path.exists():
        sys.exit(f'没有找到 {path.name}：留出题在讲师那里，最后统一跑。')
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def conclusion(ans):
    for line in ans.splitlines():
        if line.startswith('结论：'):
            return line[3:]
    return ''


def judge(q, ans, hits):
    docs = {h['doc'] for h in hits}
    cites = set(re.findall(r'〔(.+?)〕', ans))
    gold, bad = set(q.get('gold', [])), set(q.get('bad', []))
    concl = conclusion(ans)
    refused = '不能回答' in concl
    why = []
    if not gold <= docs:
        why.append('检索：少了 ' + '、'.join(sorted(gold - docs)))
    if bad & docs:
        why.append('检索：混进了 ' + '、'.join(sorted(bad & docs)))
    if q.get('refuse'):
        if not refused:
            why.append('回答：应该拒答')
        elif cites:
            why.append('回答：拒答时不写依据')
    else:
        if refused:
            why.append('回答：不该拒答')
        miss = [s for s in q.get('has', []) if norm(s) not in norm(concl)]
        if miss:
            why.append('回答：结论里没有 ' + '、'.join(miss))
        if not gold <= cites:
            why.append('回答：依据没引 ' + '、'.join(sorted(gold - cites)))
        if bad & cites:
            why.append('回答：依据引了 ' + '、'.join(sorted(bad & cites)))
    r_ok = not any(w.startswith('检索') for w in why)
    a_ok = not any(w.startswith('回答') for w in why)
    return {'检索': r_ok, '回答': a_ok, '通过': r_ok and a_ok, '原因': why}


def run(name):
    rag = RAG()
    out = OrderedDict()
    for q in load_questions(name):
        ans, hits, req = rag.ask(q['q'], q.get('role', 'member'))
        out[q['id']] = dict(judge(q, ans, hits), 题型=q['type'], 问题=q['q'], 答案=ans,
                            块=[f"{h['id']}（{h.get('score', 0)}）" for h in hits])
    return out


def report(res):
    print(f'{"题号":<5}{"题型":<6}检索 回答 通过  问题')
    for k, r in res.items():
        marks = '  '.join(OK if r[x] else NO for x in ('检索', '回答', '通过'))
        print(f'{k:<6}{r["题型"]:<6}{marks}   {r["问题"]}')
    n = len(res)
    tot = {x: sum(r[x] for r in res.values()) for x in ('检索', '回答', '通过')}
    print(f'\n通过 {tot["通过"]}/{n}　　检索 {tot["检索"]}/{n}　　回答 {tot["回答"]}/{n}')
    types = OrderedDict()
    for r in res.values():
        types.setdefault(r['题型'], []).append(r['通过'])
    print('按题型：' + '，'.join(f'{t} {sum(v)}/{len(v)}' for t, v in types.items()))


def show(res, qid):
    rag = RAG()
    q = next(x for x in load_questions('public') if x['id'] == qid)
    ans, hits, req = rag.ask(q['q'], q.get('role', 'member'))
    print('问题：', q['q'], f'（提问人：{q.get("role", "member")}）')
    print('请求：', {k: v for k, v in req.items() if not callable(v)})
    print('交给响应生成的块：')
    for h in hits:
        print(f"  {h['id']}　相似度 {h.get('score', 0)}　{h['text'][:70].replace(chr(10), ' ')}")
    print('回答：')
    print('  ' + ans.replace('\n', '\n  '))
    print('标准：', {k: q[k] for k in ('gold', 'bad', 'has', 'refuse') if k in q})
    print('结果：', '通过' if res[qid]['通过'] else '；'.join(res[qid]['原因']))


def compare(a, b):
    ra = json.loads((ROOT / 'results' / f'{a}.json').read_text(encoding='utf-8'))
    rb = json.loads((ROOT / 'results' / f'{b}.json').read_text(encoding='utf-8'))
    up = [k for k in rb if rb[k]['通过'] and not ra.get(k, {}).get('通过')]
    down = [k for k in rb if not rb[k]['通过'] and ra.get(k, {}).get('通过')]
    na, nb = sum(r['通过'] for r in ra.values()), sum(r['通过'] for r in rb.values())
    print(f'{a} 通过 {na}　→　{b} 通过 {nb}')
    print('改好了：', '、'.join(f'{k} {rb[k]["题型"]}' for k in up) or '无')
    print('改坏了：', '、'.join(f'{k} {rb[k]["题型"]}' for k in down) or '无')
    for k in down:
        print(f'  {k}：', '；'.join(rb[k]['原因']))


def main():
    ap = argparse.ArgumentParser(description='系统评估')
    ap.add_argument('--save')
    ap.add_argument('--compare', nargs=2)
    ap.add_argument('--show')
    ap.add_argument('--set', default='public', choices=list(SETS))
    ap.add_argument('--json', action='store_true', help='只输出 JSON（讲师合并评测用）')
    a = ap.parse_args()
    if a.compare:
        return compare(*a.compare)
    res = run(a.set)
    if a.json:
        print(json.dumps(res, ensure_ascii=False))
        return
    if a.show:
        return show(res, a.show)
    report(res)
    for k, r in res.items():
        if not r['通过']:
            print(f'  {k}：' + '；'.join(r['原因']))
    if a.save:
        (ROOT / 'results').mkdir(exist_ok=True)
        (ROOT / 'results' / f'{a.save}.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'已存：results/{a.save}.json')


if __name__ == '__main__':
    main()
