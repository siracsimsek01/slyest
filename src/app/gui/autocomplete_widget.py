from PyQt6.QtWidgets import (QListWidget, QListWidgetItem, QLabel,
                             QWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
from ..core.autocomplete.suggestion import Suggestion, SuggestionType
from ..core.math_formatter import MathFormatter
from typing import List

class AutoCompleteWidget(QListWidget):
 
   ## Popup widget showing autocomplete suggestions
  

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
        # Use Tool window instead of Popup to avoid blocking input
        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setMaximumHeight(300)
        self.setMinimumWidth(500)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


        self.setStyleSheet("""
            QListWidget#autocompleteWidget {
                background-color: #1C1C1E;
                border: 2px solid #007AFF;
                border-radius: 10px;
                padding: 6px;
                outline: none;
            }

            QListWidget#autocompleteWidget::item {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 3px;
                border-radius: 8px;
                min-height: 50px;
            }

            QListWidget#autocompleteWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #007AFF, stop:1 #0051D5);
                border: none;
            }

            QListWidget#autocompleteWidget::item:hover {
                background-color: #2C2C2E;
            }

            QListWidget#autocompleteWidget::item:selected:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #0A84FF, stop:1 #005ED5);
            }

            QScrollBar:vertical {
                background-color: #1C1C1E;
                width: 10px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background-color: #3A3A3C;
                border-radius: 5px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #4A4A4C;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

    def show_suggestions(self, suggestions: List[Suggestion]):
        self.clear()
        self.current_suggestions = suggestions

        for suggestion in suggestions:
            item = QListWidgetItem()

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
        container = QWidget()
        container.setObjectName("suggestionItem")
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(12, 10, 12, 10)
        main_layout.setSpacing(15)


        icon_label = QLabel(suggestion.icon)
        icon_label.setFont(QFont("Arial", 18))
        icon_label.setFixedWidth(32)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_label)

 
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        text_layout.setContentsMargins(0, 0, 0, 0)


        formatted_label = MathFormatter.to_display(suggestion.display_label)
        main_label = QLabel(formatted_label)
        main_label.setFont(QFont("SF Pro", 13, QFont.Weight.DemiBold))
        main_label.setStyleSheet("color: #FFFFFF; padding: 0px;")
        main_label.setWordWrap(False)
        text_layout.addWidget(main_label)

        if suggestion.description:
            formatted_desc = MathFormatter.to_display(suggestion.description)
            desc_label = QLabel(formatted_desc)
            desc_label.setFont(QFont("SF Pro", 10))
            desc_label.setStyleSheet("color: #98989D; padding: 0px;")
            desc_label.setWordWrap(False)
            # Truncate long descriptions
            if len(formatted_desc) > 60:
                desc_label.setText(formatted_desc[:60] + "...")
            text_layout.addWidget(desc_label)

        main_layout.addLayout(text_layout, 1)

        # type badge with improved styling
        badge_label = QLabel(suggestion.type_name)
        badge_label.setFont(QFont("SF Pro", 9, QFont.Weight.Bold))
        badge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_label.setFixedHeight(24)
        badge_label.setMinimumWidth(60)
        badge_label.setStyleSheet(f"""
            QLabel {{
                background-color: {suggestion.type_badge_color};
                color: white;
                border-radius: 12px;
                padding: 4px 10px;
                font-weight: bold;
            }}
        """)
        main_layout.addWidget(badge_label)

        # Set overall container style
        container.setStyleSheet("""
            QWidget#suggestionItem {
                background-color: transparent;
                padding: 2px;
            }
        """)

        return container
    
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