"""涨跌停板价格。

涨停板价格 = 上一交易日结算价 ×（1 + 涨跌停板幅度），跌停板价格 = 上一交易日结算价 ×（1 − 幅度）。
计算结果不是最小变动价位整数倍时，涨停价向下取整、跌停价向上取整，保证不超出幅度。
取整方向待对照《上海期货交易所交易细则》确认，见 docs/待确认.md。
"""
from __future__ import annotations

from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal


def limit_prices(prev_settle: Decimal, pct: Decimal, tick: Decimal) -> tuple:
    up = prev_settle * (1 + pct) / tick
    down = prev_settle * (1 - pct) / tick
    return up.to_integral_value(rounding=ROUND_FLOOR) * tick, down.to_integral_value(rounding=ROUND_CEILING) * tick


def is_tick_multiple(price: Decimal, tick: Decimal) -> bool:
    q = price / tick
    return q == q.to_integral_value()
