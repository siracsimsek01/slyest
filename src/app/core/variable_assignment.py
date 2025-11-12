from sympy import sympify

class VariableManager:
    def __init__(self):
        self.variables = {}

    def assign(self, name: str, expression: str):
        """Assign a symbolic expression to a variable."""
        self.variables[name] = sympify(expression)

    def get(self, name: str):
        """Return a stored expression by variable name."""
        return self.variables.get(name)
