"""现成的小工具：读文件头、分句、算重合、找合约代码、换算日期。各组都可以直接用，不算在任何一个组件里。"""
import re
from datetime import date, timedelta

PUNCT = re.compile(r'[\s，。、；：？！?,.;:“”‘’（）()《》〔〕\[\]|*#>\-—｜/]')
CODE = re.compile(r'XM\s*(\d{4})', re.I)


def parse_front_matter(text):
    """文件开头两行 --- 之间是元数据，每行“键: 值”。返回 (元数据字典, 正文)。"""
    meta, body = {}, text
    if text.startswith('---'):
        head, _, body = text[3:].partition('\n---')
        for line in head.strip().splitlines():
            k, _, v = line.partition(':')
            if k.strip():
                meta[k.strip()] = v.strip()
    return meta, body.strip()


def split_sentences(text):
    """按行、按句号分号切成句子；“｜”也当作断开处（块前面加了标题时，标题单独算一句）。
    表格的分隔行和引用行（> 开头）去掉。"""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('>') or set(line) <= set('|-: '):
            continue
        for s in re.split(r'(?<=[。；！？｜])', line):
            s = s.rstrip('｜')
            s = s.strip()
            if s:
                out.append(s)
    return out


def bigrams(text):
    t = PUNCT.sub('', text).lower()
    return {t[i:i + 2] for i in range(len(t) - 1)}


def overlap(a, b):
    """两段文字共有多少个不同的二字片段。"""
    return len(bigrams(a) & bigrams(b))


def contract_codes(text):
    """找出文字里的合约代码，统一写成 XM2701 这样。"""
    return sorted({'XM' + m for m in CODE.findall(text)})


def contract_month(code):
    """XM2610 → '2026-10'（合约到期的年月）。"""
    d = code[-4:]
    return f'20{d[:2]}-{d[2:]}'


def parse_date(text, today):
    """把问题里的日期换算成 'YYYY-MM-DD'；没写日期返回 None。

    认得：今天、现在、目前、当前、明天、后天、昨天，以及“2027 年 1 月 4 日”“1 月 4 日”。
    没写年份时，取离 today 最近的那一年（12 月底问“1 月 4 日”，指的是下一年）。
    """
    t0 = date.fromisoformat(today)
    if re.search(r'今天|现在|目前|当前', text):
        return today
    for word, k in (('明天', 1), ('后天', 2), ('昨天', -1)):
        if word in text:
            return (t0 + timedelta(days=k)).isoformat()
    m = re.search(r'(?:(\d{4})\s*年\s*)?(\d{1,2})\s*月\s*(\d{1,2})\s*日', text)
    if not m:
        return None
    y, mo, d = m.groups()
    if y:
        return date(int(y), int(mo), int(d)).isoformat()
    cands = [date(t0.year + k, int(mo), int(d)) for k in (-1, 0, 1)]
    return min(cands, key=lambda x: abs((x - t0).days)).isoformat()


def norm(text):
    """去掉空白，方便比较“5 元/手”和“5元/手”。"""
    return re.sub(r'\s+', '', text)
