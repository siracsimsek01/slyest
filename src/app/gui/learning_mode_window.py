from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel)

class LearningModeWindow(QDialog):
    """dialog for learning mode"""
    def __init__(self, operation, input_expression, result, optional_input, parent=None):
        super().__init__(parent)
        self.apply_stylesheet()
        self.setWindowTitle("Learning Mode")
        self.setGeometry(400, 300, 800, 400)
        self.operation = operation
        self.input_expression = input_expression
        self.result = result
        self.optional_input = optional_input
        self.initialise_ui()
        
    def apply_stylesheet(self):
        self.setStyleSheet(f"""
                QDialog {{
                    background-color: #1C1C1E;
                    color: white;
                }}
                                     
                QLabel#learning {{
                    background-color: #A5A5A5;
                    color: #000000;
                    border-radius: 10px;
                    padding: 20px;
                    font-size: 12pt;
                }}
                QLabel#name {{
                    color: white;
                    font-size: 12pt; 
                    font-weight: 'bold';
                }} 
                QLabel#expression {{
                    color: white;
                    font-size: 12pt; 
                    font-family: 'Courier';
                }} """)
        
    def initialise_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # name input
        window_layout = QVBoxLayout()

        input_layout_operation = QHBoxLayout()
        operation = QLabel("Operation: ")
        operation.setObjectName("name")
        operation.setFixedWidth(200)
        operation_input = QLabel(self.operation)
        operation_input.setObjectName("expression")
        input_layout_operation.addWidget(operation)
        input_layout_operation.addWidget(operation_input)
        input_layout_operation.setContentsMargins(0, 0, 0, 0)

        input_layout_expression = QHBoxLayout()
        expression = QLabel("Input Expression: ")
        expression.setObjectName("name")
        expression.setFixedWidth(200)
        expression_input = QLabel(self.input_expression)
        expression_input.setObjectName("expression")
        input_layout_expression.addWidget(expression)
        input_layout_expression.addWidget(expression_input)

        input_layout_optional_expression = QHBoxLayout()
        optional_expression = QLabel("Optional Input Expression: ")
        optional_expression.setObjectName("name")
        optional_expression.setFixedWidth(200)
        optional_expression_input = QLabel(self.optional_input)
        optional_expression_input.setObjectName("expression")
        input_layout_optional_expression.addWidget(optional_expression)
        input_layout_optional_expression.addWidget(optional_expression_input)

        result = QHBoxLayout()
        result_label = QLabel("Answer: ")
        result_label.setObjectName("name")
        result_label.setFixedWidth(200)
        result_label_input = QLabel(self.result)
        result_label_input.setObjectName("expression")
        result.addWidget(result_label)
        result.addWidget(result_label_input)

        learning_hint_layout = QVBoxLayout()
        hinting_label = QLabel("Step-by-step hints: ")
        hinting_label.setObjectName("name")
        learning_hints = QLabel("Placeholder")
        learning_hints.setObjectName("learning")
        learning_hints.setMinimumHeight(200)
        learning_hints.setWordWrap(True)
        learning_hint_layout.addWidget(hinting_label)
        learning_hint_layout.addWidget(learning_hints)

        window_layout.addLayout(input_layout_operation)
        window_layout.addLayout(input_layout_expression)
        window_layout.addLayout(input_layout_optional_expression)
        window_layout.addLayout(result)
        window_layout.addLayout(learning_hint_layout)

        layout.addLayout(window_layout)