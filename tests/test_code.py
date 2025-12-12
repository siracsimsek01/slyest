import sys
import os
import pytest
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class MockOperations:
    def __init__(self):
        self.mock_result = "mock_result"
    
    def calculate_result(self, expression: str):
        return (expression, self.mock_result) if expression else None

    def sin(self, expression: str):
        return self.mock_result
    
    def cos(self, expression: str):
        return self.mock_result
    
    def tan(self, expression: str):
        return self.mock_result
    
    def sinh(self, expression: str):
        return self.mock_result
    
    def cosh(self, expression: str):
        return self.mock_result
    
    def tanh(self, expression: str):
        return self.mock_result
    
    def square_root(self, expression: str):
        return self.mock_result
    
    def cube_root(self, expression: str):
        return self.mock_result
    
    def square(self, expression: str):
        return self.mock_result
    
    def power(self, expression: str):
        return self.mock_result
    
    def reciprocal(self, expression: str):
        return self.mock_result
    
    def exp(self, expression: str):
        return self.mock_result
    
    def pi(self, expression: str):
        return self.mock_result
    
    def power_of_10(self, expression: str):
        return self.mock_result
    
    def natural_log(self, expression: str):
        return self.mock_result
    
    def log_base_10(self, expression: str):
        return self.mock_result
    
    def factorial(self, expression: str):
        return self.mock_result
    
    def operation(self, op: str, expression: str):
        return self.mock_result
    
    def insert_constant_e(self, expression: str):
        return self.mock_result
    
    def insert_constant_pi(self, expression: str):
        return self.mock_result


@pytest.fixture
def app():
    app = QApplication([])
    return app


@pytest.fixture
def main_window(app):
    # Assuming `MainWindow` is your actual main window class
    main_window = QMainWindow()
    main_window.expression_input = QLineEdit(main_window)  # Add a QLineEdit to simulate the input field
    main_window.operations = MockOperations()  # Mocking operations
    return main_window


def test_handle_equals_click(main_window):
    main_window.expression_input.setText("5 + 5")
    main_window.handle_equals_click()

    # Check if the expression_input text was updated correctly
    assert main_window.expression_input.text() == "5 + 5"  # Adjust based on expected format
    # Since the mock always returns "mock_result"
    assert main_window.operations.calculate_result.called_with("5 + 5")


def test_handle_trigonometric_function_click(main_window):
    # Test sin function
    main_window.expression_input.setText("30")
    main_window.handle_function_click("sin")
    assert main_window.expression_input.text() == "mock_result"
    main_window.operations.sin.assert_called_with("30")


def test_handle_constant_click(main_window):
    # Test for the constant e
    main_window.expression_input.setText("some expression")
    main_window.handle_constant_click("e")
    assert main_window.expression_input.text() == "mock_result"
    main_window.operations.insert_constant_e.assert_called_with("some expression")

    # Test for the constant π
    main_window.handle_constant_click("π")
    assert main_window.expression_input.text() == "mock_result"
    main_window.operations.insert_constant_pi.assert_called_with("some expression")


def test_handle_function_click_for_sqrt(main_window):
    main_window.expression_input.setText("16")
    main_window.handle_function_click("sqrt")
    assert main_window.expression_input.text() == "mock_result"
    main_window.operations.square_root.assert_called_with("16")


@pytest.mark.parametrize("function_name, expected_call", [
    ("sin", "sin"),
    ("cos", "cos"),
    ("tan", "tan"),
    ("sinh", "sinh"),
    ("cosh", "cosh"),
    ("tanh", "tanh"),
    ("sqrt", "square_root"),
    ("cbrt", "cube_root"),
    ("x²", "square"),
    ("x³", "cube"),
    ("xʸ", "power"),
    ("1/x", "reciprocal"),
    ("eˣ", "exp"),
    ("pi", "pi"),
    ("10ˣ", "power_of_10"),
    ("ln", "natural_log"),
    ("log₁₀", "log_base_10"),
    ("x!", "factorial"),
])
def test_handle_function_click(main_window, function_name, expected_call):
    main_window.expression_input.setText("10")
    main_window.handle_function_click(function_name)
    getattr(main_window.operations, expected_call).assert_called_with("10")


if __name__ == "__main__":
    pytest.main()
