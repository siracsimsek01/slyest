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
    def input_number(self, digit: str) -> str:
        """handle number button clicks (0-9)
        just append digit to current expression
        """
        if self.current_expression == "0" or self.current_expression == "":
            self.current_expression = digit
        else:
            self.current_expression += digit
        return self.current_expression

    def input_decimal(self) -> str:
        """decimal point button"""
        self.current_expression += "."
        return self.current_expression
        

    # basic operations
    def operation_add(self) -> str:
        """+ button"""
        self.current_expression += " + "
        return self.current_expression

    def operation_subtract(self) -> str:
        """- button"""
        # TODO
        pass

    def operation_multiply(self) -> str:
        """× button"""
        # TODO: append " × " (we convert to * later before calc)
        pass

    def operation_divide(self) -> str:
        """÷ button"""
        # TODO: append " ÷ " (convert to / before calc)
        pass

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
        self.last_result = "0"
        return "0"

    def clear_entry(self) -> str:
        """C button - clear current number only"""
        # TODO: this one's tricky, maybe later
        pass

    def backspace(self) -> str:
        """delete last char"""
        # TODO
        pass

    # special operations
    def plus_minus(self) -> str:
        """± button - toggle sign"""
        # TODO: flip sign of current number
        pass

    def percentage(self) -> str:
        """% button"""
        # TODO: divide by 100
        pass

    # powers and roots
    def square(self) -> str:
        """x² button"""
        # TODO: add "**2" or wrap in parentheses
        pass

    def cube(self) -> str:
        """x³ button"""
        # TODO
        pass

    def power(self) -> str:
        """xʸ button - general power"""
        # TODO: append "**" then wait for next input
        pass

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

    def scientific_notation(self) -> str:
        """EE button - scientific notation like 1.5e8"""
        # TODO
        pass

    # parentheses
    def open_parenthesis(self) -> str:
        """( button"""
        # TODO: append "("
        pass

    def close_parenthesis(self) -> str:
        """) button"""
        # TODO: append ")" if we have matching (
        pass

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

    # mode switching
    def toggle_angle_mode(self) -> str:
        """Rad button - toggle rad/deg"""
        # TODO: flip between "rad" and "deg"
        pass

    def toggle_second_function(self) -> str:
        """2nd button - for inverse functions"""
        # TODO: this is advanced, skip for now
        pass
