import sys
import types
import unittest

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

# Import the code under test
from src.app.ui.plotting_panel import (
    PlottingPanel,
    MultipleExpressionDialog,
    ParametricPlotDialog,
    PolarPlotDialog,
    ThreeDPlotDialog,
    ImplicitPlotDialog,
)


app = QApplication.instance() or QApplication(sys.argv)


class DummyEngine:
    def __init__(self):
        self._vars = {"a": "x+1"}

    def list_variables(self):
        return self._vars


class DummyWindowManager:
    def __init__(self):
        self.last_call = None

    def create_plot_window(self, parent, figure, title):
        self.last_call = (parent, figure, title)


class DummyPlotter:
    def __init__(self):
        self.variables = None
        self.last_call = None

    def set_variables(self, variables_dict):
        self.variables = variables_dict

    def create_plot(self, expr, variable="x", x_range=(-10, 10), num_points=1000):
        self.last_call = ("create_plot", expr, variable, x_range, num_points)
        return object()

    def create_multi_plot(self, expressions, variable="x", x_range=(-10, 10), num_points=1000):
        self.last_call = ("create_multi_plot", expressions, variable, x_range, num_points)
        return object()

    def create_parametric_plot(self, x_expr, y_expr, parameter="t", param_range=(0.0, 1.0)):
        self.last_call = ("create_parametric_plot", x_expr, y_expr, parameter, param_range)
        return object()

    def create_polar_plot(self, r_expr, parameter="theta", angle_range=(0.0, 1.0)):
        self.last_call = ("create_polar_plot", r_expr, parameter, angle_range)
        return object()

    def create_surface_plot(self, expr, x_range, y_range):
        self.last_call = ("create_surface_plot", expr, x_range, y_range)
        return object()

    def create_3d_parametric_plot(self, x_expr, y_expr, z_expr, parameter="t", param_range=(0.0, 1.0)):
        self.last_call = ("create_3d_parametric_plot", x_expr, y_expr, z_expr, parameter, param_range)
        return object()

    def create_implicit_plot(self, expr, x_range, y_range):
        self.last_call = ("create_implicit_plot", expr, x_range, y_range)
        return object()


class DummyApp:
    def __init__(self):
        self.engine = DummyEngine()
        self._current_expr = "x**2"

    def get_current_expression(self):
        return self._current_expr


class TestPlottingPanel(unittest.TestCase):
    def setUp(self):
        self.app_ref = DummyApp()
        self.panel = PlottingPanel(self.app_ref)
        self.panel.plotter = DummyPlotter()
        self.panel.window_manager = DummyWindowManager()

    def test_current_plot_parameters_defaults(self):
        params = self.panel.current_plot_parameters()
        self.assertEqual(params["x_min"], -10.0)
        self.assertEqual(params["x_max"], 10.0)
        self.assertEqual(params["variable"], "x")
        self.assertEqual(params["points"], 1000)

    def test_update_variables_sets_plotter(self):
        self.panel.update_variables({"a": "x+1"})
        self.assertEqual(self.panel.plotter.variables, {"a": "x+1"})

    def test_sync_variables_uses_app_engine(self):
        self.panel._sync_variables()
        self.assertEqual(self.panel.plotter.variables, {"a": "x+1"})

    def test_plot_single_uses_plotter_and_window_manager(self):
        self.app_ref._current_expr = "x**3"
        self.panel.plot_single()
        self.assertIsNotNone(self.panel.plotter.last_call)
        self.assertIsNotNone(self.panel.window_manager.last_call)
        kind, expr, var, x_range, n = self.panel.plotter.last_call
        self.assertEqual(kind, "create_plot")
        self.assertEqual(expr, "x**3")

    def test_plot_single_with_empty_expression_shows_warning(self):
        self.app_ref._current_expr = ""
        original = QMessageBox.warning

        calls = []

        def fake_warning(*args, **kwargs):
            calls.append((args, kwargs))

        QMessageBox.warning = fake_warning
        try:
            self.panel.plot_single()
        finally:
            QMessageBox.warning = original

        self.assertTrue(calls)

    def test_plot_single_invalid_range_shows_error(self):
        self.panel.x_min_input.setText("not_a_number")
        original = QMessageBox.critical
        calls = []

        def fake_critical(*args, **kwargs):
            calls.append((args, kwargs))

        QMessageBox.critical = fake_critical
        try:
            self.panel.plot_single()
        finally:
            QMessageBox.critical = original

        self.assertTrue(calls)

    def test_get_expression_uses_app_method_if_available(self):
        self.app_ref._current_expr = "sin(x)"
        expr = self.panel._get_expression()
        self.assertEqual(expr, "sin(x)")


