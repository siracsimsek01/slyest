from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QScrollArea, QSizePolicy, QMessageBox
)
from PyQt6.QtCore import Qt

from ..core.symbolic_engine import SymbolicEngine
from ..core.plotter import ExpressionPlotter
from ..core.math_formatter import MathFormatter
from ..gui.calculator_buttons import CalculatorButton
from ..gui.styles import get_calculator_stylesheet
from ..gui.variable_window import VariableWindow
from ..gui.learning_mode_window import LearningModeWindow
from ..gui.history_panel import HistoryPanel
from ..gui.calculator_operations import CalculatorOperations
from src.app.core.perform_substitution import Substitution
from src.app.core.algebraic_expressions import AlgebraicExpressions
from src.app.core.two_linear_equations import TwoLinearEquations
from src.app.core.symbolic_to_decimal import toggle_format
from sympy import sympify

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SLYEST - Scientific Calculator")
        self.setGeometry(100, 100, 800, 900)

        self.engine = SymbolicEngine()
        self.substitution = Substitution()
        self.equation_solver = AlgebraicExpressions()
        self.two_equations_solver = TwoLinearEquations()

        self.operations = CalculatorOperations(self.engine)
        self.plotter = ExpressionPlotter()
        self.current_expression = ""
        self.operation = ""
        self.setStyleSheet(get_calculator_stylesheet())
        self.initialise_ui()

    def _set_formatted_text(self, widget: QLineEdit, text: str):
        widget.setText(MathFormatter.to_display(text))

    def _get_internal_text(self, widget: QLineEdit) -> str:
        return MathFormatter.to_internal(widget.text())

    def initialise_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.create_top_bar(main_layout) # contains variables + history toggle
        self.create_display(main_layout) # display area
        self.create_history_panel(main_layout) # history panel (initially hidden)
        self.create_calculator_buttons(main_layout) # main calculator buttons 

    def create_top_bar(self, parent_layout):
        """create the top bar with variables and history button."""
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        variable_container = QWidget()
        variable_container.setObjectName("variableBar")
        variable_layout = QHBoxLayout(variable_container)
        variable_layout.setSpacing(8)
        var_label = QLabel("Variables:")
        var_label.setStyleSheet("color: #A0A0A0; font-size: 10pt;")
        variable_layout.addWidget(var_label)

        self.variable_buttons_layout = QHBoxLayout() # At least 5 variables
        self.variable_buttons_layout.setSpacing(6)
        variable_layout.addLayout(self.variable_buttons_layout)
        self.refresh_variable_display() # initially show none message
        variable_layout.addStretch()

        variable_layout.addWidget(self.create_new_button("Manage", "manageVarsBtn", self.open_variable_manager)) # Manage variable button
        top_bar_layout.addWidget(variable_container)
        top_bar_layout.addWidget(self.create_new_button("History ▼", "historyToggle", self.toggle_history)) # Toggle History button
        parent_layout.addWidget(top_bar)

    def create_display(self, parent_layout):
        """create the display area for showing expressions and results."""
        # expression input field (for typing algebraic expressions like "2x + 5")
        self.expression_input = QLineEdit()
        self.expression_input.setObjectName("expressionInput")
        self.expression_input.setPlaceholderText("Type expression: 2*x + 5, sin(x), x**2...")

        self.optional_expression_input = QLineEdit()
        self.optional_expression_input.setObjectName("optionalExpressionInput")
        self.optional_expression_input.setPlaceholderText("Optional: e.g., x=5, y=3 for substitution <or> x - y = 12 for solving two linear equations....")

        self.expression_input.setMinimumHeight(40)
        self.expression_input.returnPressed.connect(self.handle_expression_input)
        parent_layout.addWidget(self.expression_input)

        self.optional_expression_input.setMinimumHeight(40)
        self.optional_expression_input.returnPressed.connect(self.handle_optional_expression_input)
        parent_layout.addWidget(self.optional_expression_input)
        self.create_symbolic_buttons(parent_layout)

        container = QWidget()
        display_layout = QHBoxLayout(container)
        self.display = QLabel("0")
        self.display.setObjectName("display")
        self.display.setMinimumHeight(100)
        self.display.setWordWrap(True)
        self.display.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.display)
        scroll_area.setFixedHeight(100)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        display_layout.addWidget(self.display)
        help_btn = self.create_new_button("?", "help", self.launch_learning_mode)
        help_btn.setFixedSize(30, 30)
        display_layout.addWidget(help_btn)
        parent_layout.addWidget(container)

    def handle_expression_input(self):
        pass

    def handle_optional_expression_input(self):
        pass

    def create_symbolic_buttons(self, parent_layout):
        """create buttons for symbolic operations like simplify, expand, factor, etc"""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(6)
        button_layout.setContentsMargins(0, 5, 0, 5)

        button_layout.addWidget(self.create_new_button("Simplify", "symbolicBtn", lambda: self.handle_symbolic_operation('simplify'))) # Simplify
        button_layout.addWidget(self.create_new_button("Expand", "symbolicBtn", lambda: self.handle_symbolic_operation('expand'))) # expand
        button_layout.addWidget(self.create_new_button("Factor", "symbolicBtn", lambda: self.handle_symbolic_operation('factor'))) # factor
        button_layout.addWidget(self.create_new_button("Solve", "symbolicBtn", lambda: self.handle_symbolic_operation('solve'))) # solve
        button_layout.addWidget(self.create_new_button("Substitute", "symbolicBtn", lambda: self.handle_symbolic_operation('substitute'))) # substitute
        button_layout.addWidget(self.create_new_button("Solve 2 Equations", "symbolicBtn", lambda: self.handle_symbolic_operation('solve 2 equations'))) # sovle 2 equations
        button_layout.addWidget(self.create_new_button("Differentiate", "symbolicBtn", lambda: self.handle_symbolic_operation('differentiate'))) # differentiate

        parent_layout.addWidget(button_container)

    def create_history_panel(self, parent_layout):
        """create the history panel (collapsible)."""
        self.history_panel = HistoryPanel()
        self.history_panel.history_item_selected.connect(self.use_history_item)
        self.history_panel.setVisible(False) 
        self.history_panel.setMaximumHeight(200)
        parent_layout.addWidget(self.history_panel)

    def create_calculator_buttons(self, parent_layout):
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)

        scientific_grid = self.create_scientific_buttons() # Left column
        button_layout.addLayout(scientific_grid, 2)  # Takes 2/3 of space

        number_grid = self.create_number_pad() # Right column
        button_layout.addLayout(number_grid, 1)  # Takes 1/3 of space
        parent_layout.addWidget(button_container)

    def create_scientific_buttons(self) -> QGridLayout:
        """create the left column with scientific function buttons."""
        grid = QGridLayout()
        grid.setSpacing(6)

        # row 0: parentheses and memory
        row0 = [
            ("(", "special"),
            (")", "special"),
            ("mc", "scientific"),
            ("m+", "scientific"),
            ("m-", "scientific"),
            ("mr", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row0):
            btn = CalculatorButton(text, btn_type)
            # connect buttons
            if text in ["(", ")"]:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_parenthesis_click(t))
            elif text in ["mc", "m+", "m-", "mr"]:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_memory_click(t))
            grid.addWidget(btn, 0, col)

        # row 1: powers and exponentials
        row1 = [
            ("=", "scientific"),
            ("x²", "scientific"),
            ("x³", "scientific"),
            ("xʸ", "scientific"),
            ("eˣ", "scientific"),
            ("10ˣ", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row1):
            btn = CalculatorButton(text, btn_type)
            btn.clicked.connect(lambda checked=False, t=text: self.handle_scientific_function_click(t))
            grid.addWidget(btn, 1, col)

        # row 2: roots and logarithms
        row2 = [
            ("1/x", "scientific"),
            ("²√x", "scientific"),
            ("³√x", "scientific"),
            ("ʸ√x", "scientific"),
            ("ln", "scientific"),
            ("log₁₀", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row2):
            btn = CalculatorButton(text, btn_type)
            if text == "²√x":
                btn.clicked.connect(lambda: self.handle_scientific_function_click("sqrt"))
            elif text == "³√x":
                btn.clicked.connect(lambda: self.handle_scientific_function_click("cbrt"))
            elif text == "ʸ√x":
                btn.clicked.connect(lambda: self.handle_scientific_function_click("ʸ√x"))
            else:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_scientific_function_click(t))
            grid.addWidget(btn, 2, col)

        # Row 3: trigonometry and constants
        row3 = [
            ("x!", "scientific"),
            ("sin", "scientific"),
            ("cos", "scientific"),
            ("tan", "scientific"),
            ("e", "scientific"),
            ("π", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row3):
            btn = CalculatorButton(text, btn_type)
            if text in ["e", "π"]:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_constant_click(t))
            else:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_scientific_function_click(t))
            grid.addWidget(btn, 3, col)

        # Row 4: hyperbolic and special symbols
        row4 = [
            ("S<=>D", "scientific"),
            ("sinh", "scientific"),
            ("cosh", "scientific"),
            ("tanh", "scientific"),
            ("x", "scientific"),
            ("y", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row4):
            btn = CalculatorButton(text, btn_type)
            if text == "S<=>D":
                
                btn.clicked.connect(self.handle_std_click)
            elif text in ["x", "y"]:
                
                btn.clicked.connect(lambda checked=False, t=text: self.handle_special_click(t))
            else:
                
                btn.clicked.connect(lambda checked=False, t=text: self.handle_scientific_function_click(t))
            grid.addWidget(btn, 4, col)
        return grid

    def create_number_pad(self) -> QGridLayout:
        """Create the right column with number pad and operations."""
        grid = QGridLayout()
        grid.setSpacing(6)

        # Row 0: AC, ←, %, ÷
        row0 = [
            ("AC", "special"),
            ("←", "special"),
            ("%", "special"),
            ("÷", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row0):
            btn = CalculatorButton(text, btn_type)
            if text == "AC":
                btn.clicked.connect(self.handle_clear_click)
            elif text in ["←", "%"]:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_special_click(t))
            elif btn_type == "operation":
                btn.clicked.connect(lambda checked=False, t=text: self.handle_operation_click(t))
            grid.addWidget(btn, 0, col)

        # Row 1: 7, 8, 9, ×
        row1 = [
            ("7", "number"),
            ("8", "number"),
            ("9", "number"),
            ("×", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row1):
            btn = CalculatorButton(text, btn_type)
            if btn_type == "number":
                btn.clicked.connect(lambda checked=False, t=text: self.handle_number_click(t))
            elif btn_type == "operation":
                btn.clicked.connect(lambda checked=False, t=text: self.handle_operation_click(t))
            grid.addWidget(btn, 1, col)

        # Row 2: 4, 5, 6, -
        row2 = [
            ("4", "number"),
            ("5", "number"),
            ("6", "number"),
            ("−", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row2):
            btn = CalculatorButton(text, btn_type)
            if btn_type == "number":
                btn.clicked.connect(lambda checked=False, t=text: self.handle_number_click(t))
            elif btn_type == "operation":
                btn.clicked.connect(lambda checked=False, t=text: self.handle_operation_click(t))
            grid.addWidget(btn, 2, col)

        # Row 3: 1, 2, 3, +
        row3 = [
            ("1", "number"),
            ("2", "number"),
            ("3", "number"),
            ("+", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row3):
            btn = CalculatorButton(text, btn_type)
            if btn_type == "number":
                btn.clicked.connect(lambda checked=False, t=text: self.handle_number_click(t))
            elif btn_type == "operation":
                btn.clicked.connect(lambda checked=False, t=text: self.handle_operation_click(t))
            grid.addWidget(btn, 3, col)

        # Row 4: 0 (span 2 cols), ., =
        btn_0 = CalculatorButton("0", "number")
        btn_0.clicked.connect(lambda: self.handle_number_click("0"))
        btn_0.setMinimumWidth(128)
        grid.addWidget(btn_0, 4, 0, 1, 2)

        btn_dot = CalculatorButton(".", "number")
        btn_dot.clicked.connect(self.handle_decimal_click)
        grid.addWidget(btn_dot, 4, 2)

        btn_equals = CalculatorButton("=", "operation")
        btn_equals.clicked.connect(self.handle_equals_click)
        grid.addWidget(btn_equals, 4, 3)
        return grid

    def open_variable_manager(self):
        var_window = VariableWindow(self.engine, self)
        var_window.variables_changed.connect(self.refresh_variable_display)
        var_window.exec()
        self.refresh_variable_display()

    def refresh_variable_display(self):
        """Update the variable chips to show the last 5 variables."""
        while self.variable_buttons_layout.count():
            item = self.variable_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        variables = self.engine.list_variables()
        if not variables:
            no_vars = QLabel("None")
            no_vars.setStyleSheet("color: #A0A0A0; font-size: 10pt; font-style: italic;")
            self.variable_buttons_layout.addWidget(no_vars)
        else: 
            var_items = list(variables.items())[-5:] # Show most recent 5 variables
            for name, value in var_items:
                btn = QPushButton(f"{name}")
                btn.setObjectName("variableChip")
                btn.setToolTip(f"{name} = {value}")
                btn.clicked.connect(lambda *, n=name: self.insert_variable(n)) # Use lambda with captured variable to avoid late binding issue
                self.variable_buttons_layout.addWidget(btn)

    def insert_variable(self, var_name: str):
        if self.optional_expression_input.hasFocus():
            current_text = self._get_internal_text(self.optional_expression_input)
            self._set_formatted_text(self.optional_expression_input, current_text + var_name)
        else:
            current_text = self._get_internal_text(self.expression_input)
            self._set_formatted_text(self.expression_input, current_text + var_name)

    def toggle_history(self):
        self.history_panel.toggle_visibility()
        history_btn = self.findChild(QPushButton, "historyToggle")
        if self.history_panel.isVisible():
            history_btn.setText("History ▲")
        else:
            history_btn.setText("History ▼")

    def use_history_item(self, data: dict):
        expression = data.get('expression', '')
        optional_expression = data.get('optional_expression', '')
        self.current_expression = expression
        self._set_formatted_text(self.expression_input, self.current_expression)
        self.operations.current_expression = expression
        if optional_expression:
            self._set_formatted_text(self.optional_expression_input, optional_expression)
        else:
            self.optional_expression_input.clear()

    def handle_number_click(self, digit: str):
        if self.optional_expression_input.hasFocus():
            current_text = self._get_internal_text(self.optional_expression_input)
            result = self.operations.input_number(digit, current_text)
            if result is not None:
                self._set_formatted_text(self.optional_expression_input, result)
        else:
            current_text = self._get_internal_text(self.expression_input)
            result = self.operations.input_number(digit, current_text)
            if result is not None:
                self._set_formatted_text(self.expression_input, result)

    def handle_operation_click(self, operation_name: str):
        if self.optional_expression_input.hasFocus():
            current_text = self._get_internal_text(self.optional_expression_input)
            result = self.choose_operations_based_on_symbols(operation_name, current_text)
            if result is not None:
                self._set_formatted_text(self.optional_expression_input, result)
        else:
            current_text = self._get_internal_text(self.expression_input)
            result = self.choose_operations_based_on_symbols(operation_name, current_text)
            if result is not None:
                self._set_formatted_text(self.expression_input, result)

    def choose_operations_based_on_symbols(self, operation_name, current):
        if operation_name == "+":
            result = self.operations.operation('add', current)
        elif operation_name == "−":
            result = self.operations.operation('subtract', current)
        elif operation_name == "×":
            result = self.operations.operation('multiply', current)
        elif operation_name == "÷":
            result = self.operations.operation('divide', current)
        return result

    def handle_equals_click(self):
        current_text = self._get_internal_text(self.expression_input)
        result = self.operations.calculate_result(current_text)
        self.operation = ""
        if result is not None:
            expression, answer = result
            self._set_formatted_text(self.expression_input, expression)
            self.display.setText(MathFormatter.to_display(answer))
            self.history_panel.add_calculation(expression, answer)

    def handle_clear_click(self):
        result = self.operations.clear_all()
        self.operation = ""
        if result is not None:
            self._set_formatted_text(self.expression_input, result)
            self._set_formatted_text(self.optional_expression_input, result)
            self.display.setText(result)

    def handle_scientific_function_click(self, function_name: str):
        if self.optional_expression_input.hasFocus():
            current = self._get_internal_text(self.optional_expression_input)
        else:
            current = self._get_internal_text(self.expression_input)

        result = None
        if function_name == "sin":
            result = self.operations.sin(current)
        elif function_name == "cos":
            result = self.operations.cos(current)
        elif function_name == "tan":
            result = self.operations.tan(current)
        elif function_name == "sinh":
            result = self.operations.sinh(current)
        elif function_name == "cosh":
            result = self.operations.cosh(current)
        elif function_name == "tanh":
            result = self.operations.tanh(current)
        elif function_name == "sqrt":
            result = self.operations.square_root(current)
        elif function_name == "cbrt":
            result = self.operations.cube_root(current)
        elif function_name == "ʸ√x":
            result = self.operations.root(current)
        elif function_name == "x²":
            result = self.operations.square(current)
        elif function_name == "x³":
            result = self.operations.cube(current)
        elif function_name == "xʸ":
            result = self.operations.power(current)
        elif function_name == "1/x":
            result = self.operations.reciprocal(current)
        elif function_name == "eˣ":
            result = self.operations.exp(current)
        elif function_name == "pi":
            result = self.operations.pi(current)
        elif function_name == "10ˣ":
            result = self.operations.power_of_10(current)
        elif function_name == "ln":
            result = self.operations.natural_log(current)
        elif function_name == "log₁₀":
            result = self.operations.log_base_10(current)
        elif function_name == "x!":
            result = self.operations.factorial(current)
        elif function_name == "=":
            result = self.operations.operation("equal", current)

        if result is not None:
            if self.optional_expression_input.hasFocus():
                self._set_formatted_text(self.optional_expression_input, result)
            else:
                self._set_formatted_text(self.expression_input, result)

    def handle_decimal_click(self):
        if self.optional_expression_input.hasFocus():
            current = self._get_internal_text(self.optional_expression_input)
            result = self.operations.input_decimal(current)
            if result is not None:
                self._set_formatted_text(self.optional_expression_input, result)
        else:
            current = self._get_internal_text(self.expression_input)
            result = self.operations.input_decimal(current)
            if result is not None:
                self._set_formatted_text(self.expression_input, result)

    def handle_parenthesis_click(self, parenthesis_type: str):
        if self.optional_expression_input.hasFocus():
            current_text = self._get_internal_text(self.optional_expression_input)
            result = self.choose_parenthesis(parenthesis_type, current_text)
            if result is not None:
                self._set_formatted_text(self.optional_expression_input, result)
        else:
            current_text = self._get_internal_text(self.expression_input)
            result = self.choose_parenthesis(parenthesis_type, current_text)
            if result is not None:
                self._set_formatted_text(self.expression_input, result)

    def choose_parenthesis(self, parenthesis_type, current):
        if parenthesis_type == "(":
            result = self.operations.open_parenthesis(current)
        else:
            result = self.operations.close_parenthesis(current)
        return result

    def handle_constant_click(self, constant: str):
        if self.optional_expression_input.hasFocus():
            current = self._get_internal_text(self.optional_expression_input)
            result = self.choose_constants(constant, current)
            if result is not None:
                self._set_formatted_text(self.optional_expression_input, result)
        else:
            current = self._get_internal_text(self.expression_input)
            result = self.choose_constants(constant, current)
            if result is not None:
                self._set_formatted_text(self.expression_input, result)

    def choose_constants(self, constant, current):
        if constant == "e":
            result = self.operations.insert_constant_e(current)
        elif constant == "π":
            result = self.operations.insert_constant_pi(current)
        return result

    def handle_memory_click(self, action: str):
        current = self.display.text()
        self.operation = ""
        if current == '' or current == 'Error':
            current = '0'
        elif '/' in current:
            decimal_format = sympify(current).evalf()
            current = str(f"{float(decimal_format):.12g}")
        if action == "mc":
            result = self.operations.memory_clear()
            self.display.setText("")
        elif action == "m+":
            result = self.operations.memory_add(current)
        elif action == "m-":
            result = self.operations.memory_subtract(current)
        elif action == "mr":
            result = self.operations.memory_recall()
            if result is not None:
                self._set_formatted_text(self.expression_input, "")
                self.display.setText(MathFormatter.to_display(result))

    def handle_special_click(self, action: str):
        current = self._get_internal_text(self.expression_input)
        result = None
        if action == "←":
            result = self.operations.backspace(current)
        elif action == "%":
            result = self.operations.percentage(current)
        elif action == "Rand":
            result = self.operations.random_number()
        elif action == "x":
            result = self.operations.symbols(action, current)
        elif action == "y":
            result = self.operations.symbols(action, current)
        if result is not None:
            self._set_formatted_text(self.expression_input, result)

    def handle_symbolic_operation(self, operation: str):
        self.operation = operation
        try:
            expression_string = self._get_internal_text(self.expression_input)
            optional_expression_string = self._get_internal_text(self.optional_expression_input)
            if not expression_string:
                return
            expression_string = self.engine.replace_variables(expression_string, operation)
            if optional_expression_string:
                optional_expression_string = self.engine.replace_variables(optional_expression_string, operation)

            if operation == "simplify":
                result = str(self.engine.simplify(expression_string))
            elif operation == 'expand':
                result = str(self.engine.expand(expression_string))
            elif operation == 'factor':
                result = str(self.engine.factor(expression_string))
            elif operation == 'solve':
                result = str(self.equation_solver.solve_algerbraic_equation(expression_string))
            elif operation == 'substitute':
                substituted_values = self.get_substituted_values(optional_expression_string)
                result = str(self.substitution.perform_substitution(expression_string, substituted_values))
            elif operation == 'solve 2 equations':
                result = str(self.two_equations_solver.solve_two_linear_equations(expression_string, optional_expression_string))
            elif operation == 'differentiate':
                result = str(self.engine.differentiate(expression_string, optional_expression_string))
            self.display.setText(MathFormatter.to_display(result))

            self.history_panel.add_calculation(
                self.expression_input.text(),
                self.display.text(),
                operation=self.operation,
                optional_expression=self.optional_expression_input.text() if optional_expression_string else None
            )
        except:
            return
        
    def get_substituted_values(self, subs_str):
        subs_dict = {}
        try:
            for part in subs_str.split(','):
                key, value = part.split('=')
                subs_dict[key.strip()] = value.strip()
            return subs_dict
        except Exception as e:
            return {}  

    def create_new_button(self, button_name, object_name, button_function):
        manage_btn = QPushButton(button_name)
        manage_btn.setObjectName(object_name)
        manage_btn.clicked.connect(button_function)
        return manage_btn
    
    def handle_std_click(self):
        current_text = self.display.text()
        result, success = toggle_format(current_text)
        if success:
            self.display.setText(result)
        else:
            print(f"Toggle failed: {result}")

    def launch_learning_mode(self):
        if self.operation:
            learning_mode_window = LearningModeWindow(self.operation, self.expression_input.text(),
                self.display.text(), self.optional_expression_input.text())
            learning_mode_window.exec()
        else:
            QMessageBox.critical(self, "Error", "Learning mode is not available for this operation.")