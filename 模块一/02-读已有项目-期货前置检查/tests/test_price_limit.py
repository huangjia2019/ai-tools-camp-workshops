import unittest
from decimal import Decimal as D

from riskcore.price_limit import is_tick_multiple, limit_prices


class LimitPriceTest(unittest.TestCase):
    def test_eight_percent(self):
        # 78350 × 1.08 = 84618，向下取到 10 的整数倍；78350 × 0.92 = 72082，向上取整
        self.assertEqual(limit_prices(D('78350'), D('0.08'), D('10')), (D('84610'), D('72090')))

    def test_nine_percent(self):
        # 78350 × 1.09 = 85401.5，78350 × 0.91 = 71298.5
        self.assertEqual(limit_prices(D('78350'), D('0.09'), D('10')), (D('85400'), D('71300')))

    def test_exact_multiple_is_kept(self):
        self.assertEqual(limit_prices(D('80000'), D('0.08'), D('10')), (D('86400'), D('73600')))

    def test_tick_multiple(self):
        self.assertTrue(is_tick_multiple(D('78350'), D('10')))
        self.assertFalse(is_tick_multiple(D('78355'), D('10')))


if __name__ == '__main__':
    unittest.main()
