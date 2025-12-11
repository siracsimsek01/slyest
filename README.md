# SLYEST - Scientific Calculator for Learning and Educational Study Tool

A powerful Python-based desktop application for symbolic mathematics with intelligent autocomplete, step-by-step learning mode, and beautiful mathematical formatting. Built with PyQt6 and SymPy for an accessible and user-friendly mathematical computing experience.

## Features

### Core Functionalities

- **Smart Autocomplete**: Intelligent suggestion system with 100+ mathematical patterns, functions, and your calculation history
- **Expression Input**: Enter algebraic expressions via text-based interface with live mathematical formatting
- **Symbolic Operations**: Perform symbolic operations including simplification, expansion, factorization, substitution, and solving equations
- **Variable Assignment**: Store expressions in variables for reuse across calculations
- **Equation Solver**: Solve linear algebraic equations or systems of two linear equations symbolically
- **Calculus Operations**: Differentiate and integrate symbolic expressions
- **Interactive Plotting**: Visualize mathematical functions with customizable ranges
- **Session History**: Records up to 20 recent calculations with double-click to reuse expressions

### Advanced Features

#### **Intelligent Autocomplete System**
- **Real-time Suggestions**: As you type, get instant suggestions for functions, patterns, and history
- **Smart Ranking**: Suggestions ranked by relevance, usage frequency, and recency
- **5 Suggestion Types**:
  -  **Functions**: 35+ mathematical functions (sin, cos, sqrt, exp, log, etc.)
  -  **Constants**: Mathematical constants (π, e, φ, τ, ∞)
  - **Patterns**: 50+ mathematical templates (quadratic, sine waves, derivatives, integrals, statistics)
  - **History**: Previously used expressions
  - **Variables**: User-defined variables
- **Pattern Library**: Pre-defined templates for:
  - Algebraic expressions (quadratic, cubic, binomials)
  - Trigonometric functions (sine/cosine waves, identities)
  - Exponential & logarithmic models (growth, decay, compound interest)
  - Calculus formulas (derivatives, integrals, chain rule, product rule)
  - Statistics (mean, variance, z-score, normal distribution)
- **Keyboard Navigation**: Use ↑/↓ to navigate, Tab/Enter to select, Esc to close
- **Works on Both Inputs**: Autocomplete available for both expression and optional input fields

#### **Enhanced Learning Mode**
- **Step-by-Step Solutions**: Detailed breakdown of each calculation step
- **Educational Explanations**: Clear explanations of mathematical concepts and operations
- **Helpful Hints**: Tips for understanding each step
- **Common Mistakes**: Warnings about typical errors to avoid
- **Follow-up Questions**: Thought-provoking questions to deepen understanding
- **FOIL Method Visualization**: Special breakdown for binomial expansion showing First, Outer, Inner, Last steps
- **Beautiful UI**: Color-coded steps with proper mathematical formatting

#### **Mathematical Formatting**
- **Auto-formatted Display**: Expressions automatically formatted for readability
  - `x**2` → `x²` (superscripts)
  - `5*x` → `5x` (implicit multiplication)
  - `sqrt(x)` → `√x` (mathematical symbols)
  - Proper fraction display
- **Consistent Notation**: All inputs and outputs use beautiful mathematical notation

### User Interface

- **Dark Theme UI**: Modern PyQt6 interface with sleek dark theme designed for extended use
- **Dual Input Modes**:
  - Symbolic operation buttons (Simplify, Expand, Factor, Solve, etc.)
  - Traditional calculator number pad with scientific functions
- **Variable Management**: Intuitive chip-based display showing last 5 variables with tooltips
- **History Panel**: Collapsible panel showing recent calculations
- **Real-time Formatting**: See mathematical notation as you type

## Requirements

- Python 3.10 or higher
- PyQt6 6.6.0+
- SymPy 1.12+
- Matplotlib 3.8.0+
- rapidfuzz (optional, for fuzzy autocomplete matching)

## Installation

### 1. Clone or Download the Project

```bash
cd /path/to/Group_Project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv  # On macOS/Linux
python -m venv .venv   # On Windows

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

```bash
# Install the package and its dependencies
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt

# Optional: Install rapidfuzz for better autocomplete
pip install rapidfuzz
```

### 4. Verify Installation

```bash
# Check that all packages are installed
pip list | grep -E "sympy|PyQt6|matplotlib"
```

## Running the Application

### Option 1: Running the bash command (Recommended)

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
python -m src.app.main
```

### Option 4: Direct execution

```bash
# From the project root directory
python src/app/main.py
```

## Usage Guide

### Basic Operations

1. **Enter a symbolic expression**: Type your mathematical expression in the "Type Expression" input field
   - Examples: `(x**2 + x)/x`, `sin(x)*cos(x)`, `x**2 - 4 = 0`
   - Use autocomplete: Start typing "sin" and see suggestions appear!

