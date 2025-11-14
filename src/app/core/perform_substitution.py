import sympy
from sympy.parsing.sympy_parser import parse_expr

def perform_substitution(expression_str, substitutions_dict):
    
    if not isinstance(expression_str, str) or not expression_str.strip():
        return ("Error: No expression provided.", False)
    
    if not isinstance(substitutions_dict, dict):
        return ("Error: Invalid substitution format.", False)

    try:
        
        expr = parse_expr(expression_str)

        sym_subs = {}
        for var_name, sub_value in substitutions_dict.items():
            
            if not str(var_name).isidentifier():
                return (f"Error: Invalid variable name '{var_name}'.", False)
            
            sub_value_str = str(sub_value)
            
         
            sub_value_sym = parse_expr(sub_value_str)

            var_symbol = sympy.symbols(var_name)
            
            sym_subs[var_symbol] = sub_value_sym

        new_expr = expr.subs(sym_subs)

        return (str(new_expr), True)

    except (sympy.SympifyError, TypeError, SyntaxError):
        return ("Error: Invalid mathematical expression.", False)
    except Exception as e:
        return (f"Error: An unexpected error occurred: {e}", False)