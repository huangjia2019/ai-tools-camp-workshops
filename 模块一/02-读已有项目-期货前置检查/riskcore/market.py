"""结算价查询。"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from .data import dec, load

_PRICES = {k: v for k, v in load('settle_prices.json').items() if not k.startswith('_')}


def settle_price(contract: str, day: date) -> Decimal:
    try:
        return dec(_PRICES[contract][day.isoformat()])
    except KeyError:
        raise LookupError(f'没有 {contract} 在 {day} 的结算价') from None
