from ..core.symbolic_engine import SymbolicEngine

class CalculatorOperations:
    """handles all button click operations"""

    def __init__(self, engine: SymbolicEngine):
        self.engine = engine
        self.current_expression = ""
        self.last_result = "0"
        self.memory = "0"
        self.angle_mode = "rad"  # or "deg"

    # number input
    def input_number(self, digit, current) -> str:
        """handle number button clicks (0-9)
        just append digit to current expression
        """
        if current == "0" or current == "":
            current = digit
        else:
            current += digit
        return current

    def input_decimal(self, current) -> str:
        """decimal point button"""
        current += "."
        return current
        

    # basic operations
    def operation(self, selected_operation, current) -> str:
        operation_buttons = {
            "add": " + ",
            "subtract": " - ",
            "multiply": " * ",
            "divide": " ÷ ",
            "equal": " = "
        }
        current += operation_buttons[selected_operation]
        return current

    def symbols(self, symbol, current):
        current += symbol
        return current
    
    # equals and clear
    def calculate_result(self) -> tuple[str, str]:
        """= button - most important one
        returns (expression, result)
        """
        try:
            if not self.current_expression or self.current_expression == "":
                return None

            
            original_expression = self.current_expression

            # Replace calculator symbols with Python/SymPy compatible ones
            calc_expression = self.current_expression.replace("×", "*")
            calc_expression = calc_expression.replace("÷", "/")
            calc_expression = calc_expression.replace("−", "-")

            
            result = self.engine.parse_expression(calc_expression)
            result_str = str(result)

      
            self.last_result = result_str
            self.current_expression = ""

            return (original_expression, result_str)
        except Exception:
            return (self.current_expression, "Error")

    def clear_all(self) -> str:
        """AC button - reset everything"""
        self.current_expression = ""
        self.last_result = ""
        return ""

    def backspace(self, current) -> str:
        return current[:-1]

    def percentage(self) -> str:
        """% button"""
        # TODO: divide by 100
        pass

    # powers and roots
    def square(self, current) -> str:
        return current + "**2 "

    def cube(self, current) -> str:
        return current + "**3 "

    def power(self, current) -> str:
        return current + "**"

    def square_root(self) -> str:
        """√ button"""
        # TODO: use sqrt() from sympy
        pass

    def cube_root(self) -> str:
        """³√ button"""
        # TODO
        pass

    def reciprocal(self) -> str:
        """1/x button"""
        # TODO: 1/current_number
        pass

    # exponentials and logs
    def exp(self) -> str:
        """eˣ button"""
        # TODO: use exp() from sympy
        pass

    def power_of_10(self) -> str:
        """10ˣ button"""
        # TODO
        pass

    def natural_log(self) -> str:
        """ln button"""
        # TODO: use log() from sympy
        pass

    def log_base_10(self) -> str:
        """log₁₀ button"""
        # TODO
        pass

    # trig functions
    def sin(self) -> str:
        """sin button - check angle_mode (rad/deg)"""
        # TODO: convert to radians if in deg mode
        pass

    def cos(self) -> str:
        """cos button"""
        # TODO
        pass

    def tan(self) -> str:
        """tan button"""
        # TODO
        pass

    def sinh(self) -> str:
        """sinh button - hyperbolic"""
        # TODO
        pass

    def cosh(self) -> str:
        """cosh button"""
        # TODO
        pass

    def tanh(self) -> str:
        """tanh button"""
        # TODO
        pass

    # special functions
    def factorial(self) -> str:
        """x! button"""
        # TODO: use factorial() from sympy
        pass

    def insert_constant_e(self) -> str:
        """e button - euler's number"""
        # TODO: append "e" to expression
        pass

    def insert_constant_pi(self) -> str:
        """π button"""
        # TODO: append "pi"
        pass

    def random_number(self) -> str:
        """Rand button"""
        # TODO: use random.random()
        pass


    # parentheses
    def open_parenthesis(self, current) -> str:
        return current + "("

    def close_parenthesis(self, current) -> str:
        return current + ")"

    # memory functions
    def memory_clear(self) -> str:
        """mc button"""
        # TODO: set self.memory = "0"
        pass

    def memory_add(self) -> str:
        """m+ button"""
        # TODO: add current to memory
        pass

    def memory_subtract(self) -> str:
        """m- button"""
        # TODO: subtract current from memory
        pass

    def memory_recall(self) -> str:
        """mr button"""
        # TODO: insert memory value
        pass


    def toggle_second_function(self) -> str:
        """2nd button - for inverse functions"""
        # TODO: this is advanced, skip for now
        pass
