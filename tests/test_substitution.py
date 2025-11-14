import unittest
import sys
import os



from src.app.core.perform_substitution import perform_substitution

class TestSubstitution(unittest.TestCase):

    def test_simple_numeric(self):
        self.assertEqual(perform_substitution("x + 1", {'x': 5}), ("6", True))

    def test_symbolic_substitution(self):
        self.assertEqual(perform_substitution("x + y", {'x': 'a + 1'}), ("a + y + 1", True))

    def test_multiple_substitutions(self):
        self.assertEqual(perform_substitution("x**2 + y", {'x': 3, 'y': 1}), ("10", True))

    def test_partial_substitution(self):
        self.assertEqual(perform_substitution("x + y + z", {'x': 1, 'z': 2}), ("y + 3", True))

    def test_no_substitution(self):
        self.assertEqual(perform_substitution("x + y", {'z': 5}), ("x + y", True))

    def test_avoids_substring_replacement(self):
        self.assertEqual(perform_substitution("max_value + x", {'x': 5}), ("max_value + 5", True))

    def test_correct_parentheses(self):
        self.assertEqual(perform_substitution("c * x", {'x': 'a + b'}), ("c*(a + b)", True))

    
    def test_invalid_expression(self):
  
        expected = ("-2", True) 
        self.assertEqual(perform_substitution("2*+ - x", {'x': 1}), expected)

    
    def test_invalid_substitution_value(self):
      
        expected = ("a + b + 1", True) 
        self.assertEqual(perform_substitution("x + 1", {'x': 'a++b'}), expected)

    def test_invalid_variable_name(self):
        expected = ("Error: Invalid variable name '1x'.", False)
        self.assertEqual(perform_substitution("x + 1", {'1x': 5}), expected)

    def test_empty_expression(self):
        expected = ("Error: No expression provided.", False)
        self.assertEqual(perform_substitution("", {'x': 1}), expected)
        
    def test_whitespace_expression(self):
        expected = ("Error: No expression provided.", False)
        self.assertEqual(perform_substitution("   ", {'x': 1}), expected)

    def test_invalid_subs_dict_type(self):
        expected = ("Error: Invalid substitution format.", False)
        self.assertEqual(perform_substitution("x + 1", [{'x': 1}]), expected)


if __name__ == '__main__':
    unittest.main()