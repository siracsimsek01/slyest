#  necessary packages to be used in the main window GUI
from ..core.symbolic_engine import SymbolicEngine
from ..core.session import SessionManager
from ..utils.helpers import format_expression, validate_expression
from ..gui.styles import get_calculator_stylesheet
from ..gui.history_panel import HistoryPanel
from ..gui.calculator_button import CalculatorButton

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QSplitter, QMessageBox, QMenuBar, QMenu,
    QFileDialog, QComboBox, QListWidget, QListWidgetItem, QGridLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QAction, QIcon

class MainWindow(QMainWindow):
    
    def __init__(self):
        """Set up the calculator window."""
        super().__init__()
        self.setWindowTitle("SLYEST - Scientific Calculator")
        self.setGeometry(100, 100, 800, 900)
    
        # create the calculation engine
        self.engine = SymbolicEngine()

        # Current expression being built
        self.current_expression = ""

        # apply the dark theme stylesheet
        self.setStyleSheet(get_calculator_stylesheet())

        # create the main UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the main UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # top bar Variables + History toggle
        self.create_top_bar(main_layout)

        # display area
        self.create_display(main_layout)

        # history panel (initially hidden)
        self.create_history_panel(main_layout)

        # Bottom status bar that shows messages
        self.create_buttons(main_layout)
    
    def create_top_bar(self, parent_layout):
        """Create the top bar with variables and history button."""
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        # variable chips container
        var_container = QWidget()
        var_container.setObjectName("variableBar")
        var_layout = QHBoxLayout(var_container)
        var_layout.setSpacing(8)

        # label
        var_label = QLabel("Variables:")
        var_label.setStyleSheet("color: #A0A0A0; font-size: 10pt;")
        var_layout.addWidget(var_label)

        # container for variable buttons (last 5)
        self.variable_buttons_layout = QHBoxLayout()
        self.variable_buttons_layout.setSpacing(6)
        var_layout.addLayout(self.variable_buttons_layout)

        # initially show none message
        # self.refresh_variable_display()

        var_layout.addStretch()

        # manage variables button
        manage_btn = QPushButton("Manage")
        manage_btn.setObjectName("manageVarsBtn")
        # manage_btn.clicked.connect(self.open_variable_manager)
        var_layout.addWidget(manage_btn)

        top_bar_layout.addWidget(var_container)

        # history toggle button
        history_btn = QPushButton("History ▼")
        history_btn.setObjectName("historyToggle")
        # history_btn.clicked.connect(self.toggle_history)
        top_bar_layout.addWidget(history_btn)

        parent_layout.addWidget(top_bar)
        
    def create_display(self, parent_layout):
        """create the display area for showing expressions and results."""
        
        # subdisplay for the expression being typed
        self.subdisplay = QLabel("0")
        self.subdisplay.setObjectName("subdisplay")
        self.subdisplay.setMinimumHeight(35)
        parent_layout.addWidget(self.subdisplay)

        # Main display for results
        self.display = QLabel("0")
        self.display.setObjectName("display")
        self.display.setMinimumHeight(100)
        parent_layout.addWidget(self.display)
    
    def create_history_panel(self, parent_layout):
        """Create the collapsible history panel."""
        self.history_panel = HistoryPanel()
        # self.history_panel.history_item_selected.connect(self.use_history_item)
        self.history_panel.setVisible(False)  # start hidden
        self.history_panel.setMaximumHeight(200)
        parent_layout.addWidget(self.history_panel)
        
    def create_buttons(self, parent_layout):
        """Create the button grid with two column layout."""
        # container for buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)

        # left column: Scientific functions
        scientific_grid = self.create_scientific_buttons()
        button_layout.addLayout(scientific_grid, 2)  # takes 2/3 of space

        # right column: Number pad + operations
        number_grid = self.create_number_pad()
        button_layout.addLayout(number_grid, 1)  # takes 1/3 of space

        parent_layout.addWidget(button_container)
        
    def create_scientific_buttons(self) -> QGridLayout:
        """create the left column with scientific function buttons."""
        grid = QGridLayout()
        grid.setSpacing(6)

        # row 0: Parentheses and memory
        row0 = [
            ("(", "special"),
            (")", "special"),
            ("mc", "scientific"),
            ("m+", "scientific"),
            ("m-", "scientific"),
            ("mr", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row0):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 0, col)

        # row 1: Powers and exponentials
        row1 = [
            ("2ⁿᵈ", "scientific"),
            ("x²", "scientific"),
            ("x³", "scientific"),
            ("xʸ", "scientific"),
            ("eˣ", "scientific"),
            ("10ˣ", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row1):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 1, col)

        # row 2: roots and logarithms
        row2 = [
            ("1/x", "scientific"),
            ("²√x", "scientific"),
            ("³√x", "scientific"),
            ("ʸ√x", "scientific"),
            ("ln", "scientific"),
            ("log₁₀", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row2):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 2, col)

        # row 3: Trigonometry and constants
        row3 = [
            ("x!", "scientific"),
            ("sin", "scientific"),
            ("cos", "scientific"),
            ("tan", "scientific"),
            ("e", "scientific"),
            ("π", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row3):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 3, col)

        # row 4: hyperbolic and special
        row4 = [
            ("Rand", "scientific"),
            ("sinh", "scientific"),
            ("cosh", "scientific"),
            ("tanh", "scientific"),
            ("EE", "scientific"),
            ("Rad", "scientific"),
        ]
        for col, (text, btn_type) in enumerate(row4):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 4, col)

        return grid
    
    
    def create_number_pad(self) -> QGridLayout:
        """Create the right column with number pad and operations."""
        grid = QGridLayout()
        grid.setSpacing(6)

        # row 0
        row0 = [
            ("AC", "special"),
            ("±", "special"),
            ("%", "special"),
            ("÷", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row0):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 0, col)

        # row 1
        row1 = [
            ("7", "number"),
            ("8", "number"),
            ("9", "number"),
            ("×", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row1):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 1, col)

        # row 2
        row2 = [
            ("4", "number"),
            ("5", "number"),
            ("6", "number"),
            ("−", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row2):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 2, col)

        # row 3
        row3 = [
            ("1", "number"),
            ("2", "number"),
            ("3", "number"),
            ("+", "operation"),
        ]
        for col, (text, btn_type) in enumerate(row3):
            btn = CalculatorButton(text, btn_type)
            grid.addWidget(btn, 3, col)

        # Row 4: 0 (span 2 cols), ., =
        btn_0 = CalculatorButton("0", "number")
        btn_0.setMinimumWidth(128)
        grid.addWidget(btn_0, 4, 0, 1, 2)  # Span 2 columns

        btn_dot = CalculatorButton(".", "number")
        grid.addWidget(btn_dot, 4, 2)

        btn_equals = CalculatorButton("=", "operation")
        grid.addWidget(btn_equals, 4, 3)

        return grid
    
    ### TODO: Implement Variable Manager
    
    
    
    ### TODO: Create history window
    