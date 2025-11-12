import pytest
from sympy import symbols
from src.app.core.variable_assignment import VariableManager  

@pytest.fixture
def variable_manager_and_expression():
    return VariableManager(), symbols('x')

def test_assign_and_get_expression(variable_manager_and_expression):
    variable_manager, expression = variable_manager_and_expression
    variable_manager.assign("e1", "x + 1")
    assert str(variable_manager.get("e1")) == "x + 1"

def test_reuse_expression_in_calculation(variable_manager_and_expression):
    variable_manager, expression = variable_manager_and_expression
    variable_manager.assign("e1", "x + 1")
    expr = variable_manager.get("e1")
    result = expr * expression
    assert str(result) == "x*(x + 1)"

def test_get_nonexistent_variable_returns_none(variable_manager_and_expression):
    variable_manager, _ = variable_manager_and_expression
    assert variable_manager.get("e2") is None
