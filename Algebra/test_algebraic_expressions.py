import unittest
from unittest.mock import patch, call

from sympy import *
from algebraic_expressions import AlgebraicExpressions

class TestAlgebraicExpressions(unittest.TestCase):
    def __init__(self):
        self.algebra = AlgebraicExpressions()
        self.valid_user_input = 'x**2 - 4 = 0'
        self.invalid_user_input = 'a**2 - 4'

    def run_all_tests(self):
        self.test_process_user_input_with_valid_expressions()
        self.test_process_user_input_with_invalid_expressions()
        self.test_solve_algerbraic_equation_with_valid_input()
        self.test_solve_algerbraic_equation_with_invalid_input()
        print("All tests ran successfully!")

    def test_process_user_input_with_valid_expressions(self):
        split_input, symbol = self.algebra.process_user_input(self.valid_user_input)
        assert split_input == ['x**2 - 4 ', ' 0'], 'Incorrect Splitting'
        assert symbol == Symbol('x'), 'Incorrect Symbol'
        print('>> Test Func: process_user_input, Input: Valid, Result: Success')

    def test_process_user_input_with_invalid_expressions(self):
        split_input, symbol = self.algebra.process_user_input(self.invalid_user_input)
        assert split_input == [], 'The input is valid.'
        assert symbol == Symbol('a'), 'Incorrect Symbol'
        print('>> Test Func: process_user_input, Input: Invalid, Result: Success')

    def test_solve_algerbraic_equation_with_valid_input(self):
        answer = self.algebra.solve_algerbraic_equation(self.valid_user_input)
        assert answer == [-2, 2], "Answer is wrong."
        print('>> Test Func: solve_algerbraic_equation, Input: Valid, Result: Success')

    def test_solve_algerbraic_equation_with_invalid_input(self):
        answer = self.algebra.solve_algerbraic_equation(self.invalid_user_input)
        assert answer == None, "Answer is wrong."
        print('>> Test Func: solve_algerbraic_equation, Input: Invalid, Result: Success')


test_suite = TestAlgebraicExpressions()
test_suite.run_all_tests()