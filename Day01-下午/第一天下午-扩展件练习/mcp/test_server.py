"""不接 TRAE，用 MCP 的 stdio 协议和 xm_lab_server.py 对话一遍：握手、列工具、调工具。

    python test_server.py
"""
import json
import subprocess
import sys
from pathlib import Path

srv = subprocess.Popen([sys.executable, str(Path(__file__).resolve().parent / 'xm_lab_server.py')],
                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8')


def send(msg, reply=True):
    srv.stdin.write(json.dumps(msg, ensure_ascii=False) + '\n')
    srv.stdin.flush()
    return json.loads(srv.stdout.readline()) if reply else None


r = send({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
          'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'test', 'version': '0'}}})
print('握手：', r['result']['serverInfo'], r['result']['protocolVersion'])
send({'jsonrpc': '2.0', 'method': 'notifications/initialized'}, reply=False)
tools = send({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'})['result']['tools']
print('工具：', '、'.join(t['name'] for t in tools))
r = send({'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call',
          'params': {'name': 'limit_prices', 'arguments': {'contract': 'XM2702', 'date': '2027-01-05', 'settle_price': 20000}}})
print('调用：', r['result']['content'][0]['text'])
r = send({'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call', 'params': {'name': 'params_on', 'arguments': {'contract': 'XM9999', 'date': '2027-01-05'}}})
print('出错时：', r['result']['isError'], r['result']['content'][0]['text'])
srv.stdin.close()
srv.wait(timeout=5)
print('通过' if len(tools) == 4 else '不通过')
