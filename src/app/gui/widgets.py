"""
Custom widgets (reusable UI components) for the app.
These are like building blocks we use in the main window.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QDialog, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure    


class HistoryWidget(QWidget):
    
    expression_selected = pyqtSignal(str) 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont('Courier', 10))
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        # add a hint for users
        instructions = QLabel("Double-click to reuse expression")
        instructions.setFont(QFont("Arial", 9))
        instructions.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(instructions)
        
    def add_entry(self, operation: str, input_expr: str, result: str):
        # add a new calculation to history list
          entry_text = f"{operation.upper()}: {input_expr} → {result}"
          
          item = QListWidgetItem(entry_text)
          item.setData(Qt.ItemDataRole.UserRole, input_expr)  # Store the expression for reuse
          self.list_widget.addItem(item)
          
          # gives each operation type a different color
          if operation == 'simplify':
            item.setForeground(Qt.GlobalColor.darkBlue)
          elif operation == 'expand':
            item.setForeground(Qt.GlobalColor.darkGreen)
          elif operation == 'factor':
            item.setForeground(Qt.GlobalColor.darkMagenta)
          elif operation == 'solve':
            item.setForeground(Qt.GlobalColor.darkRed)
            
          self.list_widget.insertItem(0, item) # Newest on top
          
          # only keep last 50 entries
          while self.list_widget.count() > 50:
              self.list_widget.takeItem(self.list_widget.count() - 1)
              
          def on_item_double_clicked(self, item: QListWidgetItem):
              expr = item.data(Qt.ItemDataRole.UserRole)
              self.expression_selected.emit(expr)
              
          def clear(self):
              self.list_widget.clear()
              