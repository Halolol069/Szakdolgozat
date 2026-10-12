import unittest

from Controller.plugins.unit_plugin import calculate_mm

class Test_Unit_Plugin(unittest.TestCase):
    def test_calculate_normal_value(self):
        mm = calculate_mm(1.0)
        self.assertEqual(mm, 25.4)

    def test_calculate_zero(self):
        mm = calculate_mm(0.0)
        self.assertEqual(mm, 0.0)

    def test_calculate_large_value(self):
        mm = calculate_mm(10.0)
        self.assertEqual(mm, 254.0)

    def test_calculate_fractional_value(self):
        mm=calculate_mm(1.5)
        self.assertAlmostEqual(mm, 38.1)

if __name__ == '__main__':
    unittest.main()