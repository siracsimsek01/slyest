import unittest
from app.core.two_linear_equations import TestTwoLinearEqa
from unittest.mock import patch, call

class TestTwoLinearEqa(unittest.TestCase):
    def __init__(self):
        self.linear_solver = TwoLinearEqa()
        self.x = Symbol('x')
        self.y = Symbol('y')
       
        self.eqa_1_valid = '2*x + y = 8'
        self.eqa_2_valid = 'x - y = 1'

        self.eqa_1_invalid = '123456'
        self.eqa_2_invalid = 'x - y'

    def run_all_tests(self):
        self.test_sol_eqa_input_with_valid_expressions()
        self.test_sol_eqa_input_with_invalid_expressions()
        self.test_solve_two_algerbraic_equations_with_valid_input()
        self.test_solve_two_algerbraic_equations_with_invalid_input()


    def test_sol_eqa_input_with_valid_expressions(self):
        symbols = self.linear_solver.sol_eqa_input(self.eqa_1_valid)
        assert symbols == [self.x, self.y ], 'Incorrect splitting of equation.'
        print('>> Test Func: sol_eqa_input, Input: Valid, Result: Success')

    def test_sol_eqa_input_with_invalid_expressions(self):
        symbols = self.linear_solver.sol_eqa_input(self.eqa_1_invalid)
        assert symbols == [], 'Incorrect symbol.'
        print('>> Test Func: sol_eqa_input, Input: Invalid, Result: Success')

    def test_solve_two_algerbraic_equations_with_valid_input(self):
        answer = self.linear_solver.solve_two_algerbraic_equations(self.eqa_1_valid, self.eqa_2_valid)
        assert answer == {self.x: 3, self.y: 2}, "Answer is wrong."
        print('>> Test Func: solve_two_algerbraic_equations, Input: Valid, Result: Success')

    def test_solve_two_algerbraic_equations_with_invalid_input(self):
        answer = self.linear_solver.solve_two_algerbraic_equations(self.eqa_1_invalid, self.eqa_2_invalid)
        assert answer is None, 'Invalid input.'
        print('>> Test Func: solve_two_algerbraic_equations, Input: Invalid, Result: Success')


test_suite = TestTwoLinearEqa()
test_suite.run_all_tests()
