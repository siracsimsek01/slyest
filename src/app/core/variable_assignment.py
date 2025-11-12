from sympy import sympify

class VariableManager:
    def __init__(self):
        self.variables = {}

    def assign_variable(self, name, expression):
        self.variables[name] = sympify(expression)

    def get_variable(self, name):
        return self.variables.get(name)
    
    def remove_variable(self, name):
        try:
            self.variables.pop(name)
        except KeyError:
            print(f'Variable {name} is not defined yet.')
    
    def replace_variable(self, name, expression):
        try:
            self.variables[name] = sympify(expression)
        except KeyError:
            print(f'Variable {name} is not defined yet.')

if __name__ == '__main__':
    variable_manager = VariableManager()
    variable_manager.assign_variable('a', 'x + 1')
    variable_manager.assign_variable('b', 'x + 2')
    variable_manager.replace_variable('b', 'x**2')
    variable_manager.remove_variable('a')
    print(variable_manager.variables)