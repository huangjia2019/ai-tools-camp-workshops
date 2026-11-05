import json
import subprocess
import sys
import unittest
from pathlib import Path

from services.settle_query import connect, positions_of

ROOT = Path(__file__).resolve().parent.parent


class SettleQueryTest(unittest.TestCase):
    def test_member_positions(self):
        rows = positions_of(connect(), 'M001', 'M001')
        self.assertEqual(rows, [('A1001', 'CU2608', 4, 0), ('A1002', 'CU2607', 0, 2)])


class McpServerTest(unittest.TestCase):
    def test_initialize_list_and_call(self):
        msgs = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 't', 'version': '0'}}},
            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'get_limit_prices', 'arguments': {'contract': 'CU2608', 'trading_day': '2026-06-15'}}},
        ]
        out = subprocess.run([sys.executable, str(ROOT / 'mcp/futures_mcp_server.py')], input='\n'.join(json.dumps(m) for m in msgs) + '\n',
                             capture_output=True, text=True, timeout=20, check=True).stdout.splitlines()
        replies = [json.loads(x) for x in out]
        self.assertEqual([r['id'] for r in replies], [1, 2, 3])
        self.assertEqual(len(replies[1]['result']['tools']), 4)
        data = json.loads(replies[2]['result']['content'][0]['text'])
        self.assertEqual((data['upper'], data['lower']), ('84130', '71670'))


if __name__ == '__main__':
    unittest.main()
