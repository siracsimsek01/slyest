from sympy import *

class TwoLinearEquations:
    def __init__(self):
        pass

    def get_equation_symbols(self, equation):
        equation_variables = list()
        for char in equation:
            if char.isalpha():
                equation_variables.append(Symbol(char))
                if len(equation_variables) == 2:
                    break
        return equation_variables
    
    def split_input(self, input):
        split_input = input.split('=')
        if len(split_input) == 2:
            return split_input
        else:
            return []

    def solve_two_linear_equations(self, equation_1, equation_2):
        split_input_1 = self.split_input(equation_1)
        split_input_2 = self.split_input(equation_2)
        symbols = self.get_equation_symbols(equation_1)
        if len(symbols) != 2:
            symbols = self.get_equation_symbols(equation_2)

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
    two_linear_equation_solver = TwoLinearEquations()
    equation_1 = input("Please enter the first correct format of equation: ")
    equation_2 = input("Please enter the second correct format of equation: ")
    answers = two_linear_equation_solver.solve_two_linear_equations(equation_1, equation_2)
    print(f'Answers: {answers}')