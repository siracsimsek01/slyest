"""
variable management window for calculator.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..core.symbolic_engine import SymbolicEngine
class VariableWindow(QDialog):
    """dialog for managing calculation variables."""
    variables_changed = pyqtSignal() # signal emitted when variables are updated

    def __init__(self, engine: SymbolicEngine, parent=None):
        super().__init__(parent)
        self.engine = engine  # reference to the calculator's engine
        self.setWindowTitle("Variable Manager")
        self.setGeometry(200, 200, 500, 600)

        # Apply dark theme
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #1C1C1E;
                color: white;
            }}
            QLabel {{
                color: white;
                font-size: 12pt;
            }}
            QLineEdit {{
                background-color: #2C2C2E;
                color: white;
                border: 2px solid #3A3A3C;
                border-radius: 8px;
                padding: 8px;
                font-size: 11pt;
            }}
            QLineEdit:focus {{
                border: 2px solid #FF9F0A;
            }}
            QPushButton {{
                background-color: #FF9F0A;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 11pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #E68A00;
            }}
            QPushButton#deleteBtn {{
                background-color: #D32F2F;
            }}
            QPushButton#deleteBtn:hover {{
                background-color: #B71C1C;
            }}
            QListWidget {{
                background-color: #2C2C2E;
                color: white;
                border: 2px solid #3A3A3C;
                border-radius: 8px;
                padding: 5px;
                font-size: 11pt;
            }}
            QListWidget::item {{
                padding: 10px;
                border-radius: 4px;
            }}
            QListWidget::item:hover {{
                background-color: #3A3A3C;
            }}
            QListWidget::item:selected {{
                background-color: #505050;
            }}
        """)

        self.initialise_ui()
        self.refresh_variable_list()

    def initialise_ui(self):
        """set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # title
        title = QLabel("Variable Manager")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # instructions
        instructions = QLabel("Create and manage variables for your calculations")
        instructions.setStyleSheet("color: #A0A0A0; font-size: 10pt;")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)

        # add new variable section
        add_section = QWidget()
        add_layout = QVBoxLayout(add_section)

        # name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFixedWidth(80)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., x1, myVar")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        add_layout.addLayout(name_layout)

        # value input
        value_layout = QHBoxLayout()
        value_label = QLabel("Value:")
        value_label.setFixedWidth(80)
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("e.g., x^2 + 1, sin(x)")
        self.value_input.returnPressed.connect(self.add_variable)
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_input)
        add_layout.addLayout(value_layout)

        # Add button
        add_btn_layout = QHBoxLayout()
        add_btn_layout.addStretch()
        self.add_btn = QPushButton("Add Variable")
        self.add_btn.clicked.connect(self.add_variable)
        add_btn_layout.addWidget(self.add_btn)
        add_btn_layout.addStretch()
        add_layout.addLayout(add_btn_layout)

        layout.addWidget(add_section)

        # divider
        divider = QLabel()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: #3A3A3C;")
        layout.addWidget(divider)

        # Variables list
        list_label = QLabel("Existing Variables:")
        list_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(list_label)

        self.variable_list = QListWidget()
        self.variable_list.itemDoubleClicked.connect(self.edit_variable)
        layout.addWidget(self.variable_list)

        # buttons at bottom
        button_layout = QHBoxLayout()

        self.use_btn = QPushButton("Use in Calculations")
        self.use_btn.clicked.connect(self.use_variable)
        button_layout.addWidget(self.use_btn)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.edit_variable)
        button_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.clicked.connect(self.delete_variable)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(button_layout)

    def add_variable(self):
        name = self.name_input.text().strip()
        value = self.value_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a variable name")
            return
        if not value:
            QMessageBox.warning(self, "Invalid Input", "Please enter a variable value")
            return
        try:
            self.engine.assign_variable(name, value)
            self.name_input.clear()
            self.value_input.clear()
            self.refresh_variable_list()
            self.variables_changed.emit() # Notify when changed
            self.statusBar().showMessage(f"Variable '{name}' added successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add variable:\n{str(e)}")

    def edit_variable(self):
        current_item = self.variable_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a variable to edit")
            return
        item_text = current_item.text()
        var_name = item_text.split(" = ")[0].strip()
        current_value = str(self.engine.get_variable(var_name))
        self.name_input.setText(var_name)
        self.value_input.setText(current_value)
        self.value_input.setFocus()

    def delete_variable(self):
        current_item = self.variable_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a variable to delete")
            return
        item_text = current_item.text()
        var_name = item_text.split(" = ")[0].strip()
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{var_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if var_name in self.engine.variables:
                del self.engine.variables[var_name]
            self.refresh_variable_list()
            self.variables_changed.emit()

    def use_variable(self):
        current_item = self.variable_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a variable to use")
            return
        item_text = current_item.text()
        var_name = item_text.split(" = ")[0].strip()
        self.selected_variable = var_name
        self.accept()

    def refresh_variable_list(self):
        self.variable_list.clear()
        variables = self.engine.list_variables()
        if not variables:
            # Show empty message
            item = QListWidgetItem("No variables yet. Add one above!")
            item.setFlags(Qt.ItemFlag.NoItemFlags)  # Make it non-selectable
            item.setForeground(Qt.GlobalColor.gray)
            self.variable_list.addItem(item)
        else:
            # Add each variable to the list
            for name, value in variables.items():
                item_text = f"{name} = {value}"
                item = QListWidgetItem(item_text)
                self.variable_list.addItem(item)

    def statusBar(self):
        class DummyStatusBar:
            def showMessage(self, msg):
                pass  # Could show in parent window if needed
        return DummyStatusBar()