from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from src.app.core.session import SessionManager

class HistoryWindow(QDialog):
    """dialog for managing saving history."""
    # variables_changed = pyqtSignal() # signal emitted when variables are updated

    def __init__(self, calculation_history, parent=None):
        self.calculation_history = calculation_history
        super().__init__(parent)
        self.setWindowTitle("History Window")
        self.setGeometry(200, 200, 500, 300)
        self.session_manager = SessionManager()

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
                    
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Enter file name:")
        name_label.setFixedWidth(80)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., My Calculations")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        button_layout = QHBoxLayout()

        self.export_text_btn = QPushButton("Export Text File")
        self.export_text_btn.clicked.connect(self.export_text_file)
        button_layout.addWidget(self.export_text_btn)

        self.export_pdf_btn = QPushButton("Export PDF File")
        self.export_pdf_btn.clicked.connect(self.export_pdf_file)
        button_layout.addWidget(self.export_pdf_btn)

        layout.addLayout(button_layout)

    def export_text_file(self):
        name = self.name_input.text().strip()
        self.session_manager.export_history("txt", name, self.calculation_history)


    def export_pdf_file(self):
        name = self.name_input.text().strip()
        self.session_manager.export_history("pdf", name, self.calculation_history)
