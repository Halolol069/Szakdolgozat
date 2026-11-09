import unittest

from Controller.plugins.currency_plugin import calculate_huf, calculate_dynamic_huf


class Test_Currency(unittest.TestCase):

    def test_calculate_dynamic_rate(self):
        huf = calculate_dynamic_huf(10.0, 400.0)
        self.assertEqual(huf, 4000.0)

    def test_calculate_normal_value(self):
        huf = calculate_huf(10.0)
        self.assertEqual(huf, 3950.0)

    def test_calculate_zero(self):
        huf = calculate_huf(0.0)
        self.assertEqual(huf, 0.0)

    def test_calculate_fractional_value(self):
        huf = calculate_huf(1.5)
        self.assertAlmostEqual(huf, 592.5, places=1)

if __name__ == '__main__':
    unittest.main()