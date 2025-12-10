### History Panel widget for the calculator
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont 
from ..gui.history_window import HistoryWindow

class HistoryPanel(QWidget):
    ### widget that displays calculation history
    history_item_selected = pyqtSignal(dict)
    
    def __init__(self, session_manager=None, parent=None):
        super().__init__(parent)
        self.setObjectName("historyPanel")
        self.session_manager = session_manager
        self.calculation_history = []
        self.initialise_ui()
        
    def initialise_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        header_layout = self.create_header()
        layout.addLayout(header_layout)

        self.history_list = self.create_history_list()
        layout.addWidget(self.history_list)

        instructions = self.create_instructions_label()
        layout.addWidget(instructions)

    def create_header(self):  
        header_layout = QHBoxLayout() 

        title = QLabel("History")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("historyToggle")
        self.clear_btn.clicked.connect(self.clear_history)
        header_layout.addWidget(self.clear_btn)
        # layout.addLayout(header_layout)

        # save button
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("historyToggle")
        self.save_btn.clicked.connect(self.export_history)
        header_layout.addWidget(self.save_btn)
        # layout.addLayout(header_layout)

        return header_layout
    
    def create_history_list(self):
        # self.calculation_history = list()
        history_list = QListWidget()
        history_list.setObjectName("historyList")
        history_list.itemDoubleClicked.connect(self.on_item_clicked)
        # layout.addWidget(self.history_list)

        return history_list
        
    def create_instructions_label(self):
        instructions = QLabel("Double-click to reuse")
        instructions.setStyleSheet("color: #A0A0A0; font-size: 9pt; font-style: italic;")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(instructions)
        return instructions
        
    def add_calculation(self, expression: str, result: str, operation=None, optional_expression=None):
        if operation:
            item_text = f"{operation}: {expression} => {result}"
            if optional_expression:
                item_text = f"{operation}: {expression}, {optional_expression} => {result}"
        else:
            item_text = f"{expression} = {result}"

        self.calculation_history.append(item_text)

        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, {
            'expression': expression,
            'optional_expression': optional_expression
        })
        self.history_list.insertItem(0, item)

        while self.history_list.count() > 20:
            self.history_list.takeItem(self.history_list.count() - 1)
            
    def on_item_clicked(self, item: QListWidgetItem):
        data = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(data, dict):
            self.history_item_selected.emit(data)
        else:
            self.history_item_selected.emit({ 
                'expression': data,
                'optional_expression': None
            })
    def clear_history(self):
        self.history_list.clear()
        if self.session_manager:
            self.session_manager.clear_history()

    def export_history(self):
        if self.session_manager:
            data_to_export = self.session_manager.get_history()
        else:
            data_to_export = self.calculation_history           
        history_window = HistoryWindow(data_to_export)
        history_window.exec()

    def toggle_visibility(self):
        self.setVisible(not self.isVisible())