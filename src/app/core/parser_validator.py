def validate_characters(expr):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/^.()_ ²³√"
    for ch in expr:
        if ch not in allowed:
            return f"Invalid character: '{ch}'"
    return None


def validate_parentheses(expr):
    count = 0
    for ch in expr:
        if ch == "(":
            count += 1
        elif ch == ")":
            count -= 1
            if count < 0:
                return "Closing parenthesis without opening one"
    if count != 0:
        return "Unmatched parentheses"
    return None


def validate_operators(expr):
    bad_sequences = ["++", "--", "**", "//", "..", "+*", "+/", "*-", "*/"]
    for seq in bad_sequences:
        if seq in expr:
            return f"Invalid operator sequence: '{seq}'"
    stripped = expr.strip()
    if stripped[0] in "*/.^":
        return "Expression cannot start with operator"
    if stripped[-1] in "+-*/^.":
        return "Expression cannot end with operator"
    return None


def handle_powers(expr):
    expr = expr.replace("x²", "x^2")
    expr = expr.replace("x³", "x^3")
    expr = expr.replace("²", "^2")
    expr = expr.replace("³", "^3")
    expr = expr.replace("^", "**")
    return expr


def handle_roots(expr):
    expr = expr.replace("√(", "sqrt(")
    expr = expr.replace("**(1/2)", ")__SQRT__")
    expr = expr.replace("(1/2)", "__SQRT__")
    expr = expr.replace("(1/3)", "__CBRT__")
    expr = expr.replace("**(1/", "__ROOT__(")
    return expr


def handle_implicit_multiplication(expr):
    result = ""
    for i in range(len(expr) - 1):
        a, b = expr[i], expr[i+1]
        if a.isdigit() and b.isalpha():
            result += a + "*"
            continue
        if a.isalpha() and b.isdigit():
            result += a + "*"
            continue
        if a == ")" and (b.isalpha() or b.isdigit()):
            result += a + "*"
            continue
        if a.isalpha() and b == "(":
            result += a + "*"
            continue
        result += a
    result += expr[-1]
    return result


def handle_functions(expr):
    repl = {
        "sin(": "SIN(",
        "cos(": "COS(",
        "tan(": "TAN(",
        "sinh(": "SINH(",
        "cosh(": "COSH(",
        "tanh(": "TANH(",
        "asin(": "ASIN(",
        "acos(": "ACOS(",
        "atan(": "ATAN(",
        "ln(": "LN(",
        "log(": "LOG(",
        "exp(": "EXP("
    }
    for k, v in repl.items():
        expr = expr.replace(k, v)
    return expr


def handle_constants(expr):
    expr = expr.replace("pi", "PI")
    expr = expr.replace("e", "E")
    return expr


def parse_expression(expr):
    expr = expr.replace(" ", "")
    err = validate_characters(expr)
    if err: 
        return {"error": err}
    err = validate_parentheses(expr)
    if err: 
        return {"error": err}
    err = validate_operators(expr)
    if err: 
        return {"error": err}
    expr = handle_powers(expr)
    expr = handle_roots(expr)
    expr = handle_implicit_multiplication(expr)
    expr = handle_functions(expr)
    expr = handle_constants(expr)
    expr = expr.replace("__SQRT__", "SQRT(")
    expr = expr.replace("__CBRT__", "CBRT(")
    expr = expr.replace("__ROOT__(", "ROOT(")
    return {"parsed": expr}