2. **Enter an optional expression**: Required for substitution, solving two equations, differentiation, and integration
   - Examples:
     - `x=3, y=5` for substitution
     - `x - y = 25` for the second linear equation
     - `x` for differentiation/integration variable

3. **Choose an Operation**: Click one of the operation buttons
   - **Simplify**: Reduce expression to simplest form
   - **Expand**: Expand products and powers
   - **Factor**: Factorize the expression
   - **Solve**: Solve equation for one unknown variable
   - **Substitute**: Replace variables with given values
   - **Solve 2 Equations**: Solve system of two linear equations
   - **Differentiate**: Find the derivative with respect to a variable
   - **Integrate**: Find the indefinite integral
   - **Plot**: Visualize the expression as a graph

4. **View Results**: Results appear in the output display area with beautiful mathematical formatting

5. **Learning Mode**: Click the **?** button next to the result to see step-by-step solution

### Using Autocomplete

1. **Trigger Suggestions**: Start typing in any input field
   - Suggestions appear after 150ms
   - Minimum 1 character required

2. **Navigate Suggestions**:
   - **↓** (Down Arrow): Move to next suggestion
   - **↑** (Up Arrow): Move to previous suggestion
   - **Tab** or **Enter**: Accept selected suggestion
   - **Esc**: Close autocomplete dropdown
   - **Click**: Select with mouse

3. **Autocomplete Examples**:
   - Type `sin` → See sine function, sine patterns, and sine history
   - Type `quad` → See quadratic formula patterns
   - Type `log` → See logarithm functions and patterns
   - Type `der` → See derivative patterns
   - Type `int` → See integral patterns

4. **Pattern Placeholders**: Patterns use `{a}`, `{b}`, `{c}` as placeholders
   - Example: `{a}*sin({b}*x + {c})` → Replace with your values

### Variable Assignment

1. **Assign Variables**
   - Click **Manage** button on the top bar to open the variable manager
   - Fill in the name and the expression that needs to be assigned
   - Click "Add Variable"

2. **View Variables**
   - Assigned variables are displayed in the variable manager
   - Top left panel shows last 5 variables
   - Hover over variable chips to see their expressions

3. **Edit and Delete Variables**
   - Edit and delete variables in the variable manager window

4. **Use Variables**
   - Once assigned, variables can be used in calculations
   - Variables appear in autocomplete suggestions
   - Click variable chips to insert them into expressions

### Session History

1. **Open the History Panel**: Click the "History ▼" button in the top-right
2. **Automatic Recording**: Up to 20 calculations are automatically saved
3. **Reusing Expressions**: Double-click any history item to load it back
4. **Clearing History**: Use the "Clear" button to remove all entries
5. **History in Autocomplete**: Recent expressions appear in autocomplete

### Learning Mode

1. **Trigger Learning Mode**: After any calculation, click the **?** button
2. **View Step-by-Step**: See detailed breakdown of the solution
3. **Read Explanations**: Each step includes:
   - What was done
   - Why it was done
   - Mathematical rules applied
   - Hints and tips
   - Common mistakes to avoid
   - Follow-up questions

4. **FOIL Visualization**: For binomial expansion, see special FOIL breakdown
   - First, Outer, Inner, Last steps shown separately
   - Color-coded boxes for each component

### Plotting Functions

1. **Enter Expression**: Type a function like `sin(x)`, `x**2`, or `exp(-x)`
2. **Click Plot**: Opens the plotting panel
3. **Customize**:
   - Set x-axis range (min/max)
   - Set y-axis range (min/max)
   - Add multiple functions to compare
4. **View Graph**: Interactive plot with gridlines

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
│       │   ├── learning_mode_window.py  # Step-by-step learning mode
│       │   ├── plotting_panel.py        # Interactive plotting panel
│       │   ├── autocomplete_widget.py   # Autocomplete dropdown UI
│       │   └── styles.py                # Dark theme stylesheet
│       ├── core/
│       │   ├── __init__.py
│       │   ├── symbolic_engine.py       # SymPy operations wrapper
│       │   ├── algebraic_expressions.py # Linear equation solver
│       │   ├── perform_substitution.py  # Substitution operations
│       │   ├── two_linear_equations.py  # Two linear equations solver
│       │   ├── variable_assignment.py   # Variable management
│       │   ├── parser_validator.py      # Expression parser
│       │   ├── session.py               # Session history data models
│       │   ├── plotter.py               # Plotting functionality
│       │   ├── math_formatter.py        # Mathematical notation formatter
│       │   ├── symbolic_to_decimal.py   # Format conversion
│       │   ├── step_solver/
│       │   │   ├── operation_router.py  # Routes operations to solvers
│       │   │   └── explanation_enhancer.py # Generates educational explanations
│       │   └── autocomplete/
│       │       ├── autocomplete_manager.py  # Manages autocomplete logic
│       │       ├── suggestion.py            # Suggestion data structure
│       │       ├── function_provider.py     # Provides function suggestions
│       │       ├── history_provider.py      # Provides history suggestions
│       │       ├── pattern_provider.py      # Provides pattern suggestions
│       │       └── patterns.json            # Mathematical pattern templates
│       └── utils/
│           ├── __init__.py
│           └── helpers.py               # Utility functions
├── tests/                               # Unit tests
│   ├── __init__.py
│   ├── test_algebraic_expressions.py
│   ├── test_operators.py
│   ├── test_parser.py
│   ├── test_substitution.py
│   ├── test_two_linear_equations.py
│   ├── test_variable_assignment.py
│   ├── test_autocomplete.py
│   └── test_detailed_explanations.py
├── .gitignore                           # GitIgnore file
├── requirements.txt                     # Python dependencies
├── run.sh                               # Launch script
└── README.md                            # This file
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_autocomplete.py

