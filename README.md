# SLYEST - Simple System for Symbolic Math

A Python-based desktop application for symbolic (non-numerical) calculations including simplification, expansion, factorization, substitution, and solving equations. Built with PyQt6 and SymPy for an accessible, user-friendly mathematical computing experience.

**CE320 Group Projects 2025 - Group 8**

## Features

### Core Functionality
- **Expression Input**: Enter algebraic expressions via text-based interface
- **Symbolic Operations**:
  - Simplification
  - Expansion
  - Factorization
  - Substitution
  - Solving algebraic equations
- **Variable Assignment**: Store expressions in variables for reuse (e.g., `e1 := x + 1`)
- **Equation Solver**: Solve algebraic equations symbolically with clear solution display

### Additional Features
- **Session History**: Complete record of past calculations with the ability to scroll back and reuse expressions
- **Plotting Support**: Graph mathematical expressions using matplotlib integration
- **Rich PyQt6 GUI**: Modern, accessible user interface designed for users with varying mathematical backgrounds
- **Export Functionality**: Save session history as text, JSON, or LaTeX format

## Requirements

- Python 3.10 or higher
- PyQt6 6.6.0+
- SymPy 1.12+
- Matplotlib 3.8.0+

## Installation

### 1. Clone or Download the Project

```bash
cd /path/to/slyest
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
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

### Option 1: Using the installed command

```bash
# Make sure virtual environment is activated
app
```

### Option 2: Using Python module

```bash
# From the project root directory
python -m app.main
```

### Option 3: Direct execution

```bash
# From the project root directory
python src/app/main.py
```

## Usage Guide

### Basic Operations

1. **Enter an Expression**: Type your mathematical expression in the input field
   - Examples: `(x^2 + x)/x`, `sin(x)*cos(x)`, `x^2 - 4`

2. **Choose an Operation**: Click one of the operation buttons
   - **Simplify**: Reduce expression to simplest form
   - **Expand**: Expand products and powers
   - **Factor**: Factor the expression
   - **Solve**: Solve equation for unknown variable

3. **View Results**: Results appear in the output display area

### Variable Assignment

1. Enter and evaluate an expression
2. Type a variable name in the "Variable name" field (e.g., `e1`)
3. Click "Assign Last Result"
4. Use the variable in future expressions

### Plotting

1. Enter an expression containing a variable (e.g., `x^2 + 2*x + 1`)
2. Click the "Plot" button
3. A new window opens showing the graph
4. Use the toolbar to zoom, pan, and save the plot

### Session History

- All operations are automatically recorded in the history panel
- Double-click any history entry to reuse that expression
- Export history via File → Export History menu

## Project Structure

```
slyest/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # Application entry point
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py   # Main PyQt6 window
│       │   └── widgets.py       # Custom widgets
│       ├── core/
│       │   ├── __init__.py
│       │   ├── symbolic_engine.py  # SymPy operations wrapper
│       │   ├── session.py       # Session history management
│       │   └── plotter.py       # Plotting functionality
│       └── utils/
│           ├── __init__.py
│           └── helpers.py       # Utility functions
├── tests/                       # Unit tests
│   └── __init__.py
├── .gitignore
├── pyproject.toml              # Project configuration
└── README.md                   # This file
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

SLYEST uses SymPy's expression parser. Here are some common syntax patterns:

| Mathematical Notation | SLYEST Input |
|----------------------|--------------|
| x² | `x**2` or `x^2` |
| √x | `sqrt(x)` |
| sin(x) | `sin(x)` |
| e^x | `exp(x)` |
| ln(x) | `log(x)` |
| π | `pi` |
| ∞ | `oo` |
| 2x | `2*x` or `2x` |

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
- 3D plotting support
- Keyboard shortcuts for common operations

## License

MIT License - See project documentation for details.

## Contributors

**Group 8** - CE320 Group Projects 2025
- Clients: Rahmat and GLAs

## Support

For issues, questions, or contributions, please contact the development team or refer to the project documentation.

---

Built with ❤️ using Python, PyQt6, and SymPy
