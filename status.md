# SLYEST | project status

## whats done

### ui components
- calculator window done with all buttons
- dark theme colors working
- variable manager works
- history panel shows calculations
- text input field for typing expressions (not implemented yet, just ui)
- symbolic operation buttons added: simplify, expand, factor, solve, substitute, plot (ui only, not implemented)

### backend
- symbolic_engine.py is working (simplify, expand, factor, solve, substitute)
- basic calculator operations work: numbers, +, -, ×, ÷, =, AC, decimal

## whats NOT done

### calculator_operations.py
only 8 out of 40 functions work. the rest are empty with TODO comments.

working:
- input_number
- input_decimal
- operation_add, subtract, multiply, divide
- calculate_result
- clear_all

not working (need to implement):
- parentheses
- powers and roots (x², √, etc)
- trig functions (sin, cos, tan)
- logs (ln, log)
- memory (mc, m+, m-, mr)
- special stuff (±, %, factorial, pi, e)
- everything else...

### expression handlers in calculator_window.py
need to implement 4 handler functions:

1. handle_expression_input() - when user types expression and presses enter
2. handle_symbolic_operation() - when clicking simplify/expand/factor/solve buttons
3. handle_substitute() - when clicking substitute button
4. handle_plot() - when clicking plot button

all have TODO comments with hints on what to do.

### plotting
file: plotter.py

all three functions are empty templates:
- create_plot
- create_parametric_plot
- create_multi_plot

used to work but had wrong imports (PyQt5 instead of PyQt6). now its empty for us to implement.

## what works right now

- you can click number buttons and see numbers
- basic math works: 5 + 3 = 8
- AC button clears
- variables window opens and you can manage variables
- history shows your calculations

## what doesnt work

- cant type expressions and press enter (field exists but no logic)
- most scientific buttons dont work (sin, sqrt, etc)
- parentheses dont work
- memory buttons dont work
- plotting is broken/empty
- cant do algebra like "2*x + 5" in calculator mode

## what we need to do

1. finish implementing calculator_operations.py (32 functions left)
2. implement the expression input handler so typing works
3. implement plotting functions

## how to test

run calculator:
```
python -m app.main
```

try basic math - works
try scientific functions - doesnt work yet
try typing expression and pressing enter - doesnt work yet

## files to edit

calculator_operations.py - 32 functions to implement
plotter.py - 3 functions to implement
calculator_window.py - 4 handler functions to implement

## files to NOT edit

symbolic_engine.py - already works
styles.py - styling done
main_window.py - ui done (except those 4 handler functions)
calculator_buttons.py - done
variable_window.py - done
history_panel.py - done
main.py - entry point, done

## completion estimate

honestly like 30-35% done

ui is 80% done
backend symbolic engine is 100% done
calculator operations maybe 20% done
plotting 0% done
expression input 0% done


