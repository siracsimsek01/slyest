from src.app.core.symbolic_to_decimal import toggle_format
import unittest
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.app.core.symbolic_to_decimal import toggle_format

class TestSymbolicToDecimal(unittest.TestCase):

    def test_fraction_to_decimal(self):
     
        result, success = toggle_format("1/2")
        self.assertTrue(success)
        self.assertEqual(result, "0.5")

    def test_decimal_to_fraction(self):
        
        result, success = toggle_format("0.5")
        self.assertTrue(success)
        self.assertEqual(result, "1/2")

    def test_calculator_symbols(self):
        
        result, success = toggle_format("10 ÷ 4")
        self.assertTrue(success)
        self.assertEqual(result, "2.5")

    def test_tolerance_fix(self):
       
        original_fraction = "39/461"
        
       
        decimal_val, success1 = toggle_format(original_fraction)
        self.assertTrue(success1)
        
        
        final_fraction, success2 = toggle_format(decimal_val)
        self.assertTrue(success2)
        
        
        self.assertEqual(final_fraction, "39/461")

    def test_pi_conversion(self):
       
        result, success = toggle_format("pi")
        self.assertTrue(success)
        self.assertTrue(result.startswith("3.14"))

    def test_invalid_input(self):
        
        result, success = toggle_format("hello world")
        self.assertFalse(success)
        self.assertTrue(result.startswith("Error"))

if __name__ == '__main__':
    unittest.main()