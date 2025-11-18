from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QListWidgetItem
)

from ..core.symbolic_engine import SymbolicEngine
from ..core.plotter import ExpressionPlotter
from ..gui.calculator_buttons import CalculatorButton
from ..gui.styles import get_calculator_stylesheet
from ..gui.variable_window import VariableWindow
from ..gui.history_panel import HistoryPanel
from ..gui.calculator_operations import CalculatorOperations
from src.app.core.perform_substitution import Substitution
from src.app.core.algebraic_expressions import AlgebraicExpressions
from src.app.core.two_linear_equations import TwoLinearEquations


class MainWindow(QMainWindow):
    def __init__(self):
        """set up the calculator window."""
        super().__init__()
        self.setWindowTitle("SLYEST - Scientific Calculator")
        self.setGeometry(100, 100, 800, 900)

        # create the calculation engine
        self.engine = SymbolicEngine()
        self.substitution = Substitution()
        self.equation_solver = AlgebraicExpressions()
        self.two_equations_solver = TwoLinearEquations()

        # create the operations handler (this does all the button logic)
        self.operations = CalculatorOperations(self.engine)

        # create plotter for graphing expressions
        self.plotter = ExpressionPlotter()

        # Current expression being built
        self.current_expression = ""

        # Apply the dark theme stylesheet
        self.setStyleSheet(get_calculator_stylesheet())

        # create the main UI
        self.init_ui()

    def init_ui(self):
        """create all the UI components."""
        # main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # top bar: variables + history toggle
        self.create_top_bar(main_layout)

        # display area
        self.create_display(main_layout)

        # history panel (initially hidden)
        self.create_history_panel(main_layout)

        # main calculator buttons (two-column Apple layout)
        self.create_buttons(main_layout)

    def create_top_bar(self, parent_layout):
        """create the top bar with variables and history button."""
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        # variable chips container
        var_container = QWidget()
        var_container.setObjectName("variableBar")
        var_layout = QHBoxLayout(var_container)
        var_layout.setSpacing(8)

        # Label
        var_label = QLabel("Variables:")
        var_label.setStyleSheet("color: #A0A0A0; font-size: 10pt;")
        var_layout.addWidget(var_label)

        # container for variable buttons (last 5)
        self.variable_buttons_layout = QHBoxLayout()
        self.variable_buttons_layout.setSpacing(6)
        var_layout.addLayout(self.variable_buttons_layout)

        # initially show none message
        self.refresh_variable_display()

        var_layout.addStretch()

        # manage variables button
        manage_btn = QPushButton("Manage")
        manage_btn.setObjectName("manageVarsBtn")
        manage_btn.clicked.connect(self.open_variable_manager)
        var_layout.addWidget(manage_btn)

        top_bar_layout.addWidget(var_container)

        # history toggle button
        history_btn = QPushButton("History ▼")
        history_btn.setObjectName("historyToggle")
        history_btn.clicked.connect(self.toggle_history)
        top_bar_layout.addWidget(history_btn)

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

        # symbolic operation buttons (simplify, expand, etc)
        self.create_symbolic_buttons(parent_layout)

        # main display for results
        self.display = QLabel("0")
        self.display.setObjectName("display")
        self.display.setMinimumHeight(100)
        parent_layout.addWidget(self.display)

    def create_symbolic_buttons(self, parent_layout):
        """create buttons for symbolic operations like simplify, expand, factor, etc"""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(6)
        button_layout.setContentsMargins(0, 5, 0, 5)

        # simplify button
        simplify_btn = QPushButton("Simplify")
        simplify_btn.setObjectName("symbolicBtn")
        simplify_btn.clicked.connect(lambda: self.handle_symbolic_operation('simplify'))
        button_layout.addWidget(simplify_btn)

        # expand button
        expand_btn = QPushButton("Expand")
        expand_btn.setObjectName("symbolicBtn")
        expand_btn.clicked.connect(lambda: self.handle_symbolic_operation('expand'))
        button_layout.addWidget(expand_btn)

        # factor button
        factor_btn = QPushButton("Factor")
        factor_btn.setObjectName("symbolicBtn")
        factor_btn.clicked.connect(lambda: self.handle_symbolic_operation('factor'))
        button_layout.addWidget(factor_btn)

        # solve button
        solve_btn = QPushButton("Solve")
        solve_btn.setObjectName("symbolicBtn")
        solve_btn.clicked.connect(lambda: self.handle_symbolic_operation('solve'))
        button_layout.addWidget(solve_btn)

        # substitute button
        substitute_btn = QPushButton("Substitute")
        substitute_btn.setObjectName("symbolicBtn")
        substitute_btn.clicked.connect(lambda: self.handle_symbolic_operation('substitute'))
        button_layout.addWidget(substitute_btn)

        # plot button
        solve_2_equations_btn = QPushButton("Solve 2 Equations")
        solve_2_equations_btn.setObjectName("symbolicBtn")
        solve_2_equations_btn.clicked.connect(lambda: self.handle_symbolic_operation('solve 2 equations'))
        button_layout.addWidget(solve_2_equations_btn)

        parent_layout.addWidget(button_container)

    def create_history_panel(self, parent_layout):
        """create the history panel (collapsible)."""
        self.history_panel = HistoryPanel()
        self.history_panel.history_item_selected.connect(self.use_history_item)
        self.history_panel.setVisible(False)  # Start hidden
        self.history_panel.setMaximumHeight(200)
        parent_layout.addWidget(self.history_panel)

    def create_buttons(self, parent_layout):
        """Create the button grid with Apple's two-column layout."""
        # Container for buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)

        # left column: scientific functions
        scientific_grid = self.create_scientific_buttons()
        button_layout.addLayout(scientific_grid, 2)  # Takes 2/3 of space

        # right column: number pad + operations
        number_grid = self.create_number_pad()
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
            ("2ⁿᵈ", "scientific"),
            ("x²", "scientific"),
            ("x³", "scientific"),
            ("xʸ", "scientific"),
            ("eˣ", "scientific"),
            ("10ˣ", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row1):
            btn = CalculatorButton(text, btn_type)
            if text == "2ⁿᵈ":
                btn.clicked.connect(lambda: self.handle_special_click("2ⁿᵈ"))
            else:
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
            # map button text to function names
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

        # Row 4: hyperbolic and special
        row4 = [
            ("Rand", "scientific"),
            ("sinh", "scientific"),
            ("cosh", "scientific"),
            ("tanh", "scientific"),
            ("EE", "scientific"),
            ("Rad", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row4):
            btn = CalculatorButton(text, btn_type)
            if text in ["Rand", "EE", "Rad"]:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_special_click(t))
            else:
                btn.clicked.connect(lambda checked=False, t=text: self.handle_scientific_function_click(t))
            grid.addWidget(btn, 4, col)

        return grid

    def create_number_pad(self) -> QGridLayout:
        """Create the right column with number pad and operations."""
        grid = QGridLayout()
        grid.setSpacing(6)

        # Row 0: AC, +/-, %, ÷
        row0 = [
            ("AC", "special"),
            ("±", "special"),
            ("%", "special"),
            ("÷", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row0):
            btn = CalculatorButton(text, btn_type)
            # connect buttons
            if text == "AC":
                btn.clicked.connect(self.handle_clear_click)
            elif text in ["±", "%"]:
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
        grid.addWidget(btn_0, 4, 0, 1, 2)  # Span 2 columns

        btn_dot = CalculatorButton(".", "number")
        btn_dot.clicked.connect(self.handle_decimal_click)
        grid.addWidget(btn_dot, 4, 2)

        btn_equals = CalculatorButton("=", "operation")
        btn_equals.clicked.connect(self.handle_equals_click)
        grid.addWidget(btn_equals, 4, 3)

        return grid

    def open_variable_manager(self):
        """Open the variable management window."""
        var_window = VariableWindow(self.engine, self)
        var_window.variables_changed.connect(self.refresh_variable_display)
        var_window.exec()

        # Refresh variable display after closing
        self.refresh_variable_display()

    def refresh_variable_display(self):
        """Update the variable chips to show the last 5 variables."""
        # Clear existing buttons
        while self.variable_buttons_layout.count():
            item = self.variable_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get variables from engine
        variables = self.engine.list_variables()

        if not variables:
            # Show "None" message
            no_vars = QLabel("None")
            no_vars.setStyleSheet("color: #A0A0A0; font-size: 10pt; font-style: italic;")
            self.variable_buttons_layout.addWidget(no_vars)
        else:
            # Show last 5 variables (most recent)
            var_items = list(variables.items())[-5:]

            for name, value in var_items:
                # create a button for each variable
                btn = QPushButton(f"{name}")
                btn.setObjectName("variableChip")
                btn.setToolTip(f"{name} = {value}")
                # Use lambda with captured variable to avoid late binding issue
                btn.clicked.connect(lambda *, n=name: self.insert_variable(n))
                self.variable_buttons_layout.addWidget(btn)

    def insert_variable(self, var_name: str):
        """Insert a variable name into the current expression."""
        self.current_expression += var_name
        self.expression_input.setText(self.current_expression)

    def toggle_history(self):
        """toggle the history panel visibility."""
        self.history_panel.toggle_visibility()

        # Update button text
        history_btn = self.findChild(QPushButton, "historyToggle")
        if self.history_panel.isVisible():
            history_btn.setText("History ▲")
        else:
            history_btn.setText("History ▼")

    def use_history_item(self, expression: str):
        """Use an expression from history."""
        self.current_expression = expression
        self.expression_input.setText(self.current_expression)

    def handle_expression_input(self):
        """when user types expression and presses enter"""
        # TODO: get text from self.expression_input.text()
        # TODO: use self.engine to parse/simplify
        # TODO: show result in self.display
        pass

    ### button handlers
    # TODO: connect all buttons to these handlers

    def handle_optional_expression_input(self):
        pass

    def connect_button_to_operation(self, button: CalculatorButton, operation_func):
        """helper to connect button to function"""
        button.clicked.connect(operation_func)

    def handle_number_click(self, digit: str):
        """when number buttons (0-9) are clicked"""
        result = self.operations.input_number(digit)
        if result is not None:
            self.expression_input.setText(result)

    def handle_operation_click(self, operation_name: str):
        """when +, -, ×, ÷ buttons clicked"""
        if operation_name == "+":
            result = self.operations.operation_add()
        elif operation_name == "−":
            result = self.operations.operation_subtract()
        elif operation_name == "×":
            result = self.operations.operation_multiply()
        elif operation_name == "÷":
            result = self.operations.operation_divide()

        if result is not None:
            self.expression_input.setText(result)

    def handle_equals_click(self):
        """= button - calculate and show result"""
        result = self.operations.calculate_result()
        if result is not None:
            expression, answer = result
            self.expression_input.setText(expression)
            self.display.setText(answer)
            self.history_panel.add_calculation(expression, answer)

    def handle_clear_click(self):
        """AC button - clear everything"""
        result = self.operations.clear_all()
        if result is not None:
            self.expression_input.setText(result)
            self.display.setText(result)

    def handle_scientific_function_click(self, function_name: str):
        """scientific functions like sin, cos, etc"""
        result = None
        if function_name == "sin":
            result = self.operations.sin()
        elif function_name == "cos":
            result = self.operations.cos()
        elif function_name == "tan":
            result = self.operations.tan()
        elif function_name == "sinh":
            result = self.operations.sinh()
        elif function_name == "cosh":
            result = self.operations.cosh()
        elif function_name == "tanh":
            result = self.operations.tanh()
        elif function_name == "sqrt":
            result = self.operations.square_root()
        elif function_name == "cbrt":
            result = self.operations.cube_root()
        elif function_name == "x²":
            result = self.operations.square()
        elif function_name == "x³":
            result = self.operations.cube()
        elif function_name == "xʸ":
            result = self.operations.power()
        elif function_name == "1/x":
            result = self.operations.reciprocal()
        elif function_name == "eˣ":
            result = self.operations.exp()
        elif function_name == "10ˣ":
            result = self.operations.power_of_10()
        elif function_name == "ln":
            result = self.operations.natural_log()
        elif function_name == "log₁₀":
            result = self.operations.log_base_10()
        elif function_name == "x!":
            result = self.operations.factorial()

        if result is not None:
            self.expression_input.setText(result)

    def handle_decimal_click(self):
        """decimal point button"""
        result = self.operations.input_decimal()
        if result is not None:
            self.expression_input.setText(result)

    def handle_parenthesis_click(self, paren_type: str):
        """parenthesis buttons"""
        if paren_type == "(":
            result = self.operations.open_parenthesis()
        else:
            result = self.operations.close_parenthesis()

        if result is not None:
            self.expression_input.setText(result)

    def handle_constant_click(self, constant: str):
        """constant buttons like e and π"""
        if constant == "e":
            result = self.operations.insert_constant_e()
        elif constant == "π":
            result = self.operations.insert_constant_pi()

        if result is not None:
            self.expression_input.setText(result)

    def handle_memory_click(self, action: str):
        """memory buttons - mc, m+, m-, mr"""
        if action == "mc":
            result = self.operations.memory_clear()
        elif action == "m+":
            result = self.operations.memory_add()
        elif action == "m-":
            result = self.operations.memory_subtract()
        elif action == "mr":
            result = self.operations.memory_recall()

        if result is not None:
            self.expression_input.setText(result)

    def handle_special_click(self, action: str):
        """special buttons - ±, %, Rand, EE, Rad, 2nd"""
        result = None
        if action == "±":
            result = self.operations.plus_minus()
        elif action == "%":
            result = self.operations.percentage()
        elif action == "Rand":
            result = self.operations.random_number()
        elif action == "EE":
            result = self.operations.scientific_notation()
        elif action == "Rad":
            result = self.operations.toggle_angle_mode()
            # update button text to show current mode
            if result:
                for btn in self.findChildren(CalculatorButton):
                    if btn.text() in ["Rad", "Deg"]:
                        btn.setText("Deg" if result == "deg" else "Rad")
            return
        elif action == "2ⁿᵈ":
            result = self.operations.toggle_second_function()

        if result is not None:
            self.expression_input.setText(result)

    def handle_symbolic_operation(self, operation: str):
        try:
            expression_string = self.expression_input.text()
            optional_expression_string = self.optional_expression_input.text()
            if not expression_string:
                return
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
            self.display.setText(result)
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