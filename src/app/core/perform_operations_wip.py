
'''WORK IN PROGRESS – NOT YET CONNECTED TO GUI

These functions will eventually be integrated into MainWindow.
Currently kept separate for development and testing.'''
def simplify_expression(self):
    try:
        expr_str = self.input_field.text().strip()
        if not expr_str:
            return

        expr = self.engine.parse_expression(expr_str)

        import sympy as sp
        result = sp.simplify(expr)

        formatted = format_expression(result)
        self.output_display.setPlainText(formatted)

        from .session import HistoryEntry
        entry = HistoryEntry("Simplify", expr_str, formatted)
        self.session.history.append(entry)
        self.history_list.addItem(str(entry))

        self.statusBar().showMessage("Simplified successfully")
        return result

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to simplify: {str(e)}")


def expand_expression(self):
    try:
        expr_str = self.input_field.text().strip()
        if not expr_str:
            return

        expr = self.engine.parse_expression(expr_str)

        import sympy as sp
        result = sp.expand(expr)

        formatted = format_expression(result)
        self.output_display.setPlainText(formatted)

        from .session import HistoryEntry
        entry = HistoryEntry("Expand", expr_str, formatted)
        self.session.history.append(entry)
        self.history_list.addItem(str(entry))

        self.statusBar().showMessage("Expanded successfully")
        return result

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to expand: {str(e)}")


def factor_expression(self):
    try:
        expr_str = self.input_field.text().strip()
        if not expr_str:
            return

        expr = self.engine.parse_expression(expr_str)

        import sympy as sp
        result = sp.factor(expr)

        formatted = format_expression(result)
        self.output_display.setPlainText(formatted)

        from .session import HistoryEntry
        entry = HistoryEntry("Factor", expr_str, formatted)
        self.session.history.append(entry)
        self.history_list.addItem(str(entry))

        self.statusBar().showMessage("Factored successfully")
        return result

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to factor: {str(e)}")