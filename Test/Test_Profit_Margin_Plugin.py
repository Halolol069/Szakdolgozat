import unittest

from Controller.plugins.profit_margin_plugin import calculate_margin, calculate_reverse_margin

class TestProfitMarginPlugin(unittest.TestCase):

    def test_calculate_normal_values(self):
        sell_price, profit = calculate_margin(1000.0, 20.0)
        self.assertAlmostEqual(sell_price, 1200.0)
        self.assertAlmostEqual(profit, 200.0)

    def test_calculate_margin_zero_margin(self):
        sell_price, profit = calculate_margin(5000.0, 0.0)
        self.assertAlmostEqual(sell_price, 5000.0)
        self.assertAlmostEqual(profit, 0.0)

    def test_calculate_high_margin(self):
        sell_price, profit = calculate_margin(2000.0, 150.0)
        self.assertAlmostEqual(sell_price, 5000.0)
        self.assertAlmostEqual(profit, 3000.0)

    def test_calculate_reverse_margin_normal(self):
        margin_percent, profit = calculate_reverse_margin(1000.0, 1200.0)
        self.assertAlmostEqual(margin_percent, 20.0)
        self.assertAlmostEqual(profit, 200.0)

    def test_calculate_reverse_margin_loss(self):
        margin_percent, profit = calculate_reverse_margin(1000.0, 800.0)
        self.assertAlmostEqual(margin_percent, -20.0)
        self.assertAlmostEqual(profit, -200.0)

    def test_calculate_reverse_margin_zero_net(self):
        margin_percent, profit = calculate_reverse_margin(0.0, 1000.0)
        self.assertAlmostEqual(margin_percent, 0.0)
        self.assertAlmostEqual(profit, 1000.0)

if __name__ == '__main__':
    unittest.main()