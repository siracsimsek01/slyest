from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox,
    QDialog, QTextEdit, QMessageBox
)


class PlottingPanel(QWidget):
    def __init__(self, application_reference, parent=None):
        super().__init__(parent)
        self.app = application_reference

        from ..core.plotter import ExpressionPlotter, PlotWindowManager
        self.plotter = ExpressionPlotter()
        self.window_manager = PlotWindowManager()

        self.variable_input = None
        self.x_min_input = None
        self.x_max_input = None

        self.build_interface()
        self.apply_styling()

    def apply_styling(self):
        self.setStyleSheet("""
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
        """)

    def build_interface(self):
        main_layout = QVBoxLayout()
        group_box = QGroupBox("Plotting Controls")
        group_layout = QVBoxLayout()

        group_layout.addLayout(self.create_range_row())
        group_layout.addLayout(self.create_actions_row())

        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

    def create_range_row(self):
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

        plot_button = QPushButton("Plot Expression")
        plot_button.clicked.connect(self.plot_single_expression)
        layout.addWidget(plot_button)

        multiple_button = QPushButton("Plot Multiple")
        multiple_button.clicked.connect(self.plot_multiple_expressions)
        layout.addWidget(multiple_button)

        parametric_button = QPushButton("Parametric Plot")
        parametric_button.clicked.connect(self.plot_parametric_curve)
        layout.addWidget(parametric_button)

        layout.addStretch()
        return layout

    def update_variables(self, variables_dict):
        self.plotter.set_variables(variables_dict)

    def plot_single_expression(self):
        expression = self.current_expression()
        if not expression:
            QMessageBox.warning(self, "Warning", "Please enter an expression")
            return

        if hasattr(self.app, "engine") and hasattr(self.app.engine, "list_variables"):
            self.plotter.set_variables(self.app.engine.list_variables())

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

    def plot_multiple_expressions(self):
        if hasattr(self.app, "engine") and hasattr(self.app.engine, "list_variables"):
            self.plotter.set_variables(self.app.engine.list_variables())

        dialog = MultipleExpressionDialog(
            self,
            self.plotter,
            self.window_manager,
            self.current_plot_parameters
        )
        dialog.exec()

    def plot_parametric_curve(self):
        if hasattr(self.app, "engine") and hasattr(self.app.engine, "list_variables"):
            self.plotter.set_variables(self.app.engine.list_variables())

        dialog = ParametricPlotDialog(
            self,
            self.plotter,
            self.window_manager,
            self.current_plot_parameters
        )
        dialog.exec()

    def current_expression(self):
        if hasattr(self.app, "get_current_expression"):
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
        self.apply_styling()
        self.build_interface()

    def apply_styling(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
            }
            QLabel {
                color: #CCCCCC;
                font-size: 11pt;
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
        """)

    def build_interface(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter expressions (one per line):"))

        self.text_input = QTextEdit()
        self.text_input.setPlainText("x**2\nx**3\nsin(x)")
        layout.addWidget(self.text_input)

        button_layout = QHBoxLayout()
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.execute_plot)
        button_layout.addWidget(plot_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def expressions(self):
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
        self.apply_styling()
        self.build_interface()

    def apply_styling(self):
        self.setStyleSheet("""
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
        """)

    def build_interface(self):
        layout = QVBoxLayout()

        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X Expression:"))
        self.x_input = QLineEdit("cos(t)")
        x_layout.addWidget(self.x_input)
        layout.addLayout(x_layout)

        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y Expression:"))
        self.y_input = QLineEdit("sin(t)")
        y_layout.addWidget(self.y_input)
        layout.addLayout(y_layout)

        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("Parameter:"))
        self.param_input = QLineEdit("t")
        self.param_input.setMaximumWidth(50)
        param_layout.addWidget(self.param_input)
        param_layout.addStretch()
        layout.addLayout(param_layout)

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
        layout.addLayout(range_layout)

        button_layout = QHBoxLayout()
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.execute_plot)
        button_layout.addWidget(plot_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def execute_plot(self):
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
