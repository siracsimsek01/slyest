import unittest
from unittest.mock import patch, call

from sympy import *
from algebraic_expressions import AlgebraicExpressions

class TestAlgebraicExpressions(unittest.TestCase):
    def __init__(self):
        self.algebra = AlgebraicExpressions()

    def test_process_user_input_with_valid_expressions(self):
        user_input = 'x**2 - 4 = 0'
        split_input, symbol = self.algebra.process_user_input(user_input)
        assert split_input == ['x**2 - 4 ', ' 0'], 'Incorrect Splitting'
        assert symbol == Symbol('x'), 'Incorrect Symbol'
        print('Success')

    def test_process_user_input_with_invalid_expressions(self):
        user_input = 'a**2 - 4'
        split_input, symbol = self.algebra.process_user_input(user_input)
        assert split_input == [], 'The input is valid.'
        assert symbol == Symbol('a'), 'Incorrect Symbol'
        print('Success')

    def test_solve_equation_with_valid_input(self):
        user_input = 'a**2 - 4 = 0'
        answer = self.algebra.solve_equation(user_input)
        assert answer == [-2, 2], "Answer is wrong."
        print('Success')

    def test_solve_equation_with_invalid_input(self):
        user_input = 'a**2 - 4'
        answer = self.algebra.solve_equation(user_input)
        assert answer == None, "Answer is wrong."
        print('Success')


test = TestAlgebraicExpressions()
test.test_process_user_input_with_valid_expressions()
test.test_process_user_input_with_invalid_expressions()
test.test_solve_equation_with_valid_input()
