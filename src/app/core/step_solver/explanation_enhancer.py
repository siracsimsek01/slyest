import os
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

try:
    # modern OpenAI SDK
    from openai import OpenAI
    _openai_available = True
except Exception:
    _openai_available = False


@dataclass
class ExplainOutput:
    explanation: str
    hint: Optional[str] = None
    common_mistake: Optional[str] = None
    follow_up: Optional[str] = None

    def to_dict(self) -> Dict:
        # drop None fields
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


class ExplanationEnhancer:
    def __init__(self, api_type: str = "local", api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_type = api_type.lower()
        self.api_key = api_key or os.getenv(f"{api_type.upper()}_API_KEY") if api_type else None
        self.use_api = (self.api_type in {"openai"} and (self.api_key or os.getenv("OPENAI_API_KEY")))
        self.model = model
        self._client = OpenAI(api_key=(self.api_key or os.getenv("OPENAI_API_KEY"))) if (self.use_api and _openai_available) else None
        self._cache: Dict[Tuple, Dict] = {}

    # ---------- Public ----------
    def enhance_all_steps(self, steps: List[Dict], context: Dict) -> List[Dict]:
        out = []
        for step in steps:
            out.append(self.enhance_explanation(step, context))
        return out

    def enhance_explanation(self, step: Dict, context: Dict) -> Dict:
        if not step:
            return step

       ###"local path
        enriched = self._enhance_locally(step, context)

       ### local not enough? call openAI API
       
        needs_help = context.get("learning_mode", True) and context.get("level", "auto") != "none"
        if self.use_api and needs_help:
            try:
                enriched = self._enhance_with_openai(enriched, context)
            except Exception as e:
                # never fail UX because of API
                enriched.setdefault("meta", {})["llm_error"] = str(e)

        return enriched

    # ---------- Local rules ----------
    def _enhance_locally(self, step: Dict, context: Dict) -> Dict:
        title = (step.get("title") or "").lower()
        expr = step.get("expression", "")
        rule = step.get("rule", "")

        local = ExplainOutput(
            explanation=self._template_explanation(title, expr, rule, context),
            hint=self._generate_hint(title, expr, rule, context),
            common_mistake=self._generate_common_mistake(title, expr, rule),
            follow_up=self._generate_follow_up(title, context)
        )

        step["explanation_pack"] = local.to_dict()
        # for backward compatibility with your UI
        step["explanation"] = local.explanation
        return step

    def _template_explanation(self, title: str, expr: str, rule: str, context: Dict) -> str:
        op = (context.get("operation") or "calculate").lower()

        if "given expression" in title or "given equation" in title or "given function" in title:
            if op == "calculate":
                return (f"We start with the expression {expr}. Our goal is to evaluate this step-by-step by "
                       f"following the order of operations (PEMDAS/BODMAS): Parentheses/Brackets first, "
                       f"then Exponents/Orders, followed by Multiplication and Division (left to right), "
                       f"and finally Addition and Subtraction (left to right).")
            if op == "solve":
                return (f"We begin with the equation {expr}. The goal of solving an equation is to find "
                       f"the value(s) of the unknown variable that make the equation true. We'll do this "
                       f"by performing valid algebraic operations on both sides to isolate the variable, "
                       f"always maintaining the equality.")
            if op == "simplify":
                return (f"We start with {expr}. Simplification means reducing the expression to its most "
                       f"compact form by combining like terms (terms with the same variables and powers) "
                       f"and reducing fractions where possible. The simplified form is easier to work with "
                       f"and reveals the structure more clearly.")
            if op == "expand":
                return (f"We begin with {expr}. Expanding means removing parentheses by applying the "
                       f"distributive property (a(b+c) = ab + ac). This transforms a factored form into "
                       f"a sum of terms, which can be useful for further operations.")
            if op == "factor":
                return (f"Starting with {expr}, we'll factor it into a product of simpler expressions. "
                       f"Factoring is the reverse of expanding and helps us find zeros, simplify fractions, "
                       f"and solve equations more easily.")
            if op == "differentiate":
                return (f"We have the function {expr}. Differentiation finds the rate of change - how the "
                       f"output changes as the input changes. The derivative tells us the slope of the tangent "
                       f"line at any point on the function's graph.")
            if op == "integrate":
                return (f"We are working with the expression {expr}. Integration is the reverse of differentiation — "
                        f"it finds the accumulated area under the curve of a function. "
                        f"By integrating, we determine a new function whose derivative gives us the original expression.")
            if op == "substitute":
                return (f"We start with the expression {expr}. Substitution means replacing the variable with a "
                        f"specific value. This allows us to compute the numerical result of the expression "
                        f"when the variable is set to that value.")
            if op == "solve 2 equations":
                return (f"We are working with the system {expr}. Solving two equations with two unknowns means finding "
                        f"the values of the variables that satisfy *both* equations at the same time. "
                        f"This is done by eliminating one variable or substituting one equation into the other. "
                        f"The solution gives the point where the two equations intersect.")
            if op == "solve quadratic":
                return (f"We are solving the quadratic equation {expr}. A quadratic equation can have up to two "
                        f"solutions because it is based on a squared term. These solutions come from the quadratic "
                        f"formula, factoring, or completing the square. Both solutions are valid as long as they "
                        f"satisfy the original equation.")
            return f"Starting from {expr}, we'll work through this step-by-step."

        if "identify" in title:
            if "+" in expr and "-" not in expr.replace("- ", ""):
                n = expr.count("+") + 1
                return (f"This expression involves addition with {n} terms. Addition is commutative "
                       f"(a+b = b+a) and associative ((a+b)+c = a+(b+c)), meaning we can add in any order. "
                       f"We'll compute the sum by adding the terms together.")
            if "*" in expr or "×" in expr:
                return ("This step involves multiplication. Multiplication represents repeated addition "
                       "and is also commutative (a×b = b×a) and associative. We'll multiply the factors "
                       "together to get the product.")
            if "/" in expr or "÷" in expr:
                return ("This is a division operation. Division asks 'how many times does the divisor fit "
                       "into the dividend?' Remember that division by zero is undefined, and dividing by "
                       "fractions means multiplying by their reciprocal.")
            if "-" in expr:
                return ("This involves subtraction, which computes the difference between two numbers. "
                       "Unlike addition, subtraction is not commutative (a-b ≠ b-a), so order matters!")
            return "We identify the mathematical operation to determine how to proceed with the calculation."

        if "calculate result" in title:
            return ("After carefully performing the operation and following the rules of arithmetic, "
                   "we arrive at the final numeric result. Always double-check your arithmetic to avoid "
                   "calculation errors!")

        if "simplify" in title:
            if "combine" in rule.lower() or "like terms" in rule.lower():
                return ("We combine like terms - these are terms that have exactly the same variable parts. "
                       "For example, 2x and 3x are like terms (both have 'x'), so 2x + 3x = 5x. "
                       "Constants (numbers without variables) are also like terms with each other. "
                       "We can only combine coefficients of like terms, not unlike terms.")
            return ("We simplify by combining like terms, canceling common factors in fractions, "
                   "and reducing the expression to its simplest form. This makes the expression "
                   "cleaner and easier to understand while keeping its mathematical value unchanged.")

        if "foil" in title.lower() or "foil" in rule.lower():
            if "identify" in title or "binomial" in title:
                return ("This is a binomial multiplication - we have two expressions with two terms each. "
                       "We'll use the FOIL method: multiply First terms, then Outer terms, then Inner terms, "
                       "and finally Last terms. FOIL is a systematic way to ensure we don't miss any products.")
            if "apply" in title:
                return ("Using FOIL, we multiply:\n"
                       "• First: the first term from each binomial\n"
                       "• Outer: the outer terms (first from first binomial, last from second)\n"
                       "• Inner: the inner terms (last from first binomial, first from second)\n"
                       "• Last: the last term from each binomial\n"
                       "This gives us four separate products that we'll combine next.")

        if "combine all terms" in title:
            return ("Now we write out all four products from FOIL as a sum. These are the pieces "
                   "we'll put together to form our expanded expression.")

        if "expand" in title:
            return ("We apply the distributive property: a(b + c) = ab + ac. This means we multiply "
                   "each term inside the parentheses by the term outside. After distributing, we "
                   "often need to combine like terms to complete the expansion.")

        if "factor" in title:
            return ("We factor by finding common factors among terms or recognizing special patterns "
                   "like difference of squares (a² - b² = (a+b)(a-b)) or perfect square trinomials. "
                   "Factoring is the reverse of expanding and reveals the multiplicative structure.")

        if "divide" in title and "both sides" in title:
            return ("We divide both sides by the same non-zero number to maintain equality. "
                   "This is valid because dividing equal quantities by the same amount gives equal results. "
                   "This step helps us isolate the variable.")

        if "subtract" in title and "both sides" in title:
            return ("We subtract the same value from both sides of the equation. This is valid by the "
                   "subtraction property of equality: if a = b, then a - c = b - c. This helps us "
                   "move terms to isolate the variable.")

        if "solution" in title or "final" in title:
            return ("This is our final answer. We've isolated the variable and found its value. "
                   "It's good practice to verify by substituting this value back into the original "
                   "equation to check that it works!")

        return "We apply the relevant mathematical rules and properties to progress toward our solution."

    def _generate_hint(self, title: str, expr: str, rule: str, context: Dict) -> Optional[str]:
        """Generate helpful hints for students"""
        op = (context.get("operation") or "").lower()

        if "given" in title:
            if op == "solve":
                return "💡 Tip: Your goal is to get the variable alone on one side of the equals sign. Whatever you do to one side, do to the other!"
            if op == "simplify":
                return "💡 Tip: Look for terms that have the same variable parts - these can be combined by adding/subtracting their coefficients."
            if op == "expand":
                return "💡 Tip: Use FOIL (First, Outer, Inner, Last) for binomial multiplication, or distribute systematically term by term."
            if op == "factor":
                return "💡 Tip: Look for common factors first, then check for special patterns like x² - y² or perfect squares."
            if op == "substitute":
                return "💡 Tip: Replace the variable with the given value carefully, then simplify step by step to avoid mistakes."
            if op == "differentiate":
                return "💡 Tip: Apply the power rule, product rule, or chain rule as needed. Focus on how each term changes with respect to x."
            if op == "integrate":
                return "💡 Tip: Look for functions you recognize as derivatives of something simpler. Reverse the differentiation rules to find the antiderivative."
            if op == "solve quadratic":
                return "💡 Tip: Set the equation equal to zero. Check whether factoring works; if not, use the quadratic formula."
            if op == "solve 2 equations":
                return "💡 Tip: Try eliminating one variable or substitute one equation into the other. Make both equations share only one unknown at a time."

        if "simplify" in title or "combine" in rule.lower():
            return "💡 Tip: Only combine like terms! Terms must have identical variable parts (including powers) to be combined."

        if "identify" in title:
            return "💡 Tip: Understanding what operation we're doing helps us choose the right strategy and apply the correct properties."

        if "divide" in title and "both sides" in title:
            return "💡 Tip: Remember to divide EVERY term on both sides, and never divide by zero!"

        if "subtract" in title and "both sides" in title:
            return "💡 Tip: Watch out for signs! Subtracting a negative is the same as adding a positive."

        if "solution" in title:
            return "💡 Tip: Check your answer by plugging it back into the original equation - both sides should be equal!"

        return None

    def _generate_common_mistake(self, title: str, expr: str, rule: str) -> Optional[str]:
        """Highlight common student mistakes to avoid"""

        if "simplify" in title or "combine" in rule.lower():
            return "⚠️ Common Mistake: Don't combine unlike terms! For example, 2x + 3y cannot be simplified to 5xy. The variables must match exactly."

        if "expand" in title:
            return "⚠️ Common Mistake: When distributing, don't forget to multiply the sign! For example: -2(x - 3) = -2x + 6, not -2x - 6."

        if "divide" in title and "both sides" in title:
            return "⚠️ Common Mistake: Make sure to divide ALL terms on both sides, not just one term. Also, never divide by a variable that could be zero!"

        if "subtract" in title and "both sides" in title:
            return "⚠️ Common Mistake: Be careful with signs! When moving terms across the equals sign, the sign changes."

        if "factor" in title:
            return "⚠️ Common Mistake: After factoring, always check by expanding back out - you should get the original expression."

        if "solve" in title or "solution" in title:
            return "⚠️ Common Mistake: Don't forget to check your solution! Substitute it back into the original equation to verify."

        if "calculate" in title and ("+" in expr or "-" in expr or "*" in expr or "/" in expr):
            return "⚠️ Common Mistake: Follow the order of operations (PEMDAS/BODMAS)! Don't just work left to right."
        
        if "substitute" in title:
            return "⚠️ Common Mistake: Make sure to substitute the value into every instance of the variable. Forgetting some occurrences leads to incorrect results."

        if "differentiate" in title:
            return "⚠️ Common Mistake: Remember to apply all derivative rules properly (product, quotient, chain). Missing a rule often causes wrong answers."

        if "integrate" in title:
            return "⚠️ Common Mistake: Don’t forget the constant of integration when finding indefinite integrals. Also, be careful with substitution and variable changes."
        return None

    def _generate_follow_up(self, title: str, context: Dict) -> Optional[str]:
        """Generate follow-up questions to deepen understanding"""
        op = (context.get("operation") or "").lower()

        if "solution" in title or "final" in title:
            if op == "solve":
                return "🤔 Think About: What happens if you add 5 to both sides of the original equation? Would you get the same solution?"
            if op == "simplify":
                return "🤔 Think About: Could you simplify this expression a different way and still get the same answer?"
            if op == "factor":
                return "🤔 Think About: What are the zeros of this factored expression? (Hint: when does each factor equal zero?)"
            if op == "expand":
                return "🤔 Think About: Can you factor the expanded form back to the original? This confirms you did it correctly!"

        if "given" in title and op == "solve":
            return "🤔 Think About: Before solving, can you estimate roughly what value the variable might be?"

        if "simplify" in title:
            return "🤔 Think About: Why can we combine like terms but not unlike terms? What makes terms 'like'?"

        return None

    # ---------- OpenAI ----------
    def _enhance_with_openai(self, step: Dict, context: Dict) -> Dict:
        if not self._client:
            return step

        # cache key
        key = (
            self.model,
            step.get("title"),
            step.get("expression"),
            step.get("rule"),
            context.get("operation"),
            context.get("level"),
        )
        if key in self._cache:
            step["explanation_pack"] = self._cache[key]
            step["explanation"] = step["explanation_pack"]["explanation"]
            return step

        # enforce short, structured, safe outputs
        response = self._client.responses.create(
            model=self.model,                   # pick a small fast model for explanations
            temperature=0,
            seed=42,                            # deterministic pedagogy for same input
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise math tutor. "
                        "Explain each step in 1–2 sentences, no hidden reasoning. "
                        "Prefer plain language, avoid heavy notation unless needed."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps({
                        "step": {
                            "title": step.get("title"),
                            "expression": step.get("expression"),
                            "rule": step.get("rule")
                        },
                        "context": {
                            "operation": context.get("operation"),
                            "level": context.get("level", "GCSE"),   # GCSE/A-level/Uni
                            "style": context.get("style", "student-friendly")
                        }
                    })
                }
            ],
            # ask for structured JSON back
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "ExplainOutput",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "explanation": {"type": "string"},
                            "hint": {"type": "string"},
                            "common_mistake": {"type": "string"},
                            "follow_up": {"type": "string"}
                        },
                        "required": ["explanation"]
                    }
                }
            },
            max_output_tokens=160,
        )

        # parse
        content = response.output[0].content[0].text  # structured JSON string
        data = json.loads(content)

        # merge
        step["explanation_pack"] = data
        step["explanation"] = data["explanation"]

        # cache
        self._cache[key] = data
        return step
