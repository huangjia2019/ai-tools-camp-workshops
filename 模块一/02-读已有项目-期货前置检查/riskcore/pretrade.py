"""下单前检查：价格是否为最小变动价位整数倍、是否在涨跌停板内、开仓保证金是否够。"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .calendar import prev_trading_day, trading_day_of
from .data import dec
from .margin import required_margin
from .market import settle_price
from .params import lookup, spec
from .price_limit import is_tick_multiple, limit_prices


@dataclass
class Order:
    account: str
    contract: str
    side: str            # buy / sell
    offset: str          # open / close
    price: Decimal
    lots: int
    ts: datetime
    hedge: bool = False


def check(order: Order, available: Decimal) -> list:
    """返回问题清单，空表示通过。"""
    problems = []
    if order.lots <= 0:
        problems.append('手数必须为正整数')
    day = trading_day_of(order.ts)
    s = spec(order.contract)
    tick = dec(s['tick'])
    p = lookup(order.contract, day)
    if not is_tick_multiple(order.price, tick):
        problems.append(f'价格 {order.price} 不是最小变动价位 {tick} 的整数倍')
    upper, lower = limit_prices(settle_price(order.contract, prev_trading_day(day)), p.limit_pct, tick)
    if not lower <= order.price <= upper:
        problems.append(f'价格 {order.price} 超出 {day} 的涨跌停板 [{lower}, {upper}]')
    if order.offset == 'open':
        ratio = p.margin_hedge if order.hedge else p.margin_general
        need = required_margin(order.price, order.lots, s['multiplier'], ratio)
        if need > available:
            problems.append(f'可用资金 {available} 不足，开仓需保证金 {need}')
    return problems
