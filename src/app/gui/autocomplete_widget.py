from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..core.autocomplete.suggestion import Suggestion, SuggestionTyp
from typing import List

class AutoCompleteWidget(QListWidget):
    """
    Popup widget showing autocomplete suggestions
    """
    
    suggestion_selected = pyqtSignal(Suggestion)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("autocompleteWidget")
        self.setup_ui()
        self.current_suggestions = []
        
        # Connect signals
        self.itemClicked.connect(self.on_item_clicked)
    
    def setup_ui(self):
        """Configure widget appearance"""
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMaximumHeight(200)
        self.setMinimumWidth(300)
        
        # TODO: Add styling (dark theme, hover effects)
        # Hint: Use styles.py or inline stylesheets
    
    def show_suggestions(self, suggestions: List[Suggestion]):
        """Display suggestions in the popup"""
        self.clear()
        self.current_suggestions = suggestions
        
        for suggestion in suggestions:
            item = QListWidgetItem()
            
            # TODO: Create custom widget for each item
            # Should show: icon, text, type badge, description
            widget = self._create_suggestion_item(suggestion)
            
            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)
        
        if suggestions:
            self.setCurrentRow(0)  # Select first item
            self.show()
        else:
            self.hide()
    
    def _create_suggestion_item(self, suggestion: Suggestion) -> QWidget:
        """create a custom widget for displaying a suggestion"""
        # TODO: Build widget with:
        pass
    
    def on_item_clicked(self, item: QListWidgetItem):
        row = self.row(item)
        suggestion = self.current_suggestions[row]
        self.suggestion_selected.emit(suggestion)
        self.hide()
    
    def move_selection_up(self):
        current = self.currentRow()
        if current > 0:
            self.setCurrentRow(current - 1)
    
    def move_selection_down(self):
        current = self.currentRow()
        if current < self.count() - 1:
            self.setCurrentRow(current + 1)
    
    def accept_current(self):
        current_item = self.currentItem()
        if current_item:
            self.on_item_clicked(current_item)