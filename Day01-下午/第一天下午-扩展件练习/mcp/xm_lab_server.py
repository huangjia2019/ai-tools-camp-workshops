"""练习用的 MCP 服务 xm-lab：查练习金属 XM 的合约规格、某一天的参数、涨跌停价和已录入的通知。

只用 Python 标准库（3.8 以上），只读，不联网。TRAE 按 stdio 方式启动它，配置见同目录的 配置示例.json。
数据在同目录的 xm_data.json；inbox/ 里的新通知还没有录进去，这个服务看不到。

    python xm_lab_server.py --selftest      不接 TRAE，自己跑一遍四个工具
"""
import json
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / 'xm_data.json').read_text(encoding='utf-8'))
PROTOCOL = '2025-06-18'

TOOLS = [
    {'name': 'contract_spec', 'description': '查一个合约的规格：交易单位、最小变动价位、最后交易日。',
     'inputSchema': {'type': 'object', 'properties': {'contract': {'type': 'string', 'description': '合约代码，例如 XM2701'}},
                     'required': ['contract']}},
    {'name': 'params_on', 'description': '查一个合约在某一天适用的涨跌停板幅度和交易保证金比例，以及依据。',
     'inputSchema': {'type': 'object', 'properties': {'contract': {'type': 'string', 'description': '合约代码，例如 XM2702'},
                                                      'date': {'type': 'string', 'description': '日期，YYYY-MM-DD'}},
                     'required': ['contract', 'date']}},
    {'name': 'limit_prices', 'description': '按某一天的涨跌停板幅度计算涨停价和跌停价：涨停价向下、跌停价向上取到最小变动价位的整数倍。',
     'inputSchema': {'type': 'object', 'properties': {'contract': {'type': 'string'}, 'date': {'type': 'string', 'description': 'YYYY-MM-DD'},
                                                      'settle_price': {'type': 'number', 'description': '上一交易日结算价，元/吨'}},
                     'required': ['contract', 'date', 'settle_price']}},
    {'name': 'list_notices', 'description': '列出已经录入数据的通知，以及数据更新到哪一天。',
     'inputSchema': {'type': 'object', 'properties': {}}},
]


def _contract(code):
    code = str(code).strip().upper().replace(' ', '')
    if code not in DATA['合约']:
        raise ValueError(f'没有这个合约：{code}。可查的合约：' + '、'.join(DATA['合约']))
    return code


def params_on(contract, date):
    code = _contract(contract)
    rows = [r for r in DATA['参数'] if code in r['合约'] and r['起用日期'] <= date]
    if not rows:
        raise ValueError(f'{date} 之前没有 {code} 的参数记录')
    r = max(rows, key=lambda x: x['起用日期'])
    return {'合约': code, '日期': date, '涨跌停板幅度': r['涨跌停板幅度'], '一般持仓保证金': r['一般持仓保证金'],
            '套期保值保证金': r['套期保值保证金'], '起用日期': r['起用日期'], '依据': r['依据'], '数据更新到': DATA['数据更新到']}


def limit_prices(contract, date, settle_price):
    p = params_on(contract, date)
    tick = Decimal(str(DATA['合约'][p['合约']]['最小变动价位']))
    rate = Decimal(p['涨跌停板幅度'].rstrip('%')) / 100
    price = Decimal(str(settle_price))
    if price <= 0:
        raise ValueError('结算价必须是正数')
    up = (price * (1 + rate) / tick).to_integral_value(ROUND_FLOOR) * tick
    down = (price * (1 - rate) / tick).to_integral_value(ROUND_CEILING) * tick
    return {'合约': p['合约'], '日期': date, '结算价': str(price), '涨跌停板幅度': p['涨跌停板幅度'], '最小变动价位': str(tick),
            '涨停价': str(up), '跌停价': str(down), '依据': p['依据'] + '；涨停价向下、跌停价向上取整'}


def call(name, args):
    if name == 'contract_spec':
        code = _contract(args.get('contract', ''))
        return dict(DATA['合约'][code], 合约=code)
    if name == 'params_on':
        return params_on(args.get('contract', ''), args.get('date', ''))
    if name == 'limit_prices':
        return limit_prices(args.get('contract', ''), args.get('date', ''), args.get('settle_price', 0))
    if name == 'list_notices':
        return {'已录入的通知': DATA['通知'], '数据更新到': DATA['数据更新到']}
    raise ValueError(f'没有这个工具：{name}')


def handle(msg):
    """处理一条 JSON-RPC 消息；通知（没有 id）不回复。"""
    mid, method, params = msg.get('id'), msg.get('method'), msg.get('params') or {}
    if mid is None:
        return None
    if method == 'initialize':
        result = {'protocolVersion': params.get('protocolVersion') or PROTOCOL, 'capabilities': {'tools': {'listChanged': False}},
                  'serverInfo': {'name': 'xm-lab', 'version': '1.0.0'},
                  'instructions': '练习交易所 XM 合约的只读数据。数据只到 xm_data.json 里的“数据更新到”那一天，之后发布的通知查不到。'}
    elif method == 'ping':
        result = {}
    elif method == 'tools/list':
        result = {'tools': TOOLS}
    elif method == 'tools/call':
        try:
            out = call(params.get('name'), params.get('arguments') or {})
            result = {'content': [{'type': 'text', 'text': json.dumps(out, ensure_ascii=False)}], 'isError': False}
        except (ValueError, TypeError, ArithmeticError) as e:
            result = {'content': [{'type': 'text', 'text': f'出错：{e}'}], 'isError': True}
    else:
        return {'jsonrpc': '2.0', 'id': mid, 'error': {'code': -32601, 'message': f'不支持的方法：{method}'}}
    return {'jsonrpc': '2.0', 'id': mid, 'result': result}


def serve():
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            reply = handle(json.loads(line))
        except json.JSONDecodeError:
            reply = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': '不是合法的 JSON'}}
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + '\n')
            sys.stdout.flush()


def selftest():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    for name, args in [('list_notices', {}), ('contract_spec', {'contract': 'XM2702'}),
                       ('params_on', {'contract': 'XM2702', 'date': '2027-01-05'}),
                       ('limit_prices', {'contract': 'XM2702', 'date': '2027-01-05', 'settle_price': 20000})]:
        print(name, json.dumps(call(name, args), ensure_ascii=False))


if __name__ == '__main__':
    selftest() if '--selftest' in sys.argv else serve()
