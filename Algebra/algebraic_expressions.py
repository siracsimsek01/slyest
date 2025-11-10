from sympy import *

class AlgebraicExpressions:
    def __init__(self):
        pass

    def process_user_input(self, user_input):
        for char in user_input:
            if char.isalpha():
                equation_symbol = char
                break
        symbol = Symbol(equation_symbol)
        split_input = user_input.split('=')
        if len(split_input) == 2:
            return split_input, symbol
        print('The equation must include "=" and must include both sides to solve.')
        return [], symbol
    
    def solve_algerbraic_equation(self, user_input):
        split_input, symbol = self.process_user_input(user_input)
        if len(split_input) == 2 and symbol:
            try:
                LHS = simplify(split_input[0])
                RHS = simplify(split_input[1])
                equation = Eq(LHS, RHS)
                answer = solve(equation, symbol)
                return answer
            except:
                print('Error in input equation. Please try again.')
        else:
            print('Error in input equation. Please try again.')

if __name__ == '__main__':
    algebraic_exp = AlgebraicExpressions()
    user_input = input('Please type the expression - Eg; x**2 - 15 = 1\nYour input: ')
    answers = algebraic_exp.solve_algerbraic_equation(user_input)
    print(f'Answers: {answers}')