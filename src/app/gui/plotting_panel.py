from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox,
    QDialog, QTextEdit, QMessageBox
)


PANEL_STYLE = """
    QGroupBox {
        border: 2px solid #444;
        border-radius: 8px;
        margin-top: 10px;
        padding: 15px;
        font-weight: bold;
        color: #FFA500;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
    QLabel {
        color: #CCCCCC;
        font-size: 11pt;
    }
    QLineEdit {
        background-color: #2B2B2B;
        color: #FFFFFF;
        border: 2px solid #444;
        border-radius: 5px;
        padding: 5px;
        font-size: 11pt;
    }
    QLineEdit:focus {
        border: 2px solid #FFA500;
    }
    QPushButton {
        background-color: #FFA500;
        color: #000000;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        font-size: 11pt;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #FFB733;
    }
    QPushButton:pressed {
        background-color: #CC8400;
    }
"""

DIALOG_STYLE = """
    QDialog {
        background-color: #1E1E1E;
    }
    QLabel {
        color: #CCCCCC;
        font-size: 11pt;
    }
    QLineEdit {
        background-color: #2B2B2B;
        color: #FFFFFF;
        border: 2px solid #444;
        border-radius: 5px;
        padding: 5px;
        font-size: 11pt;
    }
    QLineEdit:focus {
        border: 2px solid #FFA500;
    }
    QTextEdit {
        background-color: #2B2B2B;
        color: #FFFFFF;
        border: 2px solid #444;
        border-radius: 5px;
        font-size: 11pt;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    QPushButton {
        background-color: #FFA500;
        color: #000000;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        font-size: 11pt;
        font-weight: bold;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: #FFB733;
    }
    QPushButton:pressed {
        background-color: #CC8400;
    }
"""


