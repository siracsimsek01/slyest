from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, 
    QFrame, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont
from typing import List, Dict

class StepPanel(QWidget):
    """
    displays step by step solutions with latex rendering
    """
    
    close_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_steps = []
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        header = self._create_header()
        layout.addWidget(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # container for step cards
        self.steps_container = QWidget()
        self.steps_layout = QVBoxLayout(self.steps_container)
        self.steps_layout.setSpacing(10)
        self.steps_layout.setContentsMargins(15, 15, 15, 15)
        
        scroll.setWidget(self.steps_container)
        layout.addWidget(scroll)
        
        self.setStyleSheet("""
            QWidget {
                background: #1E1E1E;
            }
            QScrollArea {
                border: none;
                background: #1E1E1E;
            }
        """)
    
    def _create_header(self) -> QWidget:
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: #2A2A2A;
                border-bottom: 2px solid #FF9F0A;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(header)
        
        # title
        title = QLabel("Step-by-Step Solution")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF9F0A; border: none;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # close button
        close_btn = QPushButton("✕")
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FFFFFF;
                border: none;
                font-size: 20pt;
                padding: 5px 10px;
            }
            QPushButton:hover {
                color: #FF9F0A;
            }
        """)
        close_btn.clicked.connect(self.close_requested.emit)
        layout.addWidget(close_btn)
        
        return header
    
    def show_steps(self, steps: List[Dict], animate: bool = True):
        # clear previous steps
        self._clear_steps()
        
        self.current_steps = steps
        
        # create step cards
        for i, step in enumerate(steps):
            card = self._create_step_card(i + 1, step)
            self.steps_layout.addWidget(card)
            
        
            if animate:
                self._animate_card(card, delay=i * 150)
        
        # add stretch at bottom
        self.steps_layout.addStretch()
    
    def _create_step_card(self, step_num: int, step: Dict) -> QFrame:
  
        card = QFrame()
        card.setObjectName("stepCard")
        
        if step.get('is_final', False):
            border_color = "#4CAF50"  # green for answer
            bg_color = "#2A3A2A"
        else:
            border_color = "#FF9F0A"  # orange for steps
            bg_color = "#2A2A2A"
        
        card.setStyleSheet(f"""
            QFrame#stepCard {{
                background: {bg_color};
                border-left: 4px solid {border_color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        
        # step number and title
        header_layout = QHBoxLayout()
        
        step_label = QLabel(f"Step {step_num}")
        step_label.setStyleSheet(f"color: {border_color}; font-weight: bold; font-size: 10pt;")
        header_layout.addWidget(step_label)
        
        title = QLabel(step['title'])
        title.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size: 12pt;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # math expression (HARD: latex rendering)
        expr_widget = self._create_math_display(step['expression'])
        layout.addWidget(expr_widget)
        
        # explanation
        explanation = QLabel(step['explanation'])
        explanation.setWordWrap(True)
        explanation.setStyleSheet("color: #B0B0B0; font-size: 11pt; padding: 5px 0;")
        layout.addWidget(explanation)
        
        # rule name
        rule = QLabel(f"📚 {step['rule']}")
        rule.setStyleSheet("color: #808080; font-style: italic; font-size: 9pt;")
        layout.addWidget(rule)
        
        # initially hidden for animation
        card.setMaximumHeight(0)
        card.setVisible(False)
        
        return card
    
    def _create_math_display(self, expression: str) -> QWidget:
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: #1E1E1E;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(container)
        
        # convert math expression to displayable format
        formatted_expr = self._format_math_simple(expression)
        
        expr_label = QLabel(formatted_expr)
        expr_label.setFont(QFont("Courier New", 14))
        expr_label.setStyleSheet("color: #FFFFFF; background: transparent;")
        expr_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(expr_label)
        
        return container
    
    def _format_math_simple(self, expression: str) -> str:
        """
        format math expression for display
    
        conversions:
        - ** → superscript
        - sqrt() → √
        - * → ×
        - / → fraction (or ÷)
        """
        formatted = expression
        
        # replace operators
        formatted = formatted.replace('*', ' × ')
        formatted = formatted.replace('/', ' ÷ ')
        
        # handle powers: x**2 → x²
        import re
        formatted = re.sub(r'\*\*(\d)', lambda m: self._to_superscript(m.group(1)), formatted)
        
        # handle sqrt
        formatted = formatted.replace('sqrt(', '√(')
        
        # wrap in monospace font
        return f'<span style="font-family: Courier New; font-size: 14pt;">{formatted}</span>'
    
    def _to_superscript(self, digit: str) -> str:
        superscripts = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                       '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
        return superscripts.get(digit, digit)
    
    def _animate_card(self, card: QFrame, delay: int = 0):
        from PyQt6.QtCore import QTimer
        
        def show_card():
            card.setVisible(True)
            
            # calculate target height
            card.setMaximumHeight(16777215)  # remove max height temporarily
            target_height = card.sizeHint().height()
            card.setMaximumHeight(0)  # reset for animation
            
            # create animation
            animation = QPropertyAnimation(card, b"maximumHeight")
            animation.setDuration(400)  # 400ms
            animation.setStartValue(0)
            animation.setEndValue(target_height)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            # start animation
            animation.start()
            
            # keep reference so it doesn't get garbage collected
            card.animation = animation
        
        # delay start if specified
        if delay > 0:
            QTimer.singleShot(delay, show_card)
        else:
            show_card()
    
    def _clear_steps(self):
        while self.steps_layout.count():
            item = self.steps_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def clear(self):
        self._clear_steps()
        self.current_steps = []