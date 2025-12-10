"""
This file handles all the math calculations using SymPy library.
Think of it as the brain that does all the symbolic math work.
"""

from typing import Union, Dict, Any
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy import Derivative 
from sympy import diff, sin, exp 
from sympy.abc import x,y 
from sympy import Symbol, sympify
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

    def simplify(self, expr: Union[str, sp.Expr]) -> sp.Expr:
        """simplify the expression."""
        if isinstance(expr, str):
            expr = self.parse_expression(expr)
        return sp.simplify(expr)
    
    def expand(self, expr: Union[str, sp.Expr]) -> sp.Expr:
        """expand the expression."""
        if isinstance(expr, str):
            expr = self.parse_expression(expr)
        return sp.expand(expr)
    
    def factor(self, expr: Union[str, sp.Expr]) -> sp.Expr:
        """factor the expression."""
        if isinstance(expr, str):
            expr = self.parse_expression(expr)
        return sp.factor(expr)
    
    def substitute(self, expr: Union[str, sp.Expr], substitutions: Dict[str, Any]) -> sp.Expr:
        """substitute variables in the expression."""
        if isinstance(expr, str):
            expr = self.parse_expression(expr)
        subs_dict = {sp.Symbol(k): v for k, v in substitutions.items()}
        return expr.subs(subs_dict)
    
    def solve(self, equation: Union[str, sp.Expr], variable: str = None) -> list:
        """ solve an equation to find waht value makes it true"""
        if isinstance(equation, str):
            if '=' in equation:
                # split into left and right
                lhs, rhs = equation.split('=')
                lhs_expr = self.parse_expression(lhs.strip())
                rhs_expr = self.parse_expression(rhs.strip())
                equation = sp.Eq(lhs_expr, rhs_expr)
            else:
                equation = self.parse_expression(equation)
                
            if variable:
                var = sp.Symbol(variable)
            else:
                free_symbols = equation.free_symbols
                if len(free_symbols) == 1:
                    var = list(free_symbols)[0]
                elif len(free_symbols) == 0:
                    raise ValueError("No variables found in equation")
                else:
                    raise ValueError(f"Multiple variables found: {free_symbols}. Please specify which one to solve for.")
                
                return sp.solve(equation, var)
            
    def assign_variable(self, name: str, expr: Union[str, sp.Expr]) -> sp.Expr:
        """assign a variable to an expression."""
        if isinstance(expr, str):
            expr = self.parse_expression(expr)
        self.variables[name] = expr
        return expr
    
    def get_variable(self, name: str) -> sp.Expr:
        """get the value of a variable."""
        if name not in self.variables:
            raise KeyError(f"Variable '{name}' is not defined.")
        return self.variables[name]
    
    def list_variables(self) -> Dict[str, sp.Expr]:
        
        return self.variables.copy()
    
    def replace_variables(self, expression, action):
        if len (expression.split(",")) == 2:
            return expression
        for name, value in self.variables.items():
            expression = expression.replace(name, f"({value})")
        if action in ["expand", "simplify", "factor"]:
            return sp.sympify(expression, locals=self.variables)
        return expression
    
    def differentiate(self, expr, optional_expression_input):
        if not optional_expression_input:
            var = Symbol(self.find_symbol(expr))
            return diff(expr, var)
        elif optional_expression_input.isalpha() and len(optional_expression_input) == 1:
            var = Symbol(optional_expression_input)
            return diff(expr, var)
        else:
            return "Enter only one variable."   
    def find_symbol(self, expr):
         for char in expr:
            if char.isalpha():
                return char     