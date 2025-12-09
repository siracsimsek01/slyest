from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel)

class LearningModeWindow(QDialog):
    def __init__(self, operation, input_expression, result, optional_input, parent=None):
        super().__init__(parent)
        self.apply_stylesheet()
        self.setWindowTitle("Learning Mode")
        self.setGeometry(400, 300, 800, 400)
        self.operation = operation
        self.input_expression = input_expression
        self.result = result
        self.optional_input = optional_input
        self.label_width = 200
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
        window_layout = QVBoxLayout()

        window_layout.addLayout(self.create_box_layout("Operation", self.operation, self.label_width))
        window_layout.addLayout(self.create_box_layout("Input Expression: ", self.input_expression, self.label_width))
        window_layout.addLayout(self.create_box_layout("Optional Input Expression: ", self.optional_input, self.label_width))
        window_layout.addLayout(self.create_box_layout("Answer: ", self.result, self.label_width))

        learning_hint_layout = QVBoxLayout()
        learning_hint_layout.addWidget(self.create_label("Step-by-step hints: ", "name"))
        learning_hints = QLabel("Placeholder")
        learning_hints.setObjectName("learning")
        learning_hints.setMinimumHeight(200)
        learning_hints.setWordWrap(True)
        learning_hint_layout.addWidget(learning_hints)
        window_layout.addLayout(learning_hint_layout)

        layout.addLayout(window_layout)

    def create_label(self, text, object_name, width=None):
        label = QLabel(text)
        label.setObjectName(object_name)
        if width:
            label.setFixedWidth(width)
        return label

    def create_box_layout(self, label_name, label_value, width):
        layout = QHBoxLayout()
        layout.addWidget(self.create_label(label_name, "name", width))
        layout.addWidget(self.create_label(label_value, "expression"))
        return layout