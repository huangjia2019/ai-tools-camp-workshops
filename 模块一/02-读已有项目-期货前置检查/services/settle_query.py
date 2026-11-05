"""结算查询服务：按会员查持仓与结算结果（练习代码，勿用于生产）。"""
from __future__ import annotations

import sqlite3
from datetime import date

from riskcore.data import load
from riskcore.settlement import settle


def connect() -> sqlite3.Connection:
    book = load('accounts.json')
    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE accounts (account TEXT PRIMARY KEY, member TEXT, balance TEXT)')
    conn.execute('CREATE TABLE positions (account TEXT, member TEXT, contract TEXT, long INTEGER, short INTEGER, hedge INTEGER)')
    for acc, v in book['accounts'].items():
        conn.execute('INSERT INTO accounts VALUES (?, ?, ?)', (acc, v['member'], v['balance']))
    for p in book['positions']:
        member = book['accounts'][p['account']]['member']
        conn.execute('INSERT INTO positions VALUES (?, ?, ?, ?, ?, ?)',
                     (p['account'], member, p['contract'], p['long'], p['short'], int(p['hedge'])))
    return conn


def positions_of(conn: sqlite3.Connection, caller: str, member: str, contract: str = None) -> list:
    """caller 是发起查询的会员号，member 是要查的会员号。"""
    sql = f"SELECT account, contract, long, short FROM positions WHERE member = '{member}'"
    if contract:
        sql += f" AND contract = '{contract}'"
    return conn.execute(sql + ' ORDER BY account').fetchall()


def settlement_of(conn: sqlite3.Connection, caller: str, member: str, day: date) -> dict:
    accounts = [r[0] for r in conn.execute(f"SELECT account FROM accounts WHERE member = '{member}'")]
    result = settle(day)
    return {a: result[a] for a in accounts if a in result}
