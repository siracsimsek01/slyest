from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from src.app.core.session import SessionManager

class HistoryWindow(QDialog):
    """dialog for saving calculation history"""
    def __init__(self, calculation_history, parent=None):
        super().__init__(parent)
        self.calculation_history = calculation_history
        self.session_manager = SessionManager()

        self.setWindowTitle("History Window")
        self.setGeometry(400, 300, 500, 200)

        self.apply_stylesheet()
        self.initialise_ui()
        
    def apply_stylesheet(self):
        self.setStyleSheet(f"""
                QDialog {{
                    background-color: #1C1C1E;
                    color: white;
                }}
                QLabel {{
                    color: white;
                    font-size: 12pt; 
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
            }}""")
        
    def initialise_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Enter file name:")
        name_label.setFixedWidth(120)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., My Calculations")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        button_layout = QHBoxLayout()
        self.export_text_btn = QPushButton("Export Text File")
        self.export_text_btn.clicked.connect(lambda: self.export_file('txt'))
        button_layout.addWidget(self.export_text_btn)

        self.export_pdf_btn = QPushButton("Export PDF File")
        self.export_pdf_btn.clicked.connect(lambda: self.export_file('pdf'))
        button_layout.addWidget(self.export_pdf_btn)

        layout.addLayout(button_layout)

    def export_file(self, file_type):
        name = self.name_input.text().strip()
        if name and len(self.calculation_history) != 0:
            file_name = self.session_manager.export_history(file_type, name, self.calculation_history)
            if file_name:
                self.name_input.clear()
                QMessageBox.information(self, "Info", f"'{file_name}' successfully saved!")
            else:
                QMessageBox.critical(self, "Error", "Error in saving text file.")
        elif not name:
            QMessageBox.critical(self, "Error", "Please type the file name.")
        else:
            QMessageBox.critical(self, "Error", "Calculation history is empty.")