from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QGroupBox,
                             QDialog, QTextEdit, QMessageBox)


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
        color: #FFFFFF;
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
        color: #FFFFFF;
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
        
        group_layout.addLayout(self._create_range_controls())
        group_layout.addLayout(self._create_action_buttons())
        
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
    
    def _create_action_buttons(self):
        layout = QHBoxLayout()
        
        layout.addWidget(self._create_button("Plot Expression", self.plot_single))
        layout.addWidget(self._create_button("Plot Multiple", self.plot_multiple))
        layout.addWidget(self._create_button("Parametric Plot", self.plot_parametric))
        
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
            params = self._get_parameters()
            figure = self.plotter.create_plot(
                expression,
                variable=params['variable'],
                x_range=(params['x_min'], params['x_max']),
                num_points=params['points']
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
    
    def _get_expression(self):
        if hasattr(self.app, 'get_current_expression'):
            return self.app.get_current_expression()
        elif hasattr(self.app, 'input_field'):
            return self.app.input_field.text()
        return ""
    
    def _get_parameters(self):
        return {
            'x_min': float(self.x_min_input.text()),
            'x_max': float(self.x_max_input.text()),
            'variable': self.variable_input.text(),
            'points': 1000
        }


class MultipleExpressionDialog(QDialog):
    
    def __init__(self, parent, plotter, window_manager, get_params_func):
        super().__init__(parent)
        self.plotter = plotter
        self.window_manager = window_manager
        self.get_params = get_params_func
        
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
            QMessageBox.warning(self, "Warning", "Enter at least one expression")
            return

        expressions = [e.strip() for e in text.split('\n') if e.strip()]

        try:
            params = self.get_params()
            figure = self.plotter.create_multi_plot(
                expressions,
                variable=params['variable'],
                x_range=(params['x_min'], params['x_max']),
                num_points=params['points']
            )
            self.window_manager.create_plot_window(self, figure, "Multiple Expressions")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class ParametricPlotDialog(QDialog):
    
    def __init__(self, parent, plotter, window_manager, get_params_func):
        super().__init__(parent)
        self.plotter = plotter
        self.window_manager = window_manager
        self.get_params = get_params_func
        
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