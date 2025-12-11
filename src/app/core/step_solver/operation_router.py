from typing import Dict, List
from .linear_solver import LinearEquationSolver
from .explanation_enhancer import ExplanationEnhancer
from sympy import symbols, simplify, expand, factor, diff
from sympy.parsing.sympy_parser import parse_expr


class OperationRouter:
    def __init__(self, use_enhanced_explanations: bool = True):
        self.linear_solver = LinearEquationSolver()
        self.enhancer = ExplanationEnhancer(api_type="local") if use_enhanced_explanations else None

    def _enhance_result(self, result: Dict, operation: str) -> Dict:
        """apply explanation enhancer to steps"""
        if self.enhancer and result.get('success', False):
            context = {'operation': operation}
            result['steps'] = self.enhancer.enhance_all_steps(result['steps'], context)
        return result

    def generate_steps(self, operation: str, input_expr: str, optional_input: str = "", result="") -> Dict:
        if operation == "solve":
            if ", " in result:
                operation = "solve quadratic"
                result = self._solve_2_answer_steps(input_expr, result)
            else:
                result = self._solve_steps(input_expr, result)
        elif operation == "simplify":
            result = self._simplify_steps(input_expr, result)
        elif operation == "expand":
            result = self._expand_steps(input_expr, result)
        elif operation == "factor":
            result = self._factor_steps(input_expr, result)
        elif operation == "differentiate":
            result = self._differentiate_steps(input_expr, optional_input, result)
        elif operation == "integrate":
            result = self._integrate_steps(input_expr, optional_input, result)
        elif operation == "substitute":
            result = self._substitute_steps(input_expr, optional_input, result)
        elif operation == "solve 2 equations":
            result = self._solve_two_equations_steps(input_expr, optional_input, result)
        elif operation == "calculate":
            result = self._calculate_steps(input_expr, result)
        else:
            return {
                'success': False,
                'error': f'Operation "{operation}" not supported',
                'steps': []
            }

        return self._enhance_result(result, operation)

    def _solve_steps(self, equation: str, result: str) -> Dict:
        return self.linear_solver.solve_with_steps(equation, result)
    
    def _solve_2_answer_steps(self, equation: str, result: str) -> Dict:
        try:
            steps = [
                {
                    'title': 'Given expression',
                    'expression': str(equation),
                    'explanation': 'we need to solve this equation',
                    'rule': 'starting point',
                    'is_final': False
                },
                {
                    'title': 'solve quardratic',
                    'expression': str(result),
                    'explanation': 'Solve the equation',
                    'rule': 'solving linear equation',
                    'is_final': True
                }
            ]

            return {
                'success': True,
                'steps': steps,
                'solution': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _simplify_steps(self, expr: str, result: str) -> Dict:
        try:
            steps = [
                {
                    'title': 'given expression',
                    'expression': str(expr),
                    'explanation': 'we need to simplify this expression',
                    'rule': 'starting point',
                    'is_final': False
                },
                {
                    'title': 'simplified result',
                    'expression': str(result),
                    'explanation': 'combined like terms and simplified',
                    'rule': 'simplification',
                    'is_final': True
                }
            ]

            return {
                'success': True,
                'steps': steps,
                'solution': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _expand_steps(self, expr: str, result: str) -> Dict:
        try:
            from sympy import Mul, Add, Pow
            parsed = parse_expr(expr)
            steps = [
                {
                    'title': 'given expression',
                    'expression': str(expr),
                    'explanation': 'we need to expand this expression',
                    'rule': 'starting point',
                    'is_final': False
                }
            ]

            # Check if it's a binomial multiplication like (a+b)*(c+d)
            if isinstance(parsed, Mul):
                factors = parsed.args

                # Check if we have two binomial factors (like (x+2)*(x+3))
                if len(factors) == 2 and all(isinstance(f, Add) and len(f.args) == 2 for f in factors):
                    # It's a binomial product - show FOIL steps
                    factor1, factor2 = factors
                    a, b = factor1.args
                    c, d = factor2.args

                    # Step: Show what we're multiplying
                    steps.append({
                        'title': 'identify binomial multiplication',
                        'expression': f'({a} + {b})({c} + {d})',
                        'explanation': 'we have two binomials to multiply using FOIL (First, Outer, Inner, Last)',
                        'rule': 'foil_setup',
                        'is_final': False
                    })

                    # FOIL steps
                    first = a * c
                    outer = a * d
                    inner = b * c
                    last = b * d

                    steps.append({
                        'title': 'apply FOIL method',
                        'expression': f'First: ({a})({c}) = {first}\nOuter: ({a})({d}) = {outer}\nInner: ({b})({c}) = {inner}\nLast: ({b})({d}) = {last}',
                        'explanation': 'multiply each pair of terms: First terms, Outer terms, Inner terms, Last terms',
                        'rule': 'foil_multiplication',
                        'is_final': False
                    })

                    # Combine terms
                    steps.append({
                        'title': 'combine all terms',
                        'expression': f'{first} + {outer} + {inner} + {last}',
                        'explanation': 'add all four products together',
                        'rule': 'combine_products',
                        'is_final': False
                    })

                    # Simplify like terms if any
                    if str(result) != f'{first} + {outer} + {inner} + {last}':
                        steps.append({
                            'title': 'combine like terms',
                            'expression': str(result),
                            'explanation': f'simplify by combining terms with the same variable powers',
                            'rule': 'combine_like_terms',
                            'is_final': False
                        })

            # Final result
            steps.append({
                'title': 'expanded result',
                'expression': str(result),
                'explanation': 'final expanded form',
                'rule': 'expansion',
                'is_final': True
            })

            return {
                'success': True,
                'steps': steps,
                'solution': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _factor_steps(self, expr: str, result: str) -> Dict:
        try:
            steps = [
                {
                    'title': 'given expression',
                    'expression': str(expr),
                    'explanation': 'we need to factor this expression',
                    'rule': 'starting point',
                    'is_final': False
                },
                {
                    'title': 'factored result',
                    'expression': str(result),
                    'explanation': 'factored into product form',
                    'rule': 'factorization',
                    'is_final': True
                }
            ]

            return {
                'success': True,
                'steps': steps,
                'solution': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _differentiate_steps(self, expr: str, variable: str, result: str) -> Dict:
        try:
            variable = variable if variable else expr[0]
            steps = [
                {
                    'title': 'given function',
                    'expression': f'f({variable}) = {expr}',
                    'explanation': f'we need to find the derivative with respect to {variable}',
                    'rule': 'starting point',
                    'is_final': False
                },
                {
                    'title': 'differentiate',
                    'expression': f"f'({variable}) = {result}",
                    'explanation': 'applied differentiation rules',
                    'rule': 'differentiation',
                    'is_final': True
                }
            ]

            return {
                'success': True,
                'steps': steps,
                'solution': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _integrate_steps(self, expr: str, variable: str, result: str) -> Dict:
        try:
            variable = variable if variable else expr[0]
            steps = [
                {
                    'title': 'given function',
                    'expression': f'f({variable}) = {expr}',
                    'explanation': f'we need to find the function from its derivative with respect to {variable}',
                    'rule': 'starting point',
                    'is_final': False
                },
                {
                    'title': 'integrate',
                    'expression': f"∫f({variable}) = {result}",
                    'explanation': 'applied integration rules',
                    'rule': 'integration',
                    'is_final': True
                }
            ]

            return {
                'success': True,
                'steps': steps,
                'solution': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _substitute_steps(self, expr: str, substitution: str, result: str) -> Dict:
        try:
            steps = [
                {
                    'title': 'given equation',
                    'expression': f'{expr} with {substitution}',
                    'explanation': f'substitute values: {substitution}',
                    'rule': 'substitution',
                    'is_final': False
                },
                {
                    'title': 'substituted result',
                    'expression': str(result),
                    'explanation': f'substitue {substitution} into the expression',
                    'rule': 'subsitution',
                    'is_final': True
                }
            ]

            return {
                'success': True,
                'steps': steps,
                'solution': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _solve_two_equations_steps(self, eq1: str, eq2: str, result: str) -> Dict:
        try:
            steps = [
                {
                    'title': 'given equation',
                    'expression': f'{eq1} , {eq2}',
                    'explanation': 'solving system of two linear equations',
                    'rule': 'starting point',
                    'is_final': False
                },
                {
                    'title': 'solve 2 equations',
                    'expression': str("".join(i for i in result)),
                    'explanation': 'perform two equations',
                    'rule': 'two linear equation solver',
                    'is_final': True
                }
            ]

            return {
                'success': True,
                'steps': steps,
                'solution': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }

    def _calculate_steps(self, expr: str, result: str) -> Dict:
        try:
            parsed = parse_expr(expr)
            steps = [
                {
                    'title': 'given expression',
                    'expression': str(parsed),
                    'explanation': 'evaluate this arithmetic expression',
                    'rule': 'starting point',
                    'is_final': False
                }
            ]

            if '+' in expr or '-' in expr or '*' in expr or '/' in expr:
                if parsed.is_Add:
                    terms = str(parsed).split(' + ')
                    if len(terms) > 1:
                        steps.append({
                            'title': 'identify operation',
                            'expression': str(parsed),
                            'explanation': f'this is an addition operation with {len(terms)} terms',
                            'rule': 'operation identification',
                            'is_final': False
                        })
                elif parsed.is_Mul:
                    steps.append({
                        'title': 'identify operation',
                        'expression': str(parsed),
                        'explanation': 'this is a multiplication operation',
                        'rule': 'operation identification',
                        'is_final': False
                    })

            steps.append({
                'title': 'calculate result',
                'expression': str(result),
                'explanation': f'performing the calculation gives us {result}',
                'rule': 'arithmetic evaluation',
                'is_final': True
            })

            return {
                'success': True,
                'steps': steps,
                'solution': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': []
            }
