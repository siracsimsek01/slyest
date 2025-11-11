
from sympy import *

class TwoLinearEqa:
    def __init__(self):
        pass

    def get_equation_symbols(self, eqa):
        eqa_variable = list()
        symbols = list()
        for char in eqa:
            if char.isalpha():
                eqa_variable.append(char)
                if len(eqa_variable) == 2:
                    break
        for var in eqa_variable:
            symbols.append(Symbol(var))
        return symbols
    
    def split_input(self, input):
        split_input = input.split('=')
        if len(split_input) == 2:
            return split_input
        else:
            return []

    def solve_two_algerbraic_equations(self, eqa_1, eqa_2):
        split_input_1 = self.split_input(eqa_1)
        split_input_2 = self.split_input(eqa_2)
        symbols = self.sol_eqa_input(eqa_1)
        if len(symbols) != 2:
            symbols = self.sol_eqa_input(eqa_2)

        if len(split_input_1) == 2 and len(split_input_2) == 2 and len(symbols) == 2:
            try:
                LHS = simplify(split_input_1[0])
                RHS = simplify(split_input_1[1])
                LHS_2 = simplify(split_input_2[0])
                RHS_2 = simplify(split_input_2[1])

                equ_1 = Eq(LHS, RHS)
                equ_2 = Eq(LHS_2, RHS_2)

                answer = solve((equ_1, equ_2), (symbols[0], symbols[1]))
                return answer
            except Exception as e:
                print('Error in input equation. Please try again.')
                return None
        else:
            print('Error in input equation. Please try again.')
            return None
        
if __name__ == '__main__':
    two_linear_equation_solver = TwoLinearEqa()
    eqa_1 = input("Please enter the first correct format of equation: ")
    eqa_2 = input("Please enter the second correct format of equation: ")
    answers = two_linear_equation_solver.solve_two_algerbraic_equations(eqa_1, eqa_2)
    print(f'Answers: {answers}')