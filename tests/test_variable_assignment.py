import pytest
from sympy import symbols
from src.app.core.variable_assignment import VariableManager  

@pytest.fixture
def variable_manager_and_expression():
    return VariableManager(), symbols('x')

def test_assign_and_get_expression(variable_manager_and_expression):
    variable_manager, expression = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    assert str(variable_manager.get_variable("e1")) == "x + 1"

def test_reuse_expression_in_calculation(variable_manager_and_expression):
    variable_manager, expression = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    expr = variable_manager.get_variable("e1")
    result = expr * expression
    assert str(result) == "x*(x + 1)"

def test_get_nonexistent_variable_returns_none(variable_manager_and_expression):
    variable_manager, _ = variable_manager_and_expression
    assert variable_manager.get_variable("e2") is None

def test_remove_variable(variable_manager_and_expression):
    variable_manager, _ = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    variable_manager.remove_variable("e1")
    assert variable_manager.get_variable("e1") is None

def test_remove_variable_that_doesnt_exist(variable_manager_and_expression):
    variable_manager, _ = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    variable_manager.remove_variable("e2")
    assert str(variable_manager.get_variable("e1")) == "x + 1"

def test_replace_variable(variable_manager_and_expression):
    variable_manager, _ = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    variable_manager.replace_variable("e1", "x**2")
    assert str(variable_manager.get_variable("e1")) == "x**2"

def test_replace_variable_that_doesnt_exist(variable_manager_and_expression):
    variable_manager, _ = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    result = variable_manager.replace_variable("e2", "x**2")
    assert result is False

def test_variable_used_in_addition(variable_manager_and_expression):
    variable_manager, x = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    expr = variable_manager.get_variable("e1")
    result = expr + x
    assert result == 2*x + 1

def test_variable_used_in_subtraction(variable_manager_and_expression):
    variable_manager, x = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    expr = variable_manager.get_variable("e1")
    result = expr - x
    assert str(result) == "1" 

def test_variable_used_in_division(variable_manager_and_expression):
    variable_manager, x = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    expr = variable_manager.get_variable("e1")
    result = expr / x
    assert str(result) == "(x + 1)/x"

def test_chained_calculations(variable_manager_and_expression):
    variable_manager, x = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    expr = variable_manager.get_variable("e1")
    result = (expr * x) + (expr / x)
    assert result == x*(x + 1) + (x + 1)/x

def test_replace_and_reuse(variable_manager_and_expression):
    variable_manager, x = variable_manager_and_expression
    variable_manager.assign_variable("e1", "x + 1")
    variable_manager.replace_variable("e1", "x**2")
    expr = variable_manager.get_variable("e1")
    result = expr + x
    assert result == x**2 + x

def test_multiple_variables_interaction(variable_manager_and_expression):
    variable_manager, x = variable_manager_and_expression
    variable_manager.assign_variable("a", "x + 1")
    variable_manager.assign_variable("b", "x - 1")
    expr_a = variable_manager.get_variable("a")
    expr_b = variable_manager.get_variable("b")
    result = expr_a * expr_b
    assert result == (x + 1)*(x - 1)


