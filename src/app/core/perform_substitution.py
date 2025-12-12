import sympy
from sympy.parsing.sympy_parser import parse_expr

class Substitution:
    def __init__(self):
        pass

    def perform_substitution(self, expression_str, substitutions_dict):
        if not isinstance(expression_str, str) or not expression_str.strip():
            return "Error: No expression provided."
        if not isinstance(substitutions_dict, dict):
            return "Invalid substitution format"
        try:
            expression = parse_expr(expression_str)
            substitution_dict = {}
            for variable_name, substitution_value in substitutions_dict.items():
                if not str(variable_name).isidentifier():
                    return "Invalid substitution symbol"
                substitution_value = str(substitution_value)
                substitution_value = parse_expr(substitution_value)
                variable_symbol = sympy.symbols(variable_name)
                substitution_dict[variable_symbol] = substitution_value
            result = expression.subs(substitution_dict)
            return str(result)
        except (sympy.SympifyError, TypeError, SyntaxError):
            return "Invalid mathematical expression"
        except Exception as e:
            return "Error: An expected error occured."