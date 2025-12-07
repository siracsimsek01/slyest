import unittest
from src.app.core.symbolic_engine import differentiate
from sympy import simplify, sympify

class TestDifferentiation(unittest.TestCase):

    def assertSymbolicEqual(self, result, expected):
        result_simplified = simplify(result)
        expected_simplified = simplify(sympify(expected))
        self.assertTrue(simplify(result_simplified - expected_simplified) == 0, 
                       f"Expected {expected_simplified} but got {result_simplified}")

    def test_polynomials_and_trig(self):
        self.assertSymbolicEqual(differentiate("x**2 + cos(x)", "x"), "2*x - sin(x)")
        self.assertSymbolicEqual(differentiate("x**3 + 2*x + sin(x)", "x"), "3*x**2 + 2 + cos(x)")
    
    def test_polynomials_and_exponentials(self):
        self.assertSymbolicEqual(differentiate("x**2 + exp(x)", "x"), "2*x + exp(x)")
        self.assertSymbolicEqual(differentiate("3*x**3 + exp(x)", "x"), "9*x**2 + exp(x)")
    
    def test_trig_and_exponentials(self):
        self.assertSymbolicEqual(differentiate("sin(x) * exp(x)", "x"), "exp(x)*cos(x) + exp(x)*sin(x)")
        self.assertSymbolicEqual(differentiate("cos(x) * exp(x)", "x"), "exp(x)*(-sin(x)) + exp(x)*cos(x)")
    
    def test_rational_and_trig(self):
        result = differentiate("tan(x)/x", "x")
        expected = sympify("sec(x)**2/x - tan(x)/x**2")
        self.assertTrue(simplify(result - expected) == 0)
    
    def test_multiple_trig_terms(self):
        self.assertSymbolicEqual(differentiate("sin(x) + cos(x) + tan(x)", "x"), "cos(x) - sin(x) + sec(x)**2")
    
    def test_product_of_functions(self):
        self.assertSymbolicEqual(differentiate("x**2 * sin(x)", "x"), "2*x*sin(x) + x**2*cos(x)")
    
    def test_composite_function(self):
        self.assertSymbolicEqual(differentiate("sin(x**2)", "x"), "2*x*cos(x**2)")

    def test_invalid_variable(self):
        with self.assertRaises(ValueError):
            differentiate("x**2 + cos(x)", "xyz")

    def test_constant(self):
        self.assertSymbolicEqual(differentiate("5", "x"), "0")
    
if __name__ == "__main__":
    unittest.main()