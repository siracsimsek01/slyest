"""
Helper functions useful little tools that other parts of the program can use.
Think of these as a toolbox
"""
import sympy as sp
from typing import Union


def format_expression(expr: Union[str, sp.Expr], format_type: str = 'unicode') -> str:
    if isinstance(expr, str):
        from core.symbolic_engine import SymbolicEngine
        engine = SymbolicEngine()
        expr = engine.parse_expression(expr)
    # choose the output format
    if format_type == 'unicode':
        return sp.pretty(expr, use_unicode=True)  # Nice symbols like √ and π
    elif format_type == 'latex':
        return sp.latex(expr)  # For LaTeX documents
    elif format_type == 'ascii':
        return sp.pretty(expr, use_unicode=False)  # Plain text only
    else:
        return str(expr)  # default just convert to string


def validate_expression(expression_str: str) -> tuple[bool, str]:
    try:
        from core.symbolic_engine import SymbolicEngine
        engine = SymbolicEngine()
        engine.parse_expression(expression_str)
        return True, ""  
    except Exception as e:
        return False, str(e)  

def get_expression_variables(expression: Union[str, sp.Expr]) -> set:
    if isinstance(expression, str):
        from core.symbolic_engine import SymbolicEngine
        engine = SymbolicEngine()
        expression = engine.parse_expression(expression)
    return {str(symbol) for symbol in expression.free_symbols}
