"""交易保证金 = 价格 × 交易单位 × 手数 × 保证金比例，按分四舍五入。"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal('0.01')


def required_margin(price: Decimal, lots: int, multiplier: int, ratio: Decimal) -> Decimal:
    return (price * multiplier * lots * ratio).quantize(CENT, rounding=ROUND_HALF_UP)
