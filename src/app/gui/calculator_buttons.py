from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont

class CalculatorButton(QPushButton):
    """Custom button for calculator with fixed size and font."""
    
    def __init__(self, text: str, button_type: str = "number", parent=None):

        super().__init__(text, parent)
        self.button_type = button_type
        self.button_text = text
        
        # set up the button appearance
        self.setup_style()
        self.setup_font()
        self.setMinimumSize(QSize(60, 60))
        
    def setup_style(self):
        
        base_style = """
        QPushButton {
                border-radius: 12px;
                border: none;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QPushButton:pressed {
                opacity: 0.6;
            }
        """
        
        # different colors for different button types
        if self.button_type == "operation":
            color_style = """
            background-color: #FF9F0A;
            color: white;
            """
            
        elif self.button_type == "special":
            # light gray for special functions AC, %, remove
            color_style = """
                background-color: #A5A5A5;
                color: black;
            """
        elif self.button_type == "scientific":
            # Dark gray for scientific functions (sin, cos, log, etc.)
            color_style = """
                background-color: #3A3A3C;
                color: white;
            """
        else:  # number type
            # Regular gray for number buttons
            color_style = """
                background-color: #505050;
                color: white;
            """
            
        self.setStyleSheet(base_style + "QPushButton {" + color_style + "}")
        
    def setup_font(self):
        """Set appropriate font size based on button type."""
        font = QFont()

        # Scientific buttons get smaller font (more text to fit)
        if self.button_type == "scientific":
            font.setPointSize(13)
        else:
            font.setPointSize(18)

        font.setBold(True)
        self.setFont(font)
        
class LargeCalculatorButton(CalculatorButton):
        
        def __init__(self, text: str, button_type: str = "number", parent=None):
            super().__init__(text, button_type, parent)
            self.setMinimumSize(QSize(130, 60))  # wider button