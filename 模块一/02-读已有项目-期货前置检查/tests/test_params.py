import unittest
from datetime import date
from decimal import Decimal as D

from riskcore.params import last_trading_day, lookup, stage_of


class ParamsTest(unittest.TestCase):
    def test_cu2608_in_june(self):
        p = lookup('CU2608', date(2026, 6, 15))
        self.assertEqual((p.limit_pct, p.margin_general, p.margin_hedge), (D('0.08'), D('0.10'), D('0.09')))
        self.assertEqual(p.stage, 'listing')

    def test_cu_limit_pct_is_8_percent(self):
        self.assertEqual(lookup('CU2608', date(2026, 7, 3)).limit_pct, D('0.08'))

    def test_stages_of_cu2607(self):
        self.assertEqual(stage_of('CU2607', date(2026, 5, 29)), 'listing')
        self.assertEqual(stage_of('CU2607', date(2026, 6, 1)), 'pre_delivery')
        self.assertEqual(stage_of('CU2607', date(2026, 7, 1)), 'delivery')
        self.assertEqual(last_trading_day('CU2607'), date(2026, 7, 15))
        self.assertEqual(stage_of('CU2607', date(2026, 7, 13)), 'last2')

    def test_highest_ratio_applies_in_delivery_month(self):
        # 风控办法第八条：同时适用两种以上比例时取最高值。交割月阶段 15% 高于通知的 10%
        self.assertEqual(lookup('CU2607', date(2026, 7, 1)).margin_general, D('0.15'))


if __name__ == '__main__':
    unittest.main()
