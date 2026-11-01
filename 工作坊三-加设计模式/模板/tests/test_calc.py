"""calc.py 的测试。在 模板/ 目录下运行：python3 -m unittest discover -s tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import calc  # noqa: E402


class LimitTest(unittest.TestCase):
    def test_round_both_ways(self):
        self.assertEqual(calc.limit_prices(23450, 7, 5), (25090, 21810))

    def test_exact_multiple(self):
        self.assertEqual(calc.limit_prices(20000, 5, 5), (21000, 19000))

    def test_another_contract(self):
        self.assertEqual(calc.limit_prices(23515, 7, 5), (25160, 21870))

    def test_bad_input(self):
        for args in [(0, 7, 5), (23450, 7, 0), (23450, 0, 5), (23450, 100, 5)]:
            with self.assertRaises(ValueError):
                calc.limit_prices(*args)


class MarginTest(unittest.TestCase):
    def test_general(self):
        self.assertEqual(calc.margin(23450, 5, 2, 9), '21105.00')

    def test_round_to_cent(self):
        self.assertEqual(calc.margin(23415, 5, 3, 7.5), '26341.88')


class DataTest(unittest.TestCase):
    def test_previous_trading_day_skips_holiday(self):
        self.assertEqual(calc.previous_trading_day('2027-01-04'), '2026-12-31')

    def test_settlement_prices_on_tick(self):
        ticks = {r['合约']: int(r['最小变动价位(元/吨)']) for r in calc.read_csv(calc.ROOT / 'data/参数表.csv')}
        for r in calc.read_csv(calc.ROOT / 'data/结算价.csv'):
            self.assertEqual(int(r['结算价(元/吨)']) % ticks[r['合约']], 0, r)

    def test_params_files_pass_verify(self):
        for name in ('sim/params.csv', 'prod/params.csv'):
            self.assertEqual(calc.verify(calc.ROOT / name), [], name)


if __name__ == '__main__':
    unittest.main()
