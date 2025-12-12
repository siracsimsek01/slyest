import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout
from PyQt6.QtCore import Qt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'app'))

from src.app.ui.plotting_panel import PlottingPanel
from src.app.core.plotter import ExpressionPlotter


class DummyEngine:
    def list_variables(self):
        return {"a": "x+1", "b": "2"}


class TestMainAppPlottingPanelIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.mock_engine = DummyEngine()
        self.main_app = Mock()
        self.main_app.engine = self.mock_engine
        self.main_app.get_current_expression.return_value = "x**2"

    @patch('src.app.ui.plotting_panel.PlottingPanel')
    def test_open_plotting_panel_creates_dialog(self, mock_panel):
        mock_panel_instance = Mock()
        mock_panel.return_value = mock_panel_instance
        
        self.main_app.open_plotting_panel()
        
        mock_panel.assert_called_once_with(
            application_reference=self.main_app,
            parent=Mock()
        )
        mock_panel_instance.update_variables.assert_called_once_with(
            self.mock_engine.list_variables()
        )

    @patch('src.app.ui.plotting_panel.QDialog')
    @patch('src.app.ui.plotting_panel.QVBoxLayout')
    @patch('src.app.ui.plotting_panel.PlottingPanel')
    def test_open_plotting_panel_sets_up_dialog_correctly(
        self, mock_panel, mock_layout, mock_dialog
    ):
        dialog_instance = Mock(spec=QDialog)
        layout_instance = Mock(spec=QVBoxLayout)
        panel_instance = Mock(spec=PlottingPanel)
        
        mock_dialog.return_value = dialog_instance
        mock_layout.return_value = layout_instance
        mock_panel.return_value = panel_instance
        
        self.main_app.open_plotting_panel()
        
        mock_dialog.assert_called_once_with(self.main_app)
        dialog_instance.setWindowTitle.assert_called_once_with("SLYEST - Plotting")
        dialog_instance.resize.assert_called_once_with(900, 700)
        
        mock_layout.assert_called_once()
        mock_panel.assert_called_once_with(
            application_reference=self.main_app,
            parent=dialog_instance
        )
        panel_instance.update_variables.assert_called_once_with(
            self.mock_engine.list_variables()
        )
        layout_instance.addWidget.assert_called_once_with(panel_instance)
        dialog_instance.setLayout.assert_called_once_with(layout_instance)

    @patch('src.app.ui.plotting_panel.PlottingPanel')
    def test_open_plotting_panel_executes_dialog(self, mock_panel):
        dialog_mock = Mock()
        mock_panel.side_effect = [Mock(plotting_dialog=dialog_mock)]
        
        with patch.object(self.main_app, 'plotting_dialog', dialog_mock):
            self.main_app.open_plotting_panel()
        
        dialog_mock.exec.assert_called_once()

    def test_open_plotting_panel_integration_with_real_panel(self):
        dialog = self.main_app.open_plotting_panel()
        
        self.assertIsInstance(dialog, QDialog)
        self.assertEqual(dialog.windowTitle(), "SLYEST - Plotting")
        self.assertEqual(dialog.size().width(), 900)
        self.assertEqual(dialog.size().height(), 700)
        
        panel = dialog.layout().itemAt(0).widget()
        self.assertIsInstance(panel, PlottingPanel)


class TestPlottingPanelAppIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_engine = DummyEngine()
        self.main_app = Mock()
        self.main_app.engine = self.mock_engine

    def test_plotting_panel_gets_variables_from_app(self):
        self.main_app.open_plotting_panel()
        panel = self.main_app.plotting_panel_instance
        
        panel.update_variables.assert_called_once()
        self.assertEqual(panel.plotter.variables, {"a": "x+1", "b": "2"})

    @patch.object(ExpressionPlotter, 'create_plot')
    def test_plot_single_from_app_expression(self, mock_create_plot):
        self.main_app.open_plotting_panel()
        panel = self.main_app.plotting_panel_instance
        
        panel.plot_single()
        
        mock_create_plot.assert_called_once()
        args = mock_create_plot.call_args[1]
        self.assertEqual(args['expression'], "x**2")


if __name__ == '__main__':
    unittest.main()
