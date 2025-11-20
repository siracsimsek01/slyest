import pytest
import sympy as sym

class MockInputField:
    def __init__(self, text=""):
        self._text = text
    def text(self):
        return self._text

class MockOutputDisplay:
    def __init__(self):
        self.text = ""
    def setPlainText(self, t):
        self.text = t

class MockHistoryList:
    def __init__(self):
        self.items = []
    def addItem(self, item):
        self.items.append(item)

class MockStatusBar:
    def __init__(self):
        self.msg = ""
    def showMessage(self, msg):
        self.msg = msg


class MockEngine:
    def parse_expression(self, expr_str):
        return sym.sympify(expr_str)

class MockHistoryEntry:
    def __init__(self, action, input_expr, output_expr):
        self.action = action
        self.input_expr = input_expr
        self.output_expr = output_expr
    def __str__(self):
        return f"{self.action}: {self.input_expr} -> {self.output_expr}"

class MockSession:
    def __init__(self):
        self.history = []

def format_expression(expr):
    return str(expr)

class OperationTester:
    def __init__(self, input_text):
        self.input_field = MockInputField(input_text)
        self.output_display = MockOutputDisplay()
        self.history_list = MockHistoryList()
        self._status_bar = MockStatusBar()
        self.engine = MockEngine()
        self.session = MockSession()

    def statusBar(self):
        return self._status_bar

    def simplify_expression(self):
        import sympy as sym
        try:
            expr_str = self.input_field.text().strip()
            if not expr_str:
                return

            expr = self.engine.parse_expression(expr_str)
            result = sym.simplify(expr)

            formatted = format_expression(result)
            self.output_display.setPlainText(formatted)

            entry = MockHistoryEntry("Simplify", expr_str, formatted)
            self.session.history.append(entry)
            self.history_list.addItem(str(entry))

            self.statusBar().showMessage("Simplified successfully")
            return result

        except Exception as e:
            print("Error:", str(e))

    def expand_expression(self):
        import sympy as sym
        try:
            expr_str = self.input_field.text().strip()
            if not expr_str:
                return

            expr = self.engine.parse_expression(expr_str)
            result = sym.expand(expr)

            formatted = format_expression(result)
            self.output_display.setPlainText(formatted)

            entry = MockHistoryEntry("Expand", expr_str, formatted)
            self.session.history.append(entry)
            self.history_list.addItem(str(entry))

            self.statusBar().showMessage("Expanded successfully")
            return result

        except Exception as e:
            print("Error:", str(e))

    def factor_expression(self):
        import sympy as sym
        try:
            expr_str = self.input_field.text().strip()
            if not expr_str:
                return

            expr = self.engine.parse_expression(expr_str)
            result = sym.factor(expr)

            formatted = format_expression(result)
            self.output_display.setPlainText(formatted)

            entry = MockHistoryEntry("Factor", expr_str, formatted)
            self.session.history.append(entry)
            self.history_list.addItem(str(entry))

            self.statusBar().showMessage("Factored successfully")
            return result

        except Exception as e:
            print("Error:", str(e))


def test_simplify_expression():
    tester = OperationTester("sin(x)**2 + cos(x)**2")
    result = tester.simplify_expression()

    assert str(result) == "1"
    assert tester.output_display.text == "1"
    assert tester.history_list.items[0] == "Simplify: sin(x)**2 + cos(x)**2 -> 1"
    assert tester.statusBar().msg == "Simplified successfully"


def test_expand_expression():
    tester = OperationTester("(x + 1)**3")
    result = tester.expand_expression()

    assert str(result) == "x**3 + 3*x**2 + 3*x + 1"
    assert tester.output_display.text == "x**3 + 3*x**2 + 3*x + 1"
    assert tester.history_list.items[0] == \
        "Expand: (x + 1)**3 -> x**3 + 3*x**2 + 3*x + 1"
    assert tester.statusBar().msg == "Expanded successfully"


def test_factor_expression():
    tester = OperationTester("x**2 - 5*x + 6")
    result = tester.factor_expression()

    expected = (sym.Symbol("x") - 2) * (sym.Symbol("x") - 3)
    assert sym.simplify(result - expected) == 0

    assert tester.output_display.text in ["(x - 2)*(x - 3)", "(x - 3)*(x - 2)"]
    assert "Factor: x**2 - 5*x + 6" in tester.history_list.items[0]
    assert tester.statusBar().msg == "Factored successfully"