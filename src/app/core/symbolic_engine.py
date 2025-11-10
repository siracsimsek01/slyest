"""
This file handles all the math calculations using SymPy library.
Think of it as the brain that does all the symbolic math work.
"""

from typing import Union, Dict, Any
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class SymbolicEngine:
    # This is our main calculator class that does all the symbolic math.
    def __init__(self):
        
        self.variables: Dict[str, sp.Expr] = {}  # Store user-defined variables
        self.transformations = (standard_transformations + (implicit_multiplication_application,)) # Allow implicit multiplication like 2x
        
    def parse_expression(self, expr_str: str) -> sp.Expr:
        try:
            # SymPy reads the expression and turns it into math it can work with
            return parse_expr(expr_str, transformations=self.transformations)
        except Exception as e:
            # If something went wrong, tell the user what happened
            raise ValueError(f"Failed to parse expression: {str(e)}")