class TestMultipleExpressionDialog(unittest.TestCase):
    def setUp(self):
        self.plotter = DummyPlotter()
        self.manager = DummyWindowManager()
        self.parent = PlottingPanel(DummyApp())
        self.parent.plotter = self.plotter
        self.parent.window_manager = self.manager

        def get_parameters():
            return {"x_min": -1.0, "x_max": 1.0, "variable": "x", "points": 100}

        self.dialog = MultipleExpressionDialog(self.parent, self.plotter, self.manager, get_parameters)

    def test_execute_plot_parses_lines(self):
        self.dialog.text_input.setPlainText("x**2\n\nsin(x)\n  x**3  ")
        result = self.dialog._execute_plot()
        self.assertEqual(result, ["x**2", "sin(x)", "x**3"])


class TestParametricPlotDialog(unittest.TestCase):
    def setUp(self):
        self.plotter = DummyPlotter()
        self.manager = DummyWindowManager()
        self.parent = PlottingPanel(DummyApp())
        self.dialog = ParametricPlotDialog(self.parent, self.plotter, self.manager, lambda: {})

    def test_execute_plot_calls_parametric_plot(self):
        self.dialog._execute_plot()
        self.assertIsNotNone(self.plotter.last_call)
        kind, x_expr, y_expr, param, prange = self.plotter.last_call
        self.assertEqual(kind, "create_parametric_plot")


class TestPolarPlotDialog(unittest.TestCase):
    def setUp(self):
        self.plotter = DummyPlotter()
        self.manager = DummyWindowManager()
        self.parent = PlottingPanel(DummyApp())
        self.dialog = PolarPlotDialog(self.parent, self.plotter, self.manager)

    def test_execute_plot_calls_polar_plot(self):
        self.dialog._execute_plot()
        self.assertIsNotNone(self.plotter.last_call)
        kind, expr, param, arange = self.plotter.last_call
        self.assertEqual(kind, "create_polar_plot")


class TestThreeDPlotDialog(unittest.TestCase):
    def setUp(self):
        self.plotter = DummyPlotter()
        self.manager = DummyWindowManager()
        self.parent = PlottingPanel(DummyApp())
        self.dialog = ThreeDPlotDialog(self.parent, self.plotter, self.manager)

    def test_execute_surface_plot_calls_surface_plot(self):
        self.dialog._execute_surface_plot()
        kind, expr, xr, yr = self.plotter.last_call
        self.assertEqual(kind, "create_surface_plot")

    def test_execute_curve_plot_calls_3d_parametric_plot(self):
        self.dialog._execute_curve_plot()
        kind, x_expr, y_expr, z_expr, param, prange = self.plotter.last_call
        self.assertEqual(kind, "create_3d_parametric_plot")


class TestImplicitPlotDialog(unittest.TestCase):
    def setUp(self):
        self.plotter = DummyPlotter()
        self.manager = DummyWindowManager()
        self.parent = PlottingPanel(DummyApp())
        self.dialog = ImplicitPlotDialog(self.parent, self.plotter, self.manager)

    def test_execute_plot_calls_implicit_plot(self):
        self.dialog._execute_plot()
        kind, expr, xr, yr = self.plotter.last_call
        self.assertEqual(kind, "create_implicit_plot")


if __name__ == "__main__":
    unittest.main()
