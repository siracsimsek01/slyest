from sympy import sympify

class VariableManager:
    def __init__(self):
        self.variables = {}

    def assign_variable(self, name, expression):
        self.variables[name] = sympify(expression)

    def get_variable(self, name):
        return self.variables.get(name)
    
    def remove_variable(self, name):
        return self.variables.pop(name, None)
    
    def replace_variable(self, name, new_expression):
        if name in self.variables:
            self.variables[name] = sympify(new_expression)
            return True
        return False  
    
    def replace_variables(self, expression):
        for name, value in self.variables.items():
            expression = expression.replace(name, f"({value})")
        return sympify(expression, locals=self.variables)


if __name__ == '__main__':
    variable_manager = VariableManager()
    variable_manager.assign_variable('a', 'x + 1')
    variable_manager.assign_variable('b', 'x + 2')
    variable_manager.replace_variable('b', 'x**2')
    variable_manager.remove_variable('a')
    print(variable_manager.variables)