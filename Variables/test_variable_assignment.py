from sympy import symbols
from variable_assignment import VariableManager

def test_assign_and_get_expression():
    x = symbols('x')
    vm = VariableManager()
    vm.assign("e1", "x + 1")
    assert str(vm.get("e1")) == "x + 1"

def test_reuse_expression_in_calculation():
    x = symbols('x')
    vm = VariableManager()
    vm.assign("e1", "x + 1")
    expr = vm.get("e1")
    result = expr * x
    assert str(result) == "x*(x + 1)"

def test_get_nonexistent_variable_returns_none():
    vm = VariableManager()
    assert vm.get("e2") is None

