"""合约参数：涨跌停板幅度与交易保证金比例。

参数来自两处：
1. data/contracts.json：合约规格与上市运行不同阶段的保证金标准（风控办法第五条）；
2. data/notices.json：交易所历次调整通知，每条带生效时点。
一般持仓同时适用两种以上保证金比例时取最高值（风控办法第八条）。
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from .calendar import first_trading_day_on_or_after, prev_trading_day
from .data import dec, load

CONTRACTS = {k: v for k, v in load('contracts.json').items() if not k.startswith('_')}
NOTICES = load('notices.json')['notices']


@dataclass(frozen=True)
class Params:
    contract: str
    trading_day: date
    limit_pct: object
    margin_general: object
    margin_hedge: object
    notice_id: str
    stage: str


def split(contract: str) -> tuple:
    m = re.fullmatch(r'([A-Za-z]+)(\d{4})', contract)
    if not m:
        raise ValueError(f'合约代码格式不对：{contract}')
    return m.group(1).upper(), m.group(2)


def spec(contract: str) -> dict:
    return CONTRACTS[split(contract)[0]]


def delivery_month(contract: str) -> date:
    yymm = split(contract)[1]
    return date(2000 + int(yymm[:2]), int(yymm[2:]), 1)


def last_trading_day(contract: str) -> date:
    m = delivery_month(contract)
    return first_trading_day_on_or_after(date(m.year, m.month, 15))


def stage_of(contract: str, d: date) -> str:
    """合约在 d 这个交易日处于上市运行的哪个阶段（风控办法第五条表一）。"""
    m = delivery_month(contract)
    before = date(m.year - 1, 12, 1) if m.month == 1 else date(m.year, m.month - 1, 1)
    if d >= prev_trading_day(prev_trading_day(last_trading_day(contract))):
        return 'last2'
    if d >= first_trading_day_on_or_after(m):
        return 'delivery'
    if d >= first_trading_day_on_or_after(before):
        return 'pre_delivery'
    return 'listing'


def _covers(change: dict, contract: str) -> bool:
    span = change.get('contracts')
    if not span:
        return True
    lo, hi = (split(c)[1] for c in span)
    return lo <= split(contract)[1] <= hi


def current_notice(contract: str, trading_day: date, for_settlement: bool = False) -> dict:
    product = split(contract)[0]
    hits = [n for n in NOTICES
            if product in n['changes'] and _covers(n['changes'][product], contract)
            and date.fromisoformat(n['effective_after_settlement_of']) < trading_day]
    if not hits:
        raise LookupError(f'{contract} 在 {trading_day} 没有生效中的参数')
    return max(hits, key=lambda n: n['effective_after_settlement_of'])


def lookup(contract: str, trading_day: date, for_settlement: bool = False) -> Params:
    s = spec(contract)
    notice = current_notice(contract, trading_day, for_settlement)
    change = notice['changes'][split(contract)[0]]
    stage = stage_of(contract, trading_day)
    general = max(dec(change['margin_general']), dec(s['stage_margin'][stage]), dec(s['min_margin']))
    return Params(contract=contract, trading_day=trading_day, limit_pct=dec(change['limit_pct']),
                  margin_general=general, margin_hedge=dec(change['margin_hedge']),
                  notice_id=notice['id'], stage=stage)
