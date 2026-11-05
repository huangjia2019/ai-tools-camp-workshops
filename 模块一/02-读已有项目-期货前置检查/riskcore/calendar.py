"""交易日与夜盘归属。

国内期货的一个交易日从前一个工作日的夜盘开始，到当日 15:00 收盘为止。
夜盘（含 20:55 起的集合竞价）属于下一个交易日。
"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta

from .data import load

HOLIDAYS = frozenset(date.fromisoformat(d) for d in load('calendar.json')['holidays'])


def is_trading_day(d: date) -> bool:
    return d.weekday() < 5 and d not in HOLIDAYS


def next_trading_day(d: date) -> date:
    n = d + timedelta(days=1)
    while not is_trading_day(n):
        n += timedelta(days=1)
    return n


def prev_trading_day(d: date) -> date:
    p = d - timedelta(days=1)
    while not is_trading_day(p):
        p -= timedelta(days=1)
    return p


def first_trading_day_on_or_after(d: date) -> date:
    return d if is_trading_day(d) else next_trading_day(d)


def trading_day_of(ts: datetime) -> date:
    """一笔委托属于哪个交易日。不在交易时段的时间点抛 ValueError。"""
    t = ts.time()
    if t >= time(20, 55):
        return next_trading_day(ts.date())
    if t <= time(2, 30):
        return next_trading_day(ts.date() - timedelta(days=1))
    if time(8, 55) <= t <= time(15, 0) and is_trading_day(ts.date()):
        return ts.date()
    raise ValueError(f'{ts:%Y-%m-%d %H:%M} 不在交易时段')
