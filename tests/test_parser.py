import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from app.core.parser_validator import (
    validate_characters,
    validate_parentheses,
    validate_operators,
    handle_powers,
    handle_roots,
    handle_implicit_multiplication,
    handle_functions,
    handle_constants,
    parse_expression
)
def test_validate_characters_valid():
    assert validate_characters("x^2 + 3") is None
    assert validate_characters("y+4-5*(x^3)") is None

def test_validate_characters_invalid():
    assert validate_characters("x$2") == "Invalid character: '$'"
    assert validate_characters("y@3") == "Invalid character: '@'"
    assert validate_characters("x² + y³") is None  # '²' and '³' are allowed

def test_validate_parentheses_valid():
    assert validate_parentheses("(x+2)*(x-3)") is None
    assert validate_parentheses("((x+2)*(x-3))") is None

def test_validate_parentheses_invalid():
    assert validate_parentheses("((x+2)") == "Unmatched parentheses"
    assert validate_parentheses("x+2) + (3") == "Closing parenthesis without opening one"

def test_validate_operators_valid():
    assert validate_operators("x+2-3*x") is None
    assert validate_operators("x+2/3") is None

def test_validate_operators_invalid():
    assert validate_operators("x++2") == "Invalid operator sequence: '++'"
    assert validate_operators("*x+3") == "Expression cannot start with operator"
    assert validate_operators("x+3/") == "Expression cannot end with operator"
    assert validate_operators("x**2") == "Invalid operator sequence: '**'"

def test_handle_powers():
    assert handle_powers("x²+3") == "x^2+3"
    assert handle_powers("y³+5") == "y^3+5"
    assert handle_powers("x^2 + y^3") == "x^2 + y^3"
    assert handle_powers("x² - x³") == "x^2 - x^3"

def test_handle_roots():
    assert handle_roots("√(x)") == "sqrt(x)"
    assert handle_roots("x**(1/2)") == "x)__SQRT__"
    assert handle_roots("(x+1)**(1/2)") == "(x+1)__SQRT__"
    assert handle_roots("x**(1/3)") == "x)__CBRT__"

def test_handle_implicit_multiplication():
    assert handle_implicit_multiplication("2x") == "2*x"
    assert handle_implicit_multiplication("x(3+2)") == "x*(3+2)"
    assert handle_implicit_multiplication("(x+1)2") == "(x+1)*2"
    assert handle_implicit_multiplication("x+y") == "x+y"

def test_handle_functions():
    assert handle_functions("sin(x)+log(3)") == "SIN(x)+LOG(3)"
    assert handle_functions("cos(x)*sin(x)") == "COS(x)*SIN(x)"
    assert handle_functions("tan(x)") == "TAN(x)"
    assert handle_functions("exp(x)+ln(x)") == "EXP(x)+LN(x)"

def test_handle_constants():
    assert handle_constants("pi + e") == "PI + E"
    assert handle_constants("sin(x)*pi") == "SIN(x)*PI"
    assert handle_constants("pi^2 + e^3") == "PI^2 + E^3"

def test_parse_expression_valid():
    result = parse_expression("2x + √(x²)")
    assert result["parsed"] == "2*x + sqrt(x**2)"
    result = parse_expression("sin(x) + log(3)")
    assert result["parsed"] == "SIN(x) + LOG(3)"
    result = parse_expression("x² + 3x + pi")
    assert result["parsed"] == "x^2 + 3*x + PI"

def test_parse_expression_invalid():
    result = parse_expression("2x + @")
    assert "error" in result
    assert result["error"] == "Invalid character: '@'"
    
    result = parse_expression("x++2")
    assert "error" in result
    assert result["error"] == "Invalid operator sequence: '++'"

    result = parse_expression("((x+2)")
    assert "error" in result
    assert result["error"] == "Unmatched parentheses"

    result = parse_expression("x**2")
    assert "error" in result
    assert result["error"] == "Invalid operator sequence: '**'"

