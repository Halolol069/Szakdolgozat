import unittest

from Controller.plugins.unit_plugin import (
    calculate_mm, calculate_inch,
    calculate_liter, calculate_gallon,
    calculate_bar, calculate_psi,
    calculate_kw, calculate_hp,
    calculate_nm, calculate_lbft
)


class Test_Unit_Plugin(unittest.TestCase):
    def test_calculate_normal_value(self):
        mm = calculate_mm(1.0)
        self.assertEqual(mm, 25.4)

    def test_calculate_zero(self):
        mm = calculate_mm(0.0)
        self.assertEqual(mm, 0.0)

    def test_calculate_fractional_value(self):
        mm = calculate_mm(1.5)
        self.assertAlmostEqual(mm, 38.1)

    def test_calculate_inch(self):
        self.assertAlmostEqual(calculate_inch(25.4), 1.0)
        self.assertEqual(calculate_inch(0.0), 0.0)

    def test_calculate_liter(self):
        self.assertAlmostEqual(calculate_liter(1.0), 3.78541)
        self.assertEqual(calculate_liter(0.0), 0.0)

    def test_calculate_gallon(self):
        self.assertAlmostEqual(calculate_gallon(3.78541), 1.0)
        self.assertEqual(calculate_gallon(0.0), 0.0)

    def test_calculate_bar(self):
        self.assertAlmostEqual(calculate_bar(10.0), 0.689476)
        self.assertEqual(calculate_bar(0.0), 0.0)

    def test_calculate_psi(self):
        self.assertAlmostEqual(calculate_psi(0.689476), 10.0)
        self.assertEqual(calculate_psi(0.0), 0.0)

    def test_calculate_kw(self):
        self.assertAlmostEqual(calculate_kw(100.0), 73.5499)
        self.assertEqual(calculate_kw(0.0), 0.0)

    def test_calculate_hp(self):
        self.assertAlmostEqual(calculate_hp(73.5499), 100.0)
        self.assertEqual(calculate_hp(0.0), 0.0)

    def test_calculate_nm(self):
        self.assertAlmostEqual(calculate_nm(10.0), 13.558)
        self.assertEqual(calculate_nm(0.0), 0.0)

    def test_calculate_lbft(self):
        self.assertAlmostEqual(calculate_lbft(13.558), 10.0)
        self.assertEqual(calculate_lbft(0.0), 0.0)
if __name__ == '__main__':
    unittest.main()