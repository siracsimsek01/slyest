#  necessary packages to be used in the main window GUI
from ..core.symbolic_engine import SymbolicEngine
from ..core.session import SessionManager
from ..utils.helpers import format_expression, validate_expression
from src.app.core.perform_substitution import perform_substitution
from src.app.core.algebraic_expressions import AlgebraicExpressions
from src.app.core.two_linear_equations import TwoLinearEquations
from src.app.core.variable_assignment import VariableManager

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QSplitter, QMessageBox, QMenuBar, QMenu,
    QFileDialog, QComboBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QAction, QIcon

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.engine = SymbolicEngine()
        self.session = SessionManager()
        self.substitution = QPushButton("Substitute")
        self.solve_equation = QPushButton("Solve one equation")
        self.solve_two_linear_equations = QPushButton("Solve two equations")
        self.equations_solver = AlgebraicExpressions()
        self.two_linear_equations_solver = TwoLinearEquations()
        
        
        self.init_ui()
        self.apply_stylesheet()
        
    def init_ui(self):
        
        self.setWindowTitle("SLYEST - Main Window")
        self.setGeometry(100, 100, 1200, 800)
        
        self.create_menu_bar() 
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        # Create a splitter so user can resize the left/right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side: where we enter expressions and click buttons
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right side: shows calculation history
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        
        splitter.setSizes([840, 360])

        main_layout.addWidget(splitter)

        # Bottom status bar that shows messages
        self.statusBar().showMessage("Ready")
  
    def create_menu_bar(self):
        """Create the menu bar at the top"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Add actions to file menu
        new_action = QAction("New Session", self)
        new_action.triggered.connect(self.new_session)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
    def create_left_panel(self):
        """Create the left panel with input and operation buttons"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Input area
        input_label = QLabel("Enter Expression:")
        layout.addWidget(input_label)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., x**2 + 2*x + 1")
        layout.addWidget(self.input_field)
        
        optional_input_label = QLabel("Optional: Only input a substitute value for substitution <or> second equation for solving two linear equations.")
        layout.addWidget(optional_input_label)
        
        self.optional_input_field = QLineEdit()
        self.optional_input_field.setPlaceholderText("e.g., x=5, y=3 for substitution <or> x - y = 12 for solving two linear equations.")
        layout.addWidget(self.optional_input_field)
        layout.addSpacing(20)
        
        # Operation buttons
        button_layout = QHBoxLayout()
        
        simplify_btn = QPushButton("Simplify")
        simplify_btn.clicked.connect(self.simplify_expression)
        button_layout.addWidget(simplify_btn)
        
        expand_btn = QPushButton("Expand")
        expand_btn.clicked.connect(self.expand_expression)
        button_layout.addWidget(expand_btn)
        
        factor_btn = QPushButton("Factor")
        factor_btn.clicked.connect(self.factor_expression)
        button_layout.addWidget(factor_btn)
        
        layout.addLayout(button_layout)
        
        ########

        layout.addSpacing(10)

        my_buttons_layout = QHBoxLayout()

        my_buttons_layout.addWidget(self.substitution)
        my_buttons_layout.addWidget(self.solve_equation)
        my_buttons_layout.addWidget(self.solve_two_linear_equations)

        layout.addLayout(my_buttons_layout)


        self.substitution.clicked.connect(self.on_substitution_clicked)
        self.solve_equation.clicked.connect(self.on_solve_equation_clicked)
        self.solve_two_linear_equations.clicked.connect(self.on_two_linear_equations_clicked)
        
        layout.addSpacing(10)

        ########

        # Output area
        output_label = QLabel("Result:")
        layout.addWidget(output_label)
        
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)
        
        layout.addStretch()
         
        return panel
    
    def create_right_panel(self):
        """Create the right panel with history"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        history_label = QLabel("History:")
        layout.addWidget(history_label)
        
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        self.history_list.itemClicked.connect(self.show_calculations_when_clicked)
        
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        layout.addWidget(clear_btn)
        
        return panel
    
    def show_calculations_when_clicked(self, item):
        entry = item.data(Qt.ItemDataRole.UserRole)
        if entry:
            self.input_field.setText(entry.input_expr)
            self.optional_input_field.setText(entry.optional_input_expr)
        self.output_display.clear()
    
    def apply_stylesheet(self):
        """Apply a basic stylesheet for better appearance"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
        """)
    
    def simplify_expression(self):
        """Simplify the entered expression"""
        try:
            expr_str = self.input_field.text()
            if not expr_str:
                return
            
            expr = self.engine.parse_expression(expr_str)
            result = expr.simplify()
            
            # Display result
            formatted = format_expression(result)
            self.output_display.setPlainText(formatted)
            
            # Add to history
            from ..core.session import HistoryEntry
            entry = HistoryEntry("Simplify", expr_str, result)
            self.session.history.append(entry)
            item = QListWidgetItem(str(entry))
            item.setData(Qt.ItemDataRole.UserRole, entry)
            self.history_list.addItem(item)

            self.statusBar().showMessage("Simplified successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to simplify: {str(e)}")
    
    def expand_expression(self):
        """Expand the entered expression"""
        try:
            expr_str = self.input_field.text()
            if not expr_str:
                return
            
            expr = self.engine.parse_expression(expr_str)
            result = expr.expand()
            
            formatted = format_expression(result)
            self.output_display.setPlainText(formatted)
            
            from ..core.session import HistoryEntry
            entry = HistoryEntry("Expand", expr_str, result)
            self.session.history.append(entry)
            item = QListWidgetItem(str(entry))
            item.setData(Qt.ItemDataRole.UserRole, entry)
            self.history_list.addItem(item)
            
            
            self.statusBar().showMessage("Expanded successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to expand: {str(e)}")
    
    def factor_expression(self):
        """Factor the entered expression"""
        try:
            expr_str = self.input_field.text()
            if not expr_str:
                return
            
            import sympy as sp
            expr = self.engine.parse_expression(expr_str)
            result = sp.factor(expr)
            
            formatted = format_expression(result)
            self.output_display.setPlainText(formatted)
            
            from ..core.session import HistoryEntry
            entry = HistoryEntry("Factor", expr_str, result)
            self.session.history.append(entry)
            item = QListWidgetItem(str(entry))
            item.setData(Qt.ItemDataRole.UserRole, entry)
            self.history_list.addItem(item)
            
            self.statusBar().showMessage("Factored successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to factor: {str(e)}")
    
    def new_session(self):
        """Start a new session"""
        self.session.clear_history()
        self.history_list.clear()
        self.input_field.clear()
        self.output_display.clear()
        self.statusBar().showMessage("New session started")
    
    def clear_history(self):
        """Clear the history"""
        self.session.clear_history()
        self.history_list.clear()
        self.statusBar().showMessage("History cleared")
    
    ######
    def on_substitution_clicked(self):
        expr_str = self.input_field.text()
        subs_str = self.optional_input_field.text()

        #Check for empty inputs
        if not expr_str:
            QMessageBox.critical(self, "Error", "Error: Expression field is empty.")
            return
            
        if not subs_str:
            QMessageBox.critical(self, "Error", "Error: Substitution field is empty.")
            return
        
        subs_dict = {} #example turns a string "x=5, y=3" into a dict {'x': '5', 'y': '3'}
        try:
            # Split by comma for multiple substitutions
            for part in subs_str.split(','):
                # Split by '=' to get key and value
                key, value = part.split('=')
                # Adds them to the dictionary
                subs_dict[key.strip()] = value.strip()
        except Exception as e:
            # If the string is bad (e.g., "x+5"), show an error
            QMessageBox.critical(self, "Input Error", 
                                 f"Invalid substitution format.\n"
                                 f"Please use 'x=5' or 'x=5, y=3'.\n\nError: {e}")
        
        result, success = perform_substitution(expr_str, subs_dict)

        
        if success:
            self.output_display.setPlainText(result)
            self.statusBar().showMessage("Substitution successful")
            from ..core.session import HistoryEntry
            entry = HistoryEntry("Substitution", expr_str, str(result), subs_str)

            item = QListWidgetItem(str(entry))   
            item.setData(Qt.ItemDataRole.UserRole, entry)     
            self.history_list.addItem(item)
            self.session.history.append(entry)

        else:
            QMessageBox.critical(self, "Error", result)
            self.statusBar().showMessage("Substitution failed")
        
   
    def on_solve_equation_clicked(self):
        
        try:
            
            expr_str = self.input_field.text()

            
            if not expr_str:
                QMessageBox.critical(self, "Input Error", "Error: Expression field is empty.")
                return

            
            result = self.equations_solver.solve_algerbraic_equation(expr_str)

            
            if result:
                self.output_display.setPlainText(str(result))
                self.statusBar().showMessage("Algebraic equation solved")
                
                
                from ..core.session import HistoryEntry
                entry = HistoryEntry("Assignment", expr_str, str(result))
                item = QListWidgetItem(str(entry))
                item.setData(Qt.ItemDataRole.UserRole, entry) 
                self.history_list.addItem(item)
                self.session.history.append(entry)
                
            else:
                QMessageBox.critical(self, "Error", "Error in input equation. Please type again.")
                self.statusBar().showMessage("Solving equation failed")

        except Exception as e:
            QMessageBox.critical(self, "Critical Error", f"An unexpected error occurred: {e}")
            self.statusBar().showMessage("An unexpected error occurred")
        
    def on_two_linear_equations_clicked(self):
        try:
            
            expr_str_1 = self.input_field.text()
            expr_str_2 = self.optional_input_field.text()

            
            if not expr_str_1 and expr_str_2:
                QMessageBox.critical(self, "Input Error", "Error: Expression field is empty.")
                return

            
            result = self.two_linear_equations_solver.solve_two_linear_equations(expr_str_1, expr_str_2)

            
            if result:
                result_str = ""
                for var in result:
                    if type(var) == tuple:
                        result_str += ''.join(str(var))
                    else:
                        result_str += f'{var}: {result[var]}   '
                self.output_display.setPlainText(result_str)
                self.statusBar().showMessage("Two linear equations solved")
                
                
                from ..core.session import HistoryEntry
                entry = HistoryEntry("Assignment", expr_str_1, str(result), expr_str_2)
                item = QListWidgetItem(str(entry))
                item.setData(Qt.ItemDataRole.UserRole, entry) 
                self.history_list.addItem(item)
                self.session.history.append(entry)
                
            else:
                QMessageBox.critical(self, "Error", "Error in input equation. Please type again.")
                self.statusBar().showMessage("Solving two linear equations failed")

        except Exception as e:
            QMessageBox.critical(self, "Critical Error", f"An unexpected error occurred: {e}")
            self.statusBar().showMessage("An unexpected error occurred") 