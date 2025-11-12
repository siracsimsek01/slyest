import pytest
from sympy import symbols
from variable_assignment import VariableManager

@pytest.fixture
def vm_and_x():
    """Fixture that provides a VariableManager and a symbol x."""
    return VariableManager(), symbols('x')

def test_assign_and_get_expression(vm_and_x):
    vm, x = vm_and_x
    vm.assign("e1", "x + 1")
    assert str(vm.get("e1")) == "x + 1"

def test_reuse_expression_in_calculation(vm_and_x):
    vm, x = vm_and_x
    vm.assign("e1", "x + 1")
    expr = vm.get("e1")
    result = expr * x
    assert str(result) == "x*(x + 1)"

def test_get_nonexistent_variable_returns_none(vm_and_x):
    vm, _ = vm_and_x
    assert vm.get("e2") is None
