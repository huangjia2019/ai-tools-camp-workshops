"""每日无负债结算（简化版）：只算隔夜持仓的当日盈亏与持仓保证金，不处理当日开平仓。"""
from __future__ import annotations

from datetime import date

from .calendar import prev_trading_day
from .data import dec, load
from .margin import required_margin
from .market import settle_price
from .params import lookup, spec


def settle(day: date, accounts: dict = None, positions: list = None) -> dict:
    book = load('accounts.json')
    accounts = accounts if accounts is not None else book['accounts']
    positions = positions if positions is not None else book['positions']
    out = {a: {'balance': dec(v['balance']), 'pnl': dec(0), 'margin': dec(0)} for a, v in accounts.items()}
    for pos in positions:
        s = spec(pos['contract'])
        today, before = settle_price(pos['contract'], day), settle_price(pos['contract'], prev_trading_day(day))
        net = pos['long'] - pos['short']
        p = lookup(pos['contract'], day, for_settlement=True)
        ratio = p.margin_hedge if pos.get('hedge') else p.margin_general
        row = out[pos['account']]
        row['pnl'] += (today - before) * s['multiplier'] * net
        row['margin'] += required_margin(today, pos['long'] + pos['short'], s['multiplier'], ratio)
    for row in out.values():
        row['equity'] = row['balance'] + row['pnl']
        row['available'] = row['equity'] - row['margin']
        row['margin_call'] = row['available'] < 0
    return out
