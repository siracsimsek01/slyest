### History Panel widget for the calculator

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class HistoryPanel(QWidget):
    ### widget that displays calculation history
    history_item_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        ### create the history panel
        super().__init__(parent)
        self.setObjectName("historyPanel")
        self.isVisible = False
        self.init_ui()
        
    def init_ui(self):
        ### set up the user interface
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # header with title and clear button
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

        layout.addLayout(header_layout)

        # history list
        self.history_list = QListWidget()
        self.history_list.setObjectName("historyList")
        self.history_list.itemDoubleClicked.connect(self.on_item_clicked)
        layout.addWidget(self.history_list)
        
         # Instructions label
        instructions = QLabel("Double-click to reuse")
        instructions.setStyleSheet("color: #A0A0A0; font-size: 9pt; font-style: italic;")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
    def add_calculation(self, expression: str, result: str):
        """
        add a calculation to history

        Args:
            expression: the expression string
            result: the result of the calculation
        """
        #format expression = result 
        item_text = f"{expression} = {result}"
        
        # create list item
        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, expression) # store expression for reuse
        
        # add to top of list 
        self.history_list.insertItem(0, item)
        
        # limit to last 20 entries
        while self.history_list.count() > 20:
            self.history_list.takeItem(self.history_list.count() - 1)
            
    def on_item_clicked(self, item: QListWidgetItem):
              # Get the stored expression
        expression = item.data(Qt.ItemDataRole.UserRole)

        # Emit signal so calculator can use it
        self.history_item_selected.emit(expression)

    def clear_history(self):
        """Clear all history items."""
        self.history_list.clear()

    def toggle_visibility(self):
        """Toggle between showing and hiding the history panel."""
        self.is_visible = not self.is_visible
        self.setVisible(self.is_visible)