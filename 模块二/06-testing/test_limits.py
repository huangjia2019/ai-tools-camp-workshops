import unittest

from limits import limits


class LimitsTests(unittest.TestCase):
    def test_exact_tick(self):
        self.assertEqual(limits(20000, 0.07, 5), (21400, 18600))


if __name__ == '__main__':
    unittest.main()
