from sympy import sympify, nsimplify, pi, E

def toggle_format(expression_str):
   
    try:
        if not expression_str:
            return ("", False)
        clean_str = expression_str.replace('÷', '/').replace('×', '*').replace('−', '-')
        
        expr = sympify(clean_str)

        if "." in str(clean_str):
            
            result = nsimplify(expr, rational=True, tolerance=1e-7)
            return (str(result), True)
        
        else:
            result = float(expr.evalf())
            
            return (f"{result:.12g}", True)

    except Exception as e:
        return (f"Error: {e}", False)