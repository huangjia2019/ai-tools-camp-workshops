"""期货数据 MCP 服务（stdio，只用标准库）。

给 Agent 四个只读工具：合约规格、某交易日的参数、涨跌停价、结算价。
启动：python3 mcp/futures_mcp_server.py（由 TRAE、WorkBuddy、Claude Code 等客户端拉起，不需要手动运行）。
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from riskcore.calendar import prev_trading_day  # noqa: E402
from riskcore.data import dec  # noqa: E402
from riskcore.market import settle_price  # noqa: E402
from riskcore.params import lookup, spec  # noqa: E402
from riskcore.price_limit import limit_prices  # noqa: E402

SERVER = {'name': 'futures-lab', 'version': '0.1.0'}
CONTRACT = {'type': 'string', 'description': '合约代码，例如 CU2608'}
DAY = {'type': 'string', 'description': '交易日，YYYY-MM-DD'}
TOOLS = [
    {'name': 'get_contract', 'description': '查合约规格：交易单位、最小变动价位、最低保证金、上市运行各阶段的保证金标准。',
     'inputSchema': {'type': 'object', 'properties': {'contract': CONTRACT}, 'required': ['contract']}},
    {'name': 'get_params', 'description': '查某合约在某交易日生效的涨跌停板幅度与交易保证金比例，并给出依据的通知编号。',
     'inputSchema': {'type': 'object', 'properties': {'contract': CONTRACT, 'trading_day': DAY,
                                                      'for_settlement': {'type': 'boolean', 'description': '是否用于当日结算'}},
                     'required': ['contract', 'trading_day']}},
    {'name': 'get_limit_prices', 'description': '查某合约在某交易日的涨停价与跌停价（按上一交易日结算价计算）。',
     'inputSchema': {'type': 'object', 'properties': {'contract': CONTRACT, 'trading_day': DAY}, 'required': ['contract', 'trading_day']}},
    {'name': 'get_settle_price', 'description': '查某合约某交易日的结算价。',
     'inputSchema': {'type': 'object', 'properties': {'contract': CONTRACT, 'trading_day': DAY}, 'required': ['contract', 'trading_day']}},
]


def call(name: str, args: dict) -> dict:
    c = args['contract']
    if name == 'get_contract':
        return dict(spec(c), contract=c)
    day = date.fromisoformat(args['trading_day'])
    if name == 'get_params':
        p = lookup(c, day, bool(args.get('for_settlement')))
        return {'contract': c, 'trading_day': day.isoformat(), 'limit_pct': str(p.limit_pct), 'margin_general': str(p.margin_general),
                'margin_hedge': str(p.margin_hedge), 'notice_id': p.notice_id, 'stage': p.stage}
    if name == 'get_limit_prices':
        p = lookup(c, day)
        prev = prev_trading_day(day)
        upper, lower = limit_prices(settle_price(c, prev), p.limit_pct, dec(spec(c)['tick']))
        return {'contract': c, 'trading_day': day.isoformat(), 'prev_settle_day': prev.isoformat(),
                'upper': str(upper), 'lower': str(lower), 'limit_pct': str(p.limit_pct), 'notice_id': p.notice_id}
    if name == 'get_settle_price':
        return {'contract': c, 'trading_day': day.isoformat(), 'settle_price': str(settle_price(c, day))}
    raise KeyError(name)


def handle(msg: dict):
    method, mid = msg.get('method'), msg.get('id')
    if mid is None:                       # 通知，不回
        return None
    if method == 'initialize':
        version = (msg.get('params') or {}).get('protocolVersion', '2025-06-18')
        result = {'protocolVersion': version, 'capabilities': {'tools': {}}, 'serverInfo': SERVER}
    elif method == 'ping':
        result = {}
    elif method == 'tools/list':
        result = {'tools': TOOLS}
    elif method == 'tools/call':
        params = msg.get('params') or {}
        try:
            data = call(params.get('name'), params.get('arguments') or {})
            result = {'content': [{'type': 'text', 'text': json.dumps(data, ensure_ascii=False)}], 'isError': False}
        except Exception as e:            # 工具错误按 MCP 约定放进结果，让模型看得到
            result = {'content': [{'type': 'text', 'text': f'{type(e).__name__}: {e}'}], 'isError': True}
    else:
        return {'jsonrpc': '2.0', 'id': mid, 'error': {'code': -32601, 'message': f'未知方法 {method}'}}
    return {'jsonrpc': '2.0', 'id': mid, 'result': result}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        reply = handle(json.loads(line))
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + '\n')
            sys.stdout.flush()


if __name__ == '__main__':
    main()
