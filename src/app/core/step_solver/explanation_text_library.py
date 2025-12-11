class ExplanationTexts:
    def __init__(self):
       self.expr = ""
       self.n = 0
       self.explanation = {
            "calculate": (f"We start with the expression {self.expr}. Our goal is to evaluate this step-by-step by "
                       f"following the order of operations (PEMDAS/BODMAS): Parentheses/Brackets first, "
                       f"then Exponents/Orders, followed by Multiplication and Division (left to right), "
                       f"and finally Addition and Subtraction (left to right)."),
            "solve": (f"We begin with the equation {self.expr}. The goal of solving an equation is to find "
                       f"the value(s) of the unknown variable that make the equation true. We'll do this "
                       f"by performing valid algebraic operations on both sides to isolate the variable, "
                       f"always maintaining the equality."),
            "simplify": (f"We start with {self.expr}. Simplification means reducing the expression to its most "
                       f"compact form by combining like terms (terms with the same variables and powers) "
                       f"and reducing fractions where possible. The simplified form is easier to work with "
                       f"and reveals the structure more clearly."),
            "expand": (f"We begin with {self.expr}. Expanding means removing parentheses by applying the "
                       f"distributive property (a(b+c) = ab + ac). This transforms a factored form into "
                       f"a sum of terms, which can be useful for further operations."),
            "factor": (f"Starting with {self.expr}, we'll factor it into a product of simpler expressions. "
                       f"Factoring is the reverse of expanding and helps us find zeros, simplify fractions, "
                       f"and solve equations more easily."),
            "differentiate": (f"We have the function {self.expr}. Differentiation finds the rate of change - how the "
                       f"output changes as the input changes. The derivative tells us the slope of the tangent "
                       f"line at any point on the function's graph."),
            "integrate": (f"We are working with the expression {self.expr}. Integration is the reverse of differentiation — "
                        f"it finds the accumulated area under the curve of a function. "
                        f"By integrating, we determine a new function whose derivative gives us the original expression."),
            "substitute": (f"We start with the expression {self.expr}. Substitution means replacing the variable with a "
                        f"specific value. This allows us to compute the numerical result of the expression "
                        f"when the variable is set to that value."),
            "solve 2 equations": (f"We are working with the system {self.expr}. Solving two equations with two unknowns means finding "
                        f"the values of the variables that satisfy *both* equations at the same time. "
                        f"This is done by eliminating one variable or substituting one equation into the other. "
                        f"The solution gives the point where the two equations intersect."),
            "solve quadratic": (f"We are solving the quadratic equation {self.expr}. A quadratic equation can have up to two "
                        f"solutions because it is based on a squared term. These solutions come from the quadratic "
                        f"formula, factoring, or completing the square. Both solutions are valid as long as they "
                        f"satisfy the original equation."),
            "calculate result": ("After carefully performing the operation and following the rules of arithmetic, "
                   "we arrive at the final numeric result. Always double-check your arithmetic to avoid "
                   "calculation errors!"),
            "identify: add": (f"This expression involves addition with {self.n} terms. Addition is commutative "
                       f"(a+b = b+a) and associative ((a+b)+c = a+(b+c)), meaning we can add in any order. "
                       f"We'll compute the sum by adding the terms together."),
            "identify: multiply": ("This step involves multiplication. Multiplication represents repeated addition "
                       "and is also commutative (a×b = b×a) and associative. We'll multiply the factors "
                       "together to get the product."),
            "identify: divide": ("This is a division operation. Division asks 'how many times does the divisor fit "
                       "into the dividend?' Remember that division by zero is undefined, and dividing by "
                       "fractions means multiplying by their reciprocal."),
            "identify: subtract": ("This involves subtraction, which computes the difference between two numbers. "
                       "Unlike addition, subtraction is not commutative (a-b ≠ b-a), so order matters!"),
            "identify: default": "We identify the mathematical operation to determine how to proceed with the calculation.",
            "operation: default": f"Starting from {self.expr}, we'll work through this step-by-step.",
            "simplify: combine-if": ("We combine like terms - these are terms that have exactly the same variable parts. "
                       "For example, 2x and 3x are like terms (both have 'x'), so 2x + 3x = 5x. "
                       "Constants (numbers without variables) are also like terms with each other. "
                       "We can only combine coefficients of like terms, not unlike terms."),
            "simplify: combine-else": ("We simplify by combining like terms, canceling common factors in fractions, "
                   "and reducing the expression to its simplest form. This makes the expression "
                   "cleaner and easier to understand while keeping its mathematical value unchanged."),
            "foil: identify": ("This is a binomial multiplication - we have two expressions with two terms each. "
                       "We'll use the FOIL method: multiply First terms, then Outer terms, then Inner terms, "
                       "and finally Last terms. FOIL is a systematic way to ensure we don't miss any products."),
            "foil: apply": ("Using FOIL, we multiply:\n"
                       "• First: the first term from each binomial\n"
                       "• Outer: the outer terms (first from first binomial, last from second)\n"
                       "• Inner: the inner terms (last from first binomial, first from second)\n"
                       "• Last: the last term from each binomial\n"
                       "This gives us four separate products that we'll combine next."),
            "combine all terms": ("Now we write out all four products from FOIL as a sum. These are the pieces "
                   "we'll put together to form our expanded expression."),
            "expand: title": ("We apply the distributive property: a(b + c) = ab + ac. This means we multiply "
                   "each term inside the parentheses by the term outside. After distributing, we "
                   "often need to combine like terms to complete the expansion."),
            "factor: title": ("We factor by finding common factors among terms or recognizing special patterns "
                   "like difference of squares (a² - b² = (a+b)(a-b)) or perfect square trinomials. "
                   "Factoring is the reverse of expanding and reveals the multiplicative structure."),
            "divide: title": ("We divide both sides by the same non-zero number to maintain equality. "
                   "This is valid because dividing equal quantities by the same amount gives equal results. "
                   "This step helps us isolate the variable."),
            "subtract: title":  ("We subtract the same value from both sides of the equation. This is valid by the "
                   "subtraction property of equality: if a = b, then a - c = b - c. This helps us "
                   "move terms to isolate the variable."),
            "solution: title": ("This is our final answer. We've isolated the variable and found its value. "
                   "It's good practice to verify by substituting this value back into the original "
                   "equation to check that it works!"),
            "default": "We apply the relevant mathematical rules and properties to progress toward our solution.",
        }

       self.hints = {
            "solve": "💡 Tip: Your goal is to get the variable alone on one side of the equals sign. Whatever you do to one side, do to the other!",
            "simplify": "💡 Tip: Your goal is to get the variable alone on one side of the equals sign. Whatever you do to one side, do to the other!",
            "expand": "💡 Tip: Use FOIL (First, Outer, Inner, Last) for binomial multiplication, or distribute systematically term by term.",
            "factor": "💡 Tip: Look for common factors first, then check for special patterns like x² - y² or perfect squares.",
            "substitute": "💡 Tip: Replace the variable with the given value carefully, then simplify step by step to avoid mistakes.",
            "differentiate": "💡 Tip: Apply the power rule, product rule, or chain rule as needed. Focus on how each term changes with respect to x.",
            "integrate": "💡 Tip: Look for functions you recognize as derivatives of something simpler. Reverse the differentiation rules to find the antiderivative.",
            "solve quadratic": "💡 Tip: Set the equation equal to zero. Check whether factoring works; if not, use the quadratic formula.",
            "solve 2 equations": "💡 Tip: Try eliminating one variable or substitute one equation into the other. Make both equations share only one unknown at a time.",
            "simplify: title": "💡 Tip: Only combine like terms! Terms must have identical variable parts (including powers) to be combined.",
            "identify: title": "💡 Tip: Understanding what operation we're doing helps us choose the right strategy and apply the correct properties.",
            "divide: title": "💡 Tip: Remember to divide EVERY term on both sides, and never divide by zero!",
            "subtract: title": "💡 Tip: Watch out for signs! Subtracting a negative is the same as adding a positive.",
            "solution: title": "💡 Tip: Check your answer by plugging it back into the original equation - both sides should be equal!"
        }

       self.warnings = {
            "solve": "⚠️ Common Mistake: Don't forget to check your solution! Substitute it back into the original equation to verify.",
            "simplify": "⚠️ Common Mistake: Don't combine unlike terms! For example, 2x + 3y cannot be simplified to 5xy. The variables must match exactly.",
            "expand": "⚠️ Common Mistake: When distributing, don't forget to multiply the sign! For example: -2(x - 3) = -2x + 6, not -2x - 6.",
            "factor": "⚠️ Common Mistake: Make sure to divide ALL terms on both sides, not just one term. Also, never divide by a variable that could be zero!",
            "substitute": "⚠️ Common Mistake: Make sure to substitute the value into every instance of the variable. Forgetting some occurrences leads to incorrect results.",
            "differentiate": "⚠️ Common Mistake: Remember to apply all derivative rules properly (product, quotient, chain). Missing a rule often causes wrong answers.",
            "integrate": "⚠️ Common Mistake: Don’t forget the constant of integration when finding indefinite integrals. Also, be careful with substitution and variable changes.",
            "calculate": "⚠️ Common Mistake: Follow the order of operations (PEMDAS/BODMAS)! Don't just work left to right.",
            "subtract": "⚠️ Common Mistake: Be careful with signs! When moving terms across the equals sign, the sign changes.",
            "divide": "⚠️ Common Mistake: Make sure to divide ALL terms on both sides, not just one term. Also, never divide by a variable that could be zero!",
        }

       self.follow_up = {
             "solve": "🤔 Think About: What happens if you add 5 to both sides of the original equation? Would you get the same solution?",
             "simplify": "🤔 Think About: Could you simplify this expression a different way and still get the same answer?",
             "factor": "🤔 Think About: What are the zeros of this factored expression? (Hint: when does each factor equal zero?)",
             "expand": "🤔 Think About: Can you factor the expanded form back to the original? This confirms you did it correctly!",
             "solve: given": "🤔 Think About: Before solving, can you estimate roughly what value the variable might be?",
             "simplify: title": "🤔 Think About: Why can we combine like terms but not unlike terms? What makes terms 'like'?"
        }
       
        
    def get_explanation(self, title):
        try:
              return self.explanation[title]
        except:
            return None
    
    def get_explanation_with_expression(self, title, expression):
        self.expr = expression
        try:
              return self.explanation[title]
        except:
            return None
    
    def get_explanation_with_n(self, title, n):
        self.n = n
        try:
              return self.explanation[title]
        except:
            return None
    
    def get_hints(self, title):
       try:
              return self.hints[title]
       except:
            return None
    
    def get_warnings(self, title):
       try:
              return self.warnings[title]
       except:
            return None
       
    def get_follow_ups(self, title):
       try:
              return self.follow_up[title]
       except:
            return None