class PlottingPanel(QWidget):
    
    def __init__(self, application_reference, parent=None):
        super().__init__(parent)
        self.app = application_reference
        
        from ..core.plotter import ExpressionPlotter, PlotWindowManager
        self.plotter = ExpressionPlotter()
        self.window_manager = PlotWindowManager()
        
        self._build_interface()
        self.setStyleSheet(PANEL_STYLE)
    
    def _build_interface(self):
        main_layout = QVBoxLayout()
        group_box = QGroupBox("Plotting Controls")
        group_layout = QVBoxLayout()

        group_layout.addLayout(self.create_range_row())
        group_layout.addLayout(self.create_actions_row())

        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)
    
    def _create_range_controls(self):
        layout = QHBoxLayout()

        layout.addWidget(QLabel("Variable:"))
        self.variable_input = QLineEdit("x")
        self.variable_input.setMaximumWidth(50)
        layout.addWidget(self.variable_input)

        layout.addSpacing(20)
        layout.addWidget(QLabel("Range:"))

        self.x_min_input = QLineEdit("-10")
        self.x_min_input.setMaximumWidth(80)
        layout.addWidget(self.x_min_input)

        layout.addWidget(QLabel("to"))

        self.x_max_input = QLineEdit("10")
        self.x_max_input.setMaximumWidth(80)
        layout.addWidget(self.x_max_input)

        layout.addStretch()
        return layout

    def create_actions_row(self):
        layout = QHBoxLayout()
        
        layout.addWidget(self._create_button("Plot Expression", self.plot_single))
        layout.addWidget(self._create_button("Plot Multiple", self.plot_multiple))
        layout.addWidget(self._create_button("Parametric Plot", self.plot_parametric))
        layout.addWidget(self._create_button("Polar Plot", self.plot_polar))
        layout.addWidget(self._create_button("3D Plot", self.plot_3d))
        layout.addWidget(self._create_button("Implicit Plot", self.plot_implicit))
        
        layout.addStretch()
        return layout
    
    def _create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        return button
    
    def update_variables(self, variables_dict):
        self.plotter.set_variables(variables_dict)
    
    def _sync_variables(self):
        if hasattr(self.app, 'engine') and hasattr(self.app.engine, 'list_variables'):
            self.plotter.set_variables(self.app.engine.list_variables())
    
    def plot_single(self):
        expression = self._get_expression()
        if not expression:
            QMessageBox.warning(self, "Warning", "Please enter an expression")
            return
        
        self._sync_variables()
        
        try:
            params = self.current_plot_parameters()
            figure = self.plotter.create_plot(
                expression,
                variable=params["variable"],
                x_range=(params["x_min"], params["x_max"]),
                num_points=params["points"]
            )
            self.window_manager.create_plot_window(self, figure, f"Plot of {expression}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def plot_multiple(self):
        self._sync_variables()
        dialog = MultipleExpressionDialog(self, self.plotter, self.window_manager, self._get_parameters)
        dialog.exec()

    def plot_parametric(self):
        self._sync_variables()
        dialog = ParametricPlotDialog(self, self.plotter, self.window_manager, self._get_parameters)
        dialog.exec()
    
    def plot_polar(self):
        self._sync_variables()
        dialog = PolarPlotDialog(self, self.plotter, self.window_manager)
        dialog.exec()
    
    def plot_3d(self):
        self._sync_variables()
        dialog = ThreeDPlotDialog(self, self.plotter, self.window_manager)
        dialog.exec()
    
    def plot_implicit(self):
        self._sync_variables()
        dialog = ImplicitPlotDialog(self, self.plotter, self.window_manager)
        dialog.exec()
    
    def _get_expression(self):
        if hasattr(self.app, 'get_current_expression'):
            return self.app.get_current_expression()
        if hasattr(self.app, "input_field"):
            return self.app.input_field.text()
        return ""

    def current_plot_parameters(self):
        return {
            "x_min": float(self.x_min_input.text()),
            "x_max": float(self.x_max_input.text()),
            "variable": self.variable_input.text(),
            "points": 1000
        }


class MultipleExpressionDialog(QDialog):
    def __init__(self, parent, plotter, window_manager, get_parameters):
        super().__init__(parent)
        self.plotter = plotter
        self.window_manager = window_manager
        self.get_parameters = get_parameters

        self.text_input = None

        self.setWindowTitle("Plot Multiple Expressions")
        self.resize(500, 400)
        self.setStyleSheet(DIALOG_STYLE)
        
        self._build_interface()
    
    def _build_interface(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter expressions (one per line):"))

        self.text_input = QTextEdit()
        self.text_input.setPlainText("x**2\nx**3\nsin(x)")
        layout.addWidget(self.text_input)
        
        layout.addLayout(self._create_buttons())
        self.setLayout(layout)
    
    def _create_buttons(self):
        layout = QHBoxLayout()
        
        layout.addWidget(self._create_button("Plot", self._execute_plot))
        layout.addWidget(self._create_button("Cancel", self.reject))
        
        layout.addStretch()
        return layout
    
    def _create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        return button
    
    def _execute_plot(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            return []
        return [line.strip() for line in text.splitlines() if line.strip()]

    def execute_plot(self):
        expressions = self.expressions()
        if not expressions:
            QMessageBox.warning(self, "Warning", "Enter at least one expression")
            return

        try:
            params = self.get_parameters()
            figure = self.plotter.create_multi_plot(
                expressions,
                variable=params["variable"],
                x_range=(params["x_min"], params["x_max"]),
                num_points=params["points"]
            )
            self.window_manager.create_plot_window(self, figure, "Multiple Expressions")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class ParametricPlotDialog(QDialog):
    def __init__(self, parent, plotter, window_manager, get_parameters):
        super().__init__(parent)
        self.plotter = plotter
        self.window_manager = window_manager
        self.get_parameters = get_parameters

        self.x_input = None
        self.y_input = None
        self.param_input = None
        self.min_input = None
        self.max_input = None

        self.setWindowTitle("Parametric Plot")
        self.resize(450, 250)
        self.setStyleSheet(DIALOG_STYLE)
        
        self._build_interface()
    
    def _build_interface(self):
        layout = QVBoxLayout()
        
        layout.addLayout(self._create_expression_inputs())
        layout.addLayout(self._create_parameter_controls())
        layout.addLayout(self._create_buttons())
        
        self.setLayout(layout)
    
    def _create_expression_inputs(self):
        container = QVBoxLayout()
        
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X Expression:"))
        self.x_input = QLineEdit("cos(t)")
        x_layout.addWidget(self.x_input)
        container.addLayout(x_layout)
        
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y Expression:"))
        self.y_input = QLineEdit("sin(t)")
        y_layout.addWidget(self.y_input)
        container.addLayout(y_layout)
        
        return container
    
    def _create_parameter_controls(self):
        container = QVBoxLayout()
        
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("Parameter:"))
        self.param_input = QLineEdit("t")
        self.param_input.setMaximumWidth(50)
        param_layout.addWidget(self.param_input)
        param_layout.addStretch()
        container.addLayout(param_layout)
        
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Parameter Range:"))
        self.min_input = QLineEdit("0")
        self.min_input.setMaximumWidth(80)
        range_layout.addWidget(self.min_input)
        range_layout.addWidget(QLabel("to"))
        self.max_input = QLineEdit("6.28")
        self.max_input.setMaximumWidth(80)
        range_layout.addWidget(self.max_input)
        range_layout.addStretch()
        container.addLayout(range_layout)
        
        return container
    
    def _create_buttons(self):
        layout = QHBoxLayout()
        
        layout.addWidget(self._create_button("Plot", self._execute_plot))
        layout.addWidget(self._create_button("Cancel", self.reject))
        
        layout.addStretch()
        return layout
    
    def _create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        return button
    
    def _execute_plot(self):
        try:
            figure = self.plotter.create_parametric_plot(
                self.x_input.text(),
                self.y_input.text(),
                parameter=self.param_input.text(),
                param_range=(float(self.min_input.text()), float(self.max_input.text()))
            )
            self.window_manager.create_plot_window(self, figure, "Parametric Plot")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class PolarPlotDialog(QDialog):
    
    def __init__(self, parent, plotter, window_manager):
        super().__init__(parent)
        self.plotter = plotter
        self.window_manager = window_manager
        
        self.setWindowTitle("Polar Plot")
        self.resize(450, 230)
        self.setStyleSheet(DIALOG_STYLE)
        
        self._build_interface()
    
    def _build_interface(self):
        layout = QVBoxLayout()
        
        r_layout = QHBoxLayout()
        r_layout.addWidget(QLabel("r(θ) expression:"))
        self.r_input = QLineEdit("1 + cos(theta)")
        r_layout.addWidget(self.r_input)
        layout.addLayout(r_layout)
        
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("Parameter:"))
        self.param_input = QLineEdit("theta")
        self.param_input.setMaximumWidth(80)
        param_layout.addWidget(self.param_input)
        param_layout.addStretch()
        layout.addLayout(param_layout)
        
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Angle range:"))
        self.min_input = QLineEdit("0")
        self.min_input.setMaximumWidth(80)
        range_layout.addWidget(self.min_input)
        range_layout.addWidget(QLabel("to"))
        self.max_input = QLineEdit("6.28")
        self.max_input.setMaximumWidth(80)
        range_layout.addWidget(self.max_input)
        range_layout.addStretch()
        layout.addLayout(range_layout)
        
        layout.addLayout(self._create_buttons())
        self.setLayout(layout)
    
    def _create_buttons(self):
        layout = QHBoxLayout()
        
        layout.addWidget(self._create_button("Plot", self._execute_plot))
        layout.addWidget(self._create_button("Cancel", self.reject))
        
        layout.addStretch()
        return layout
    
    def _create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        return button
    
    def _execute_plot(self):
        try:
            figure = self.plotter.create_polar_plot(
                self.r_input.text(),
                parameter=self.param_input.text(),
                angle_range=(float(self.min_input.text()), float(self.max_input.text()))
            )
            self.window_manager.create_plot_window(self, figure, "Polar Plot")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class ThreeDPlotDialog(QDialog):
    
    def __init__(self, parent, plotter, window_manager):
        super().__init__(parent)
        self.plotter = plotter
        self.window_manager = window_manager
        
        self.setWindowTitle("3D Plot")
        self.resize(500, 400)
        self.setStyleSheet(DIALOG_STYLE)
        
        self._build_interface()
    
    def _build_interface(self):
        layout = QVBoxLayout()
        
        # Surface z(x,y)
        surface_group = QGroupBox("Surface z = f(x, y)")
        surface_layout = QVBoxLayout()
        
        expr_row = QHBoxLayout()
        expr_row.addWidget(QLabel("z(x, y) ="))
        self.surface_expr_input = QLineEdit("sin(x) * cos(y)")
        expr_row.addWidget(self.surface_expr_input)
        surface_layout.addLayout(expr_row)
        
        xr_row = QHBoxLayout()
        xr_row.addWidget(QLabel("x range:"))
        self.x_min_input = QLineEdit("-5")
        self.x_min_input.setMaximumWidth(80)
        xr_row.addWidget(self.x_min_input)
        xr_row.addWidget(QLabel("to"))
        self.x_max_input = QLineEdit("5")
        self.x_max_input.setMaximumWidth(80)
        xr_row.addWidget(self.x_max_input)
        xr_row.addStretch()
        surface_layout.addLayout(xr_row)
        
        yr_row = QHBoxLayout()
        yr_row.addWidget(QLabel("y range:"))
        self.y_min_input = QLineEdit("-5")
        self.y_min_input.setMaximumWidth(80)
        yr_row.addWidget(self.y_min_input)
        yr_row.addWidget(QLabel("to"))
        self.y_max_input = QLineEdit("5")
        self.y_max_input.setMaximumWidth(80)
        yr_row.addWidget(self.y_max_input)
        yr_row.addStretch()
        surface_layout.addLayout(yr_row)
        
        surface_button = QPushButton("Plot Surface")
        surface_button.clicked.connect(self._execute_surface_plot)
        surface_layout.addWidget(surface_button)
        
        surface_group.setLayout(surface_layout)
        layout.addWidget(surface_group)
        
        # 3D parametric curve
        curve_group = QGroupBox("3D Parametric Curve (x(t), y(t), z(t))")
        curve_layout = QVBoxLayout()
        
        x_row = QHBoxLayout()
        x_row.addWidget(QLabel("x(t) ="))
        self.x_expr_input = QLineEdit("cos(t)")
        x_row.addWidget(self.x_expr_input)
        curve_layout.addLayout(x_row)
        
        y_row = QHBoxLayout()
        y_row.addWidget(QLabel("y(t) ="))
        self.y_expr_input = QLineEdit("sin(t)")
        y_row.addWidget(self.y_expr_input)
        curve_layout.addLayout(y_row)
        
        z_row = QHBoxLayout()
        z_row.addWidget(QLabel("z(t) ="))
        self.z_expr_input = QLineEdit("t")
        z_row.addWidget(self.z_expr_input)
        curve_layout.addLayout(z_row)
        
        p_row = QHBoxLayout()
        p_row.addWidget(QLabel("Parameter:"))
        self.param_input = QLineEdit("t")
        self.param_input.setMaximumWidth(60)
        p_row.addWidget(self.param_input)
        p_row.addWidget(QLabel("from"))
        self.param_min_input = QLineEdit("0")
        self.param_min_input.setMaximumWidth(80)
        p_row.addWidget(self.param_min_input)
        p_row.addWidget(QLabel("to"))
        self.param_max_input = QLineEdit("6.28")
        self.param_max_input.setMaximumWidth(80)
        p_row.addWidget(self.param_max_input)
        p_row.addStretch()
        curve_layout.addLayout(p_row)
        
        curve_button = QPushButton("Plot 3D Curve")
        curve_button.clicked.connect(self._execute_curve_plot)
        curve_layout.addWidget(curve_button)
        
        curve_group.setLayout(curve_layout)
        layout.addWidget(curve_group)
        
        self.setLayout(layout)
    
    def _execute_surface_plot(self):
        try:
            figure = self.plotter.create_surface_plot(
                self.surface_expr_input.text(),
                x_range=(float(self.x_min_input.text()), float(self.x_max_input.text())),
                y_range=(float(self.y_min_input.text()), float(self.y_max_input.text()))
            )
            self.window_manager.create_plot_window(self, figure, "3D Surface")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def _execute_curve_plot(self):
        try:
            figure = self.plotter.create_3d_parametric_plot(
                self.x_expr_input.text(),
                self.y_expr_input.text(),
                self.z_expr_input.text(),
                parameter=self.param_input.text(),
                param_range=(float(self.param_min_input.text()), float(self.param_max_input.text()))
            )
            self.window_manager.create_plot_window(self, figure, "3D Parametric Curve")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class ImplicitPlotDialog(QDialog):
    
    def __init__(self, parent, plotter, window_manager):
        super().__init__(parent)
        self.plotter = plotter
        self.window_manager = window_manager
        
        self.setWindowTitle("Implicit Plot")
        self.resize(450, 260)
        self.setStyleSheet(DIALOG_STYLE)
        
        self._build_interface()
    
    def _build_interface(self):
        layout = QVBoxLayout()
        
        expr_row = QHBoxLayout()
        expr_row.addWidget(QLabel("f(x, y) = 0 or equation:"))
        self.expr_input = QLineEdit("x**2 + y**2 - 1")
        expr_row.addWidget(self.expr_input)
        layout.addLayout(expr_row)
        
        xr_row = QHBoxLayout()
        xr_row.addWidget(QLabel("x range:"))
        self.x_min_input = QLineEdit("-2")
        self.x_min_input.setMaximumWidth(80)
        xr_row.addWidget(self.x_min_input)
        xr_row.addWidget(QLabel("to"))
        self.x_max_input = QLineEdit("2")
        self.x_max_input.setMaximumWidth(80)
        xr_row.addWidget(self.x_max_input)
        xr_row.addStretch()
        layout.addLayout(xr_row)
        
        yr_row = QHBoxLayout()
        yr_row.addWidget(QLabel("y range:"))
        self.y_min_input = QLineEdit("-2")
        self.y_min_input.setMaximumWidth(80)
        yr_row.addWidget(self.y_min_input)
        yr_row.addWidget(QLabel("to"))
        self.y_max_input = QLineEdit("2")
        self.y_max_input.setMaximumWidth(80)
        yr_row.addWidget(self.y_max_input)
        yr_row.addStretch()
        layout.addLayout(yr_row)
        
        layout.addLayout(self._create_buttons())
        self.setLayout(layout)
    
    def _create_buttons(self):
        layout = QHBoxLayout()
        
        layout.addWidget(self._create_button("Plot", self._execute_plot))
        layout.addWidget(self._create_button("Cancel", self.reject))
        
        layout.addStretch()
        return layout
    
    def _create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        return button
    
    def _execute_plot(self):
        try:
            figure = self.plotter.create_implicit_plot(
                self.expr_input.text(),
                x_range=(float(self.x_min_input.text()), float(self.x_max_input.text())),
                y_range=(float(self.y_min_input.text()), float(self.y_max_input.text()))
            )
            self.window_manager.create_plot_window(self, figure, "Implicit Plot")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))