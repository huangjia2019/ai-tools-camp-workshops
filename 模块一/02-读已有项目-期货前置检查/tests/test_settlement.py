import unittest
from datetime import date
from decimal import Decimal as D

from riskcore.settlement import settle


class SettlementTest(unittest.TestCase):
    def test_june_30(self):
        r = settle(date(2026, 6, 30))
        # A1001：CU2608 多 4 手，(78280 − 78180) × 5 × 4 = 2000；保证金 78280 × 5 × 4 × 10%
        self.assertEqual((r['A1001']['pnl'], r['A1001']['margin']), (D('2000'), D('156560.00')))
        # A1002：CU2607 空 2 手，交割月前一月阶段 10%
        self.assertEqual((r['A1002']['pnl'], r['A1002']['margin']), (D('-1000'), D('78200.00')))
        # A2001：套保持仓 9%
        self.assertEqual(r['A2001']['margin'], D('211356.00'))
        self.assertFalse(any(row['margin_call'] for row in r.values()))


if __name__ == '__main__':
    unittest.main()
