import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'app'))

from src.app.core.plotter import ExpressionPlotter
from matplotlib.figure import Figure


class TestExpressionPlotter(unittest.TestCase):
    
    def setUp(self):
        self.plotter = ExpressionPlotter()
    
    def test_creates_simple_plot(self):
        figure = self.plotter.create_plot("x**2")
        self.assertIsInstance(figure, Figure)
    
    def test_plots_with_custom_range(self):
        figure = self.plotter.create_plot("x**2", x_range=(-5, 5))
        self.assertIsInstance(figure, Figure)
    
    def test_plots_trig_function(self):
        figure = self.plotter.create_plot("sin(x)")
        self.assertIsInstance(figure, Figure)
    
    def test_substitutes_variables(self):
        self.plotter.set_variables({'a': 'x+1'})
        figure = self.plotter.create_plot("a**2")
        self.assertIsInstance(figure, Figure)
    
    def test_creates_parametric_plot(self):
        figure = self.plotter.create_parametric_plot("cos(t)", "sin(t)")
        self.assertIsInstance(figure, Figure)
    
    def test_creates_multi_plot(self):
        figure = self.plotter.create_multi_plot(["x**2", "x**3"])
        self.assertIsInstance(figure, Figure)
    
    def test_handles_invalid_expression(self):
        with self.assertRaises(ValueError):
            self.plotter.create_plot("invalid@@expression")
    
    def test_plots_with_custom_variable(self):
        figure = self.plotter.create_plot("t**2", variable='t')
        self.assertIsInstance(figure, Figure)
    
    def test_multi_plot_with_labels(self):
        figure = self.plotter.create_multi_plot(
            ["x**2", "x**3"],
            labels=["Quadratic", "Cubic"]
        )
        self.assertIsInstance(figure, Figure)
    
    def test_parametric_with_custom_range(self):
        figure = self.plotter.create_parametric_plot(
            "t**2", "t**3",
            param_range=(-2, 2)
        )
        self.assertIsInstance(figure, Figure)


if __name__ == '__main__':
    unittest.main()