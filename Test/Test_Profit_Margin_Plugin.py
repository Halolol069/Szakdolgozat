import unittest

from Controller.plugins.profit_margin_plugin import calculate_margin


class TestProfitMarginPlugin(unittest.TestCase):

    def test_calculate_normal_values(self):

        sell_price, profit = calculate_margin(1000.0, 20.0)
        self.assertEqual(sell_price, 1200.0)
        self.assertEqual(profit, 200.0)

    def test_calculate_margin_zero_margin(self):
        sell_price, profit = calculate_margin(5000.0, 0.0)
        self.assertEqual(sell_price, 5000.0)
        self.assertEqual(profit, 0.0)

    def test_calculate_high_margin(self):
        sell_price, profit = calculate_margin(2000.0, 150.0)
        self.assertEqual(sell_price, 5000.0)
        self.assertEqual(profit, 3000.0)

if __name__ == '__main__':
    unittest.main()
