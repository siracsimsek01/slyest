from ..core.symbolic_engine import SymbolicEngine

import random
class CalculatorOperations:
    """handles all button click operations"""
    def __init__(self, engine: SymbolicEngine):
        self.engine = engine
        self.current_expression = ""
        self.last_result = "0"
        self.memory = 0
        self.angle_mode = "rad"

    # number input
    def input_number(self, digit, current) -> str:
        if current == "0" or current == "":
            current = digit
        else:
            current += digit
        return current

    def input_decimal(self, current) -> str:
        current += "."
        return current

    # basic operations
    def operation(self, selected_operation, current) -> str:
        operation_buttons = {
            "add": " + ",
            "subtract": " - ",
            "multiply": " * ",
            "divide": " / ",
            "equal": " = "
        }
        current += operation_buttons[selected_operation]
        return current

    def symbols(self, symbol, current):
        current += symbol
        return current
    
    def calculate_result(self, inputs) -> tuple[str, str]:
        try:
            if not inputs or inputs == "":
                return None
            original_expression = inputs
            calc_expression = inputs.replace("×", "*")
            calc_expression = calc_expression.replace("÷", "/")
            calc_expression = calc_expression.replace("−", "-")
            if "sin" in calc_expression or "cos" in calc_expression or "tan" in calc_expression:
                result = self.engine.parse_expression(calc_expression).evalf()
            else:
                result = self.engine.parse_expression(calc_expression)
            result_str = str(f"{float(result):.12g}")
            self.last_result = result_str
            return (original_expression, result_str)
        except Exception:
            return (self.current_expression, "Error")

    def clear_all(self) -> str:
        self.current_expression = ""
        self.last_result = ""
        return ""

    def backspace(self, current) -> str:
        return current[:-1]

    def percentage(self, current) -> str:
        return current + "/100"

    def square(self, current) -> str:
        return current + "**2"

    def cube(self, current) -> str:
        return current + "**3"

    def power(self, current) -> str:
        return current + "**"

    def square_root(self, current) -> str:
        return current + "**(1/2)"

    def cube_root(self, current) -> str:
        return current + "**(1/3)"

    def root(self, current) -> str:
        return current + "**(1/"

    def reciprocal(self, current) -> str:
        return "1/(" + current + ")" if current else "1/("

    def exp(self, current) -> str:
        return "exp(" + current + ")" if current else "exp("

    def power_of_10(self, current) -> str:
        return "10**(" + current + ")" if current else "10**("

    def natural_log(self, current) -> str:
        return "log(" + current + ")" if current else "log("

    def log_base_10(self, current) -> str:
        return "log(" + current + ", 10)"

    def sin(self, current) -> str:
        return current + "sin("
    
    def cos(self, current) -> str:
        return current + "cos("

    def tan(self, current) -> str:
        return current + "tan("

    def sinh(self, current) -> str:
        return current + "sinh("

    def cosh(self, current) -> str:
        return current + "cosh("

    def tanh(self, current) -> str:
        return current + "tanh("
   
    def factorial(self, current) -> str:
        return current + "!"

    def insert_constant_e(self, current) -> str:
        return current + "e"

    def insert_constant_pi(self, current) -> str:
        return current + "pi"

    def random_number(self) -> str:
        return str(random.random())

    def open_parenthesis(self, current) -> str:
        return current + "("

    def close_parenthesis(self, current) -> str:
        return current + ")"
  
    def memory_clear(self) -> str:
        self.memory = 0
        return "0"

    def memory_add(self, current) -> str:
        self.memory += float(current)
        return str(self.memory)

    def memory_subtract(self, current) -> str:
        self.memory -= float(current)
        return str(self.memory)

    def memory_recall(self) -> str:
        return str(self.memory)