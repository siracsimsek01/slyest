"""
Centralized styles and themes for the SLYEST calculator.
Contains color schemes, fonts, and stylesheet definitions.
"""

# Color palette for dark theme (inspired by Apple's calculator)
COLORS = {
    # Background colors
    'main_bg': '#1C1C1E',  # Very dark gray - main window background
    'display_bg': '#2C2C2E',  # Dark gray - display area background

    # Button colors
    'number_btn': '#505050',  # Medium gray - number buttons
    'operation_btn': '#FF9F0A',  # Orange - operation buttons (+, -, ×, ÷, =)
    'scientific_btn': '#3A3A3C',  # Dark gray - scientific function buttons
    'special_btn': '#A5A5A5',  # Light gray - special buttons (AC, %)

    # Text colors
    'text_white': '#FFFFFF',
    'text_black': '#000000',
    'text_gray': '#A0A0A0',
}

# Global application stylesheet
CALCULATOR_STYLESHEET = f"""
    /* Main window background */
    QMainWindow {{
        background-color: {COLORS['main_bg']};
    }}

    /* Central widget */
    QWidget {{
        background-color: {COLORS['main_bg']};
        color: {COLORS['text_white']};
    }}

    /* Display label */
    QLabel#display {{
        background-color: {COLORS['display_bg']};
        color: {COLORS['text_white']};
        border-radius: 10px;
        padding: 20px;
        font-size: 40pt;
        font-weight: bold;
        qproperty-alignment: 'AlignRight | AlignVCenter';
    }}

    /* Expression input field (for typing algebraic expressions) */
    QLineEdit#expressionInput {{
        background-color: {COLORS['display_bg']};
        color: {COLORS['text_white']};
        border: 2px solid {COLORS['scientific_btn']};
        border-radius: 8px;
        padding: 8px 15px;
        font-size: 14pt;
        font-family: 'Courier';
    }}

    QLineEdit#expressionInput:focus {{
        border: 2px solid {COLORS['operation_btn']};
    }}

    QLineEdit#optionalExpressionInput {{
        background-color: {COLORS['display_bg']};
        color: {COLORS['text_white']};
        border: 2px solid {COLORS['scientific_btn']};
        border-radius: 8px;
        padding: 8px 15px;
        font-size: 14pt;
        font-family: 'Courier';
    }}

    QLineEdit#optionalExpressionInput:focus {{
        border: 2px solid {COLORS['operation_btn']};
    }}

    /* Variable bar at top */
    QWidget#variableBar {{
        background-color: {COLORS['display_bg']};
        border-radius: 8px;
        padding: 8px;
    }}

    /* Variable chip button */
    QPushButton#variableChip {{
        background-color: {COLORS['scientific_btn']};
        color: {COLORS['text_white']};
        border: none;
        border-radius: 12px;
        padding: 6px 12px;
        font-size: 11pt;
        font-weight: bold;
    }}

    QPushButton#variableChip:hover {{
        background-color: {COLORS['number_btn']};
    }}

    /* Manage variables button */
    QPushButton#manageVarsBtn {{
        background-color: {COLORS['operation_btn']};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 6px 12px;
        font-size: 11pt;
        font-weight: bold;
    }}

    QPushButton#manageVarsBtn:hover {{
        background-color: #E68A00;
    }}

    /* History panel */
    QWidget#historyPanel {{
        background-color: {COLORS['display_bg']};
        border-radius: 8px;
        padding: 10px;
    }}

    /* History list widget */
    QListWidget#historyList {{
        background-color: {COLORS['main_bg']};
        color: {COLORS['text_white']};
        border: none;
        border-radius: 6px;
        padding: 5px;
        font-family: 'Courier';
        font-size: 11pt;
    }}

    QListWidget#historyList::item {{
        padding: 8px;
        border-radius: 4px;
    }}

    QListWidget#historyList::item:hover {{
        background-color: {COLORS['scientific_btn']};
    }}

    QListWidget#historyList::item:selected {{
        background-color: {COLORS['number_btn']};
    }}

    /* History toggle button */
    QPushButton#historyToggle {{
        background-color: transparent;
        color: {COLORS['text_gray']};
        border: 1px solid {COLORS['text_gray']};
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 10pt;
    }}

    QPushButton#historyToggle:hover {{
        background-color: {COLORS['scientific_btn']};
        color: {COLORS['text_white']};
    }}

    /* Symbolic operation buttons (simplify, expand, factor, etc) */
    QPushButton#symbolicBtn {{
        background-color: {COLORS['operation_btn']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 11pt;
        font-weight: bold;
        min-width: 70px;
    }}

    QPushButton#symbolicBtn:hover {{
        background-color: #E68A00;
    }}

    QPushButton#symbolicBtn:pressed {{
        background-color: #CC7A00;
    }}
"""


def get_calculator_stylesheet() -> str:
    """
    Get the main calculator stylesheet.
    """
    return CALCULATOR_STYLESHEET


def get_dark_theme() -> dict:
    """
    Get the dark theme color dictionary.
    """
    return COLORS.copy()
