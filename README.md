# SLYEST - Simple System for Symbolic Math

A Python-based desktop application for symbolic (non-numerical) calculations including simplification, expansion, factorization, substitution, and solving equations. Built with PyQt6 and SymPy for an accessible and user-friendly mathematical computing experience.

## Features

### Core Functionalities

- **Expression Input**: Enter algebraic expressions via text-based interface
- **Symbolic Operations**: Perform symbolic operations including simplification, expansion, factorization, substitution and solving simple equations.
- **Variable Assignment**: Store expressions in variables for reuse (e.g., `e1 := x + 1`)
- **Equation Solver**: Solve linear algebraic equations or two linear equations symbolically with clear solutions display
- **Session History**: Records up to 20 recent calculations with double-click to reuse expressions

### Additional Features

- **Variable Management**: Store and reuse variables across calculations with an intuitive chip-based display
- **Dark Theme UI**: Modern PyQt6 interface with a sleek dark theme designed for extended use
- **Calculator-Style Input**: Dual input modes - symbolic operation buttons and traditional calculator number pad

## Requirements

- Python 3.10 or higher
- PyQt6 6.6.0+
- SymPy 1.12+
- Matplotlib 3.8.0+

## Installation

### 1. Clone or Download the Project

```bash
cd /path/to/Group_Project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv # On macOS/Linux:
python -m venv .venv # On Windows

# Activate virtual environment
source .venv/bin/activate # On macOS/Linux:
.venv\Scripts\activate # On Windows:
```

### 3. Install Dependencies

```bash
# Install the package and its dependencies
pip install -e .

# Or install from requirements.txt (if generated)
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Check that all packages are installed
pip list | grep -E "sympy|PyQt6|matplotlib"
```

## Running the Application

### Option 1: Running the bash command

```bash
bash run.sh
```

### Option 2: Using the installed command

```bash
# Make sure virtual environment is activated
app
```

### Option 3: Using Python module

```bash
# From the project root directory
python -m app.main
```

### Option 4: Direct execution

```bash
# From the project root directory
python src/app/main.py
```

## Usage Guide

### Basic Operations

1. **Enter an symbolic expression**: Type your mathematical expression in the "Type Expression "input field. Click the calculator buttons if required.

   - Examples: `(x**2 + x)/x`, `sin(x)*cos(x)`, `x**2 - 4 = 0`

2. **Enter an optional expression**: Optional expression is only required for substitution and solving two linear algebriac equations.

   - Examples: `x=3, y=5` for substitution, `x - y = 25` for the second linear equation.

3. **Choose an Operation**: Click one of the operation buttons

   - **Simplify**: Reduce expression to simplest form
   - **Expand**: Expand products and powers
   - **Factor**: Factorize the expression
   - **Solve**: Solve equation for one unknown variable
   - **Substitute**: Substitute the algebraic expression with given values
   - **Solve 2 Equations**: Solve two linear equations for two unknown variables

4. **View Results**: Results appear in the output display area

### Variable Assignment

1. **Assign Variables**

   - Click Manage Button on the top bar to open the variable manager.
   - Fill in the name and the expression that needs to be assigned.
   - Click "Add Variable".

2. **Read Variables and its expressions**

   - Assigned variables are displayed in the variable manager.
   - Moreover, on the top left panel, when hovered the variable, the associated expression is displayed.

3. **Edit and delete variables**

   - Edit and delete the variables in the variable manager window.

4. **Use the variable in future expressions**
   - Once the variable is assigned, we can use those variables in future calculations and history sessions.

### Session History

1. **Open the History Panel**: Click the "History ▼" button in the top-right to show/hide the history panel
2. **Automatic Recording**: Up to 20 calculations of all sorts of operations are automatically saved into the history session.
3. **Reusing Expressions**: Double-click any history item to load that expression back into the input fields
4. **Clearing History**: Use the "Clear" button in the history panel to remove all entries

## Project Structure

```
Group_Project/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py                      # Application entry point
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py           # Main PyQt6 window
│       │   ├── calculator_buttons.py    # Calculator button widgets
│       │   ├── calculator_operations.py # Calculator button logic
│       │   ├── history_panel.py         # History panel widget
│       │   ├── variable_window.py       # Variable manager window
│       │   ├── widgets.py               # Reusable UI components
│       │   └── styles.py                # Dark theme stylesheet
│       ├── core/
│       │   ├── __init__.py
│       │   ├── symbolic_engine.py       # SymPy operations wrapper
│       │   ├── algebraic_expressions.py # Linear Equation solver
│       │   ├── perform_substitution.py  # Substitution operations
│       │   ├── two_linear_equations.py  # Two Linear equations solver
│       │   ├── variable_assignment.py   # Variable management
│       │   ├── parser_validator.py      # Expression parser
│       │   ├── session.py               # Session history data models
│       │   └── plotter.py               # Plotting functionality
│       └── utils/
│           ├── __init__.py
│           └── helpers.py               # Utility functions
├── tests/                               # Unit tests for above individual functions
│   ├── __init__.py
│   ├── test_algebraic_expressions.py
|   ├── test_operators.py
|   ├── test_parser.py
│   ├── test_substitution.py
│   ├── test_two_linear_equations.py
│   └── test_variable_assignment.py
├── .gitignore                           # GitIgnore file
├── requirements.txt                     # Python dependencies
├── run.sh                               # Launch script
├── status.md                            # Development status
└── README.md                            # This file
```

## Development

### Setting Up Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=slyest
```

### Code Formatting

```bash
# Format code with Black
black src/

# Check code style
flake8 src/
```

## Expression Syntax

Here are some common symbolic syntax patterns:

| Mathematical Notation | SLYEST Input |
| --------------------- | ------------ |
| x²                    | `x**2`       |
| √x                    | `sqrt(x)`    |
| sin(x)                | `sin(x)`     |
| e^x                   | `exp(x)`     |
| ln(x)                 | `log(x)`     |
| π                     | `pi`         |
| ∞                     | `oo`         |
| 2x                    | `2*x`        |

## Troubleshooting

### Virtual Environment Issues

If you get "command not found" errors:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### PyQt6 Installation Issues

On some systems, you may need system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6

# macOS (usually works with pip install)
# No additional steps needed
```

### Import Errors

If you get import errors, ensure you're in the project directory and the package is installed:

```bash
# Install in editable mode
pip install -e .
```

## Future Enhancements

Potential features for future versions:

- Differentiation and Integration (calculus functions)
- Learning Mode (step-by-step solutions)
- Custom function definitions
- Matrix operations
- Plotting
- Keyboard shortcuts for common operations
- Any features requested by the clients

## Contributors

**CE-320 Group-8 Students**

## Support

For any issues or questions, please contact the development team or refer to the project documentation.