# Run with coverage
pytest --cov=src
```


## Expression Syntax

Here are common symbolic syntax patterns:

| Mathematical Notation | Input Syntax | Display Output |
| --------------------- | ------------ | -------------- |
| x²                    | `x**2`       | x²             |
| x³                    | `x**3`       | x³             |
| √x                    | `sqrt(x)`    | √x             |
| ³√x                   | `cbrt(x)`    | ³√x            |
| sin(x)                | `sin(x)`     | sin(x)         |
| cos²(x)               | `cos(x)**2`  | cos(x)²        |
| eˣ                    | `exp(x)`     | eˣ             |
| ln(x)                 | `ln(x)`      | ln(x)          |
| log₁₀(x)              | `log(x)`     | log(x)         |
| π                     | `pi`         | π              |
| e                     | `E`          | e              |
| ∞                     | `oo`         | ∞              |
| 2x                    | `2*x`        | 2x             |
| x/y                   | `x/y`        | x/y            |
| \|x\|                 | `abs(x)`     | \|x\|          |

## Example Use Cases

### Example 1: Simplifying Expressions
```
Input: (x**2 + 2*x + 1)/(x + 1)
Operation: Simplify
Output: x + 1
```

### Example 2: Expanding Binomials (with Learning Mode)
```
Input: (x + 2)*(x + 3)
Operation: Expand
Output: x² + 5x + 6

Learning Mode shows FOIL steps:
  First:  x * x = x²
  Outer:  x * 3 = 3x
  Inner:  2 * x = 2x
  Last:   2 * 3 = 6
  Result: x² + 5x + 6
```

### Example 3: Solving Equations
```
Input: x**2 - 5*x + 6 = 0
Operation: Solve
Output: [2, 3]
```

### Example 4: Differentiation
```
Input: sin(x**2)
Optional: x
Operation: Differentiate
Output: 2x·cos(x²)
```

### Example 5: Using Autocomplete
```
Typing "sin" shows:
  sin(x) - Sine function
  {a}*sin({b}*x + {c}) - Sine wave pattern
  sin(x)**2 + cos(x)**2 - Pythagorean identity
  sin(x) + cos(x) - From your history
```

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

# No additional steps needed
```

### Import Errors

If you get import errors, ensure you're in the project directory and the package is installed:

```bash
# Install in editable mode
pip install -e .
```

### Autocomplete Not Showing

If autocomplete doesn't appear:
1. Make sure you're typing at least 1 character
2. Wait 150ms after typing (debounce delay)
3. Avoid typing pure numbers (e.g., "12" won't trigger autocomplete)
4. Check that the input field has focus

### Performance Issues

If autocomplete is slow:
```bash
# Install rapidfuzz for faster fuzzy matching
pip install rapidfuzz
```

## Recent Updates

### Version 2.0 (Latest)
- **Plotting**: Plotting the equations.
- **Calculus Support**: Differentaiton and Integration Operations.
- **Intelligent Autocomplete System**: 100+ suggestions with smart ranking
- **Enhanced Learning Mode**: Detailed explanations with hints and warnings
- **Mathematical Formatting**: Beautiful display with superscripts and implicit multiplication
- **Save/Export Feature**: Users now can export and save their calcualtions.
- **FOIL Visualization**: Special breakdown for binomial expansion
- **Pattern Library**: 50+ pre-defined mathematical templates
- **Improved UI**: Better spacing, colors, and visual feedback

### Version 1.0
- Core symbolic operations (simplify, expand, factor, solve)
- Variable management system
- Session history tracking
- Two-equation solver
- Plotting functionality
- Dark theme UI

## Future Enhancements

Potential features for future versions:

- Custom function definitions
- Matrix operations
- More calculus features (limits, series)
- Export results to LaTeX/PDF
- Advanced plotting (3D, parametric)
- Keyboard shortcuts customization
- Save/load sessions
- Any features requested by users

## Contributors

**CE320 Group-8 Students**

## Support

For any issues or questions:
- Check this README for common solutions
- Contact the development team
- Refer to the project documentation

## 📄 License

This project is developed as part of CE320 coursework.

---

**Made with ❤️ by Group 8 | Powered by PyQt6 & SymPy**
