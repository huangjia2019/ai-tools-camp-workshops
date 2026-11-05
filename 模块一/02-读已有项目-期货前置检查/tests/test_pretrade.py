import unittest
from datetime import datetime
from decimal import Decimal as D

from riskcore.pretrade import Order, check


def order(price, lots=1, ts=datetime(2026, 6, 15, 10, 0), offset='open'):
    return Order(account='A1001', contract='CU2608', side='buy', offset=offset, price=D(price), lots=lots, ts=ts)


class PreTradeTest(unittest.TestCase):
    # 2026-06-15 的上一交易日是 06-12，CU2608 结算价 77900，幅度 8%：涨停 84130，跌停 71670

    def test_at_upper_limit_passes(self):
        self.assertEqual(check(order('84130'), D('50000')), [])

    def test_one_tick_above_upper_limit_is_rejected(self):
        self.assertEqual(len(check(order('84140'), D('50000'))), 1)

    def test_at_lower_limit_passes(self):
        self.assertEqual(check(order('71670'), D('50000')), [])

    def test_not_a_tick_multiple(self):
        self.assertIn('不是最小变动价位', check(order('78355'), D('50000'))[0])

    def test_margin_not_enough(self):
        # 78000 × 5 吨 × 2 手 × 10% = 78000
        self.assertIn('可用资金', check(order('78000', lots=2), D('77999.99'))[0])
        self.assertEqual(check(order('78000', lots=2), D('78000')), [])

    def test_close_needs_no_margin(self):
        self.assertEqual(check(order('78000', lots=2, offset='close'), D('0')), [])

    def test_friday_night_order_uses_monday_limits(self):
        self.assertEqual(check(order('84130', ts=datetime(2026, 6, 12, 21, 30)), D('50000')), [])


if __name__ == '__main__':
    unittest.main()
