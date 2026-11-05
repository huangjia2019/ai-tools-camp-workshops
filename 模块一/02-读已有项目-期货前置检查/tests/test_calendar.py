import unittest
from datetime import date, datetime

from riskcore.calendar import is_trading_day, next_trading_day, trading_day_of


class TradingDayTest(unittest.TestCase):
    def test_day_session_is_same_day(self):
        self.assertEqual(trading_day_of(datetime(2026, 6, 15, 10, 0)), date(2026, 6, 15))

    def test_thursday_night_belongs_to_friday(self):
        self.assertEqual(trading_day_of(datetime(2026, 6, 11, 21, 30)), date(2026, 6, 12))

    def test_friday_night_belongs_to_monday(self):
        self.assertEqual(trading_day_of(datetime(2026, 6, 12, 21, 30)), date(2026, 6, 15))

    def test_after_midnight_belongs_to_next_trading_day(self):
        self.assertEqual(trading_day_of(datetime(2026, 6, 13, 0, 30)), date(2026, 6, 15))

    def test_call_auction_counts_as_night_session(self):
        self.assertEqual(trading_day_of(datetime(2026, 6, 11, 20, 55)), date(2026, 6, 12))

    def test_outside_trading_hours(self):
        with self.assertRaises(ValueError):
            trading_day_of(datetime(2026, 6, 15, 16, 0))

    def test_holiday_is_skipped(self):
        self.assertFalse(is_trading_day(date(2026, 6, 19)))
        self.assertEqual(next_trading_day(date(2026, 6, 18)), date(2026, 6, 22))


if __name__ == '__main__':
    unittest.main()
