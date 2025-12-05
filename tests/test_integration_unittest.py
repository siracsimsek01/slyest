import unittest
from symbolic_engine import integrate
from symbolic_engine import simplify  # optional

class TestIntegration(unittest.TestCase):

    def assertSymbolicEqual(self, result, expected):
        try:
            simplified = simplify(f"({result}) - ({expected})")
            self.assertEqual(simplified, "0")
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

    def test_constant_of_integration(self):
        result = integrate("x", "x")
        self.assertTrue("C" in result or "c" in result or result == "x^2/2")

if __name__ == "__main__":
    unittest.main()
