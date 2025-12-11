from typing import List, Dict, Optional
from sympy import symbols, Eq, solve, simplify
from sympy.parsing.sympy_parser import parse_expr
import re

class LinearEquationSolver:    
    def __init__(self):
        self.steps = []
        
    def solve_with_steps(self, equation_str: str, result: str) -> Dict:
        self.steps = []
        
        try:
            # parse equation
            if '=' in equation_str:
                lhs_str, rhs_str = equation_str.split('=')
                lhs = parse_expr(lhs_str.strip())
                rhs = parse_expr(rhs_str.strip())
            else:
                raise ValueError("not an equation")
            
            #  original equation
            self._add_step(
                title="given equation",
                expression_left=str(lhs),
                expression_right=str(rhs),
                explanation="we need to isolate the variable",
                rule="starting point"
            )
            
            # detect variable
            variables = lhs.free_symbols | rhs.free_symbols
            if not variables:
                return self._no_variable_case(lhs, rhs)
            
            var = list(variables)[0]
            
            # analyze structure and generate steps
            current_lhs, current_rhs = lhs, rhs
            
            #  move constants from left to right
            current_lhs, current_rhs = self._move_constants_to_right(
                current_lhs, current_rhs, var
            )
            
            #  move variables from right to left
            current_lhs, current_rhs = self._move_variables_to_left(
                current_lhs, current_rhs, var
            )
            
            #  simplify both sides
            current_lhs = simplify(current_lhs)
            current_rhs = simplify(current_rhs)
            
            if current_lhs != lhs or current_rhs != rhs:
                self._add_step(
                    title="simplify both sides",
                    expression_left=str(current_lhs),
                    expression_right=str(current_rhs),
                    explanation="combine like terms",
                    rule="simplification"
                )
            
            #    divide by coefficient
            coefficient = current_lhs.as_coefficient(var)
            if coefficient and coefficient != 1:
                current_lhs = current_lhs / coefficient
                current_rhs = current_rhs / coefficient
                
                self._add_step(
                    title=f"divide both sides by {coefficient}",
                    expression_left=str(simplify(current_lhs)),
                    expression_right=str(simplify(current_rhs)),
                    explanation=f"isolate {var} by dividing both sides by its coefficient",
                    rule="division property of equality"
                )
            
            # final answer
            solution = solve(Eq(lhs, rhs), var)
            self._add_step(
                title="solution",
                expression_left=str(var),
                expression_right=str(solution[0]) if solution else "no solution",
                explanation=f"the value of {var} is {solution[0] if solution else 'undefined'}",
                rule="final answer",
                is_final=True
            )
            
            return {
                'success': True,
                'steps': self.steps,
                'solution': solution[0] if solution else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }
    
    def _move_constants_to_right(self, lhs, rhs, var):
        from sympy import Add
        
        # get constant terms on left side
        if lhs.is_Add:
            constants = [term for term in Add.make_args(lhs) if not term.has(var)]
            if constants:
                constant_sum = sum(constants)
                new_lhs = lhs - constant_sum
                new_rhs = rhs - constant_sum
                
                self._add_step(
                    title=f"subtract {constant_sum} from both sides" if constant_sum > 0 else f"add {str(constant_sum)[1:]} to both sides",
                    expression_left=str(simplify(new_lhs)),
                    expression_right=str(simplify(new_rhs)),
                    explanation=f"remove constant term to isolate terms with {var}",
                    rule="subtraction property of equality"
                )
                
                return new_lhs, new_rhs
        
        return lhs, rhs
    
    def _move_variables_to_left(self, lhs, rhs, var):
        from sympy import Add
        
        # check if rhs has variable terms
        if rhs.has(var):
            if rhs.is_Add:
                var_terms = [term for term in Add.make_args(rhs) if term.has(var)]
                if var_terms:
                    var_sum = sum(var_terms)
                    new_lhs = lhs - var_sum
                    new_rhs = rhs - var_sum
                    
                    self._add_step(
                        title=f"subtract {var_sum} from both sides" if var_sum > 0 else f"add {str(var_sum)[1:]} to both sides",
                        expression_left=str(simplify(new_lhs)),
                        expression_right=str(simplify(new_rhs)),
                        explanation=f"move all {var} terms to left side",
                        rule="subtraction property of equality"
                    )
                    
                    return new_lhs, new_rhs
        
        return lhs, rhs
    
    def _add_step(self, title: str, expression_left: str, expression_right: str,
                  explanation: str, rule: str, is_final: bool = False):
        """add a step to the solution"""
        step = {
            'title': title,
            'expression': f"{expression_left} = {expression_right}",
            'explanation': explanation,
            'rule': rule,
            'is_final': is_final
        }
        self.steps.append(step)
    
    def _no_variable_case(self, lhs, rhs):
        """handle case where there's no variable"""
        result = simplify(lhs - rhs)
        if result == 0:
            return {
                'success': True,
                'steps': [{
                    'title': 'identity',
                    'expression': f"{lhs} = {rhs}",
                    'explanation': 'this equation is always true',
                    'rule': 'identity',
                    'is_final': True
                }],
                'solution': 'all real numbers'
            }
        else:
            return {
                'success': True,
                'steps': [{
                    'title': 'contradiction',
                    'expression': f"{lhs} ≠ {rhs}",
                    'explanation': 'this equation is never true',
                    'rule': 'contradiction',
                    'is_final': True
                }],
                'solution': 'no solution'
            }