"""计算脚本：涨跌停价、交易保证金、参数文件核对。

在 模板/ 目录下运行（Windows 把 python3 换成 python）：
    python3 scripts/calc.py limit --base 23450 --pct 7 --tick 5
    python3 scripts/calc.py margin --price 23450 --unit 5 --lots 2 --ratio 9
    python3 scripts/calc.py day --date 2027-01-04 --pct 7
    python3 scripts/calc.py verify sim/params.csv
"""
import argparse
import csv
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    """读 CSV，跳过以 # 开头的说明行。"""
    with open(path, encoding='utf-8') as f:
        lines = [line for line in f if line.strip() and not line.startswith('#')]
    return list(csv.DictReader(lines))


def _num(x):
    return int(x) if x.denominator == 1 else float(x)


def limit_prices(base, pct, tick):
    """涨停价 = 基准价 ×（1 + 幅度），向下取到最小变动价位；跌停价 = 基准价 ×（1 − 幅度），向上取。幅度是百分数。"""
    base, pct, tick = Fraction(str(base)), Fraction(str(pct)), Fraction(str(tick))
    if base <= 0:
        raise ValueError('基准价必须大于 0')
    if tick <= 0:
        raise ValueError('最小变动价位必须大于 0')
    if not 0 < pct < 100:
        raise ValueError('涨跌停板幅度是百分数，应在 0 到 100 之间')
    up = base * (100 + pct) / 100
    down = base * (100 - pct) / 100
    return _num((up // tick) * tick), _num(-((-down) // tick) * tick)


def margin(price, unit, lots, ratio):
    """交易保证金 = 价格 × 交易单位 × 手数 × 保证金比例（百分数），四舍五入到分。"""
    v = Fraction(str(price)) * Fraction(str(unit)) * Fraction(str(lots)) * Fraction(str(ratio)) / 100
    if v < 0:
        raise ValueError('输入不能是负数')
    cents = (v * 100 + Fraction(1, 2)) // 1
    return f'{cents // 100}.{cents % 100:02d}'


def calendar():
    return read_csv(ROOT / 'data/交易日历.csv')


def previous_trading_day(date):
    days = sorted(r['日期'] for r in calendar() if r['是否交易日'] == '是')
    before = [d for d in days if d < date]
    if not before:
        raise ValueError(f'交易日历里找不到 {date} 之前的交易日')
    return before[-1]


def day(date, pct):
    """某个交易日三个合约的涨跌停价：基准是上一交易日的结算价。"""
    base_day = previous_trading_day(date)
    ticks = {r['合约']: r['最小变动价位(元/吨)'] for r in read_csv(ROOT / 'data/参数表.csv')}
    rows = []
    for r in read_csv(ROOT / 'data/结算价.csv'):
        if r['交易日'] == base_day:
            up, down = limit_prices(r['结算价(元/吨)'], pct, ticks[r['合约']])
            rows.append((r['合约'], r['结算价(元/吨)'], up, down))
    return base_day, rows


def verify(path):
    """核对参数文件：合约在参数表里，比例是 0 到 100 之间的百分数，日历范围内的起用日期是交易日。"""
    path = Path(path)
    if not path.exists():
        path = ROOT / path
    known = {r['合约'] for r in read_csv(ROOT / 'data/参数表.csv')}
    cal = {r['日期']: r for r in calendar()}
    lo, hi = min(cal), max(cal)
    rows = read_csv(path)
    problems = [] if rows else ['文件里没有数据行']
    for i, r in enumerate(rows, 1):
        if r.get('合约') not in known:
            problems.append(f'第 {i} 行：合约 {r.get("合约")} 不在参数表里')
        for col in ('涨跌停板幅度', '一般持仓保证金比例', '套保持仓保证金比例'):
            v = (r.get(col) or '').strip()
            m = re.fullmatch(r'(\d+(?:\.\d+)?)%', v)
            if not m or not 0 < float(m[1]) < 100:
                problems.append(f'第 {i} 行：{col}“{v}”不是 0 到 100 之间的百分数')
        d = (r.get('起用日期') or '').strip()
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d):
            problems.append(f'第 {i} 行：起用日期“{d}”格式应为 YYYY-MM-DD')
        elif lo <= d <= hi and cal.get(d, {}).get('是否交易日') != '是':
            problems.append(f'第 {i} 行：起用日期 {d} 不是交易日')
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description='涨跌停价、交易保证金与参数文件核对')
    sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('limit', help='涨跌停价')
    a.add_argument('--base', required=True, help='基准价（上一交易日结算价）')
    a.add_argument('--pct', required=True, help='涨跌停板幅度，百分数，如 7')
    a.add_argument('--tick', required=True, help='最小变动价位')
    b = sub.add_parser('margin', help='交易保证金')
    b.add_argument('--price', required=True)
    b.add_argument('--unit', required=True, help='交易单位，吨/手')
    b.add_argument('--lots', required=True, help='手数')
    b.add_argument('--ratio', required=True, help='保证金比例，百分数，如 9')
    c = sub.add_parser('day', help='某个交易日三个合约的涨跌停价')
    c.add_argument('--date', required=True, help='交易日，如 2027-01-04')
    c.add_argument('--pct', required=True, help='涨跌停板幅度，百分数')
    v = sub.add_parser('verify', help='核对参数文件')
    v.add_argument('path')
    args = ap.parse_args(argv)
    if args.cmd == 'limit':
        up, down = limit_prices(args.base, args.pct, args.tick)
        print(f'涨停价 {up}　跌停价 {down}')
    elif args.cmd == 'margin':
        print(f'交易保证金 {margin(args.price, args.unit, args.lots, args.ratio)}')
    elif args.cmd == 'day':
        base_day, rows = day(args.date, args.pct)
        print(f'{args.date} 的涨跌停价（基准：{base_day} 结算价；幅度 {args.pct}%）')
        print('合约 | 基准结算价 | 涨停价 | 跌停价')
        for row in rows:
            print(' | '.join(str(x) for x in row))
    else:
        problems = verify(args.path)
        if problems:
            print('不通过：')
            for p in problems:
                print('- ' + p)
            return 1
        print('通过')
    return 0


if __name__ == '__main__':
    sys.exit(main())
