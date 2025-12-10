import unittest
from symbolic_engine import integrate, simplify

class TestIntegration(unittest.TestCase):

    def assertSymbolicEqual(self, result, expected):
        
        try:
            diff = simplify(f"({result}) - ({expected})")
            self.assertEqual(diff, "0")
        except Exception:
           
            self.assertEqual(
                result.replace(" ", ""), 
                expected.replace(" ", "")
            )

    def test_basic_polynomials(self):
        self.assertSymbolicEqual(integrate("x", "x"), "x^2/2")
        self.assertSymbolicEqual(integrate("2*x", "x"), "x^2")
        self.assertSymbolicEqual(integrate("x^2", "x"), "x^3/3")

    def test_trigonometric(self):
        self.assertSymbolicEqual(integrate("sin(x)", "x"), "-cos(x)")
        self.assertSymbolicEqual(integrate("cos(x)", "x"), "sin(x)")

    def test_exponential(self):
        self.assertSymbolicEqual(integrate("exp(x)", "x"), "exp(x)")

    def test_rational(self):
        self.assertSymbolicEqual(integrate("1/x", "x"), "ln(x)")

    def test_constant(self):
        self.assertSymbolicEqual(integrate("5", "x"), "5*x")

    def test_zero(self):
        self.assertSymbolicEqual(integrate("0", "x"), "C")  # or "0" depending on your design

    def test_wrong_variable(self):
        # ∫ x dy = x*y
        self.assertSymbolicEqual(integrate("x", "y"), "x*y")

    def test_product(self):
        # ∫ x*sin(x) dx = -x*cos(x) + sin(x)
        self.assertSymbolicEqual(
            integrate("x*sin(x)", "x"),
            "-x*cos(x) + sin(x)"
        )

    def test_constant_of_integration(self):
        result = integrate("x", "x")
        self.assertTrue("C" in result or "c" in result or result == "x^2/2")


if __name__ == "__main__":
    unittest.main()
