from typing import Union, Tuple, Optional, Dict, List
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

class ExpressionPlotter:

    def __init__(self, variables: Optional[Dict[str, str]] = None):
        self.default_range = (-10, 10)
        self.default_points = 1000
        self.variables = variables or {}
        self.transformations = (standard_transformations + (implicit_multiplication_application,))
        self.local_dict = {
            'x': sp.Symbol('x'), 't': sp.Symbol('t'), 'y': sp.Symbol('y'),
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'log': sp.log, 'pi': sp.pi,
            'sqrt': sp.sqrt, 'abs': sp.Abs, 'ln': sp.ln, 'E': sp.E
        }

    def set_variables(self, variables: Dict[str, str]):
        self.variables = variables

    def _substitute_variables(self, expr: sp.Expr) -> sp.Expr:
        if not self.variables:
            return expr
        
        substitutions = {}
        for var_name, var_value in self.variables.items():
            try:
                substitutions[sp.Symbol(var_name)] = self._parse(var_value)
            except Exception:
                continue
        
        return expr.subs(substitutions) if substitutions else expr

    def _parse(self, expr: Union[str, sp.Expr]) -> sp.Expr:
        if isinstance(expr, str):
            return parse_expr(expr, transformations=self.transformations, local_dict=self.local_dict)
        return expr

    def create_plot(
        self,
        expr: Union[str, sp.Expr],
        variable: str = 'x',
        x_range: Optional[Tuple[float, float]] = None,
        title: Optional[str] = None,
        num_points: int = None,
        substitute_vars: bool = True
    ) -> Figure:
        try:
            expr = self._parse(expr)
            if substitute_vars:
                expr = self._substitute_variables(expr)

            x = sp.symbols(variable)
            
            x_range = x_range or self.default_range
            num_points = num_points or self.default_points
            xs = np.linspace(float(x_range[0]), float(x_range[1]), num_points)
            
            free_vars = expr.free_symbols
            if len(free_vars) > 1:
                var_names = ', '.join(str(v) for v in free_vars)
                raise ValueError(f"Expression contains multiple variables ({var_names}). 2D plotting requires a single variable. Try using variable substitution to reduce to one variable.")
            
            if len(free_vars) == 0:
                const_value = float(expr.evalf())
                ys = np.full_like(xs, const_value)
            else:
                f = sp.lambdify(x, expr, 'numpy')
                with np.errstate(divide='ignore', invalid='ignore'):
                    ys = f(xs)

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(xs, ys, label=str(expr), linewidth=2)
            ax.set_xlabel(variable, fontsize=12)
            ax.set_ylabel(f"f({variable})", fontsize=12)
            ax.set_title(title or f"Plot of {expr}", fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            return fig
        except Exception as e:
            raise ValueError(f"Error plotting expression: {e}")

    def create_parametric_plot(
        self,
        x_expr: Union[str, sp.Expr],
        y_expr: Union[str, sp.Expr],
        parameter: str = 't',
        param_range: Optional[Tuple[float, float]] = None,
        title: Optional[str] = None,
        num_points: int = None,
        substitute_vars: bool = True
    ) -> Figure:
        try:
            x_expr = self._parse(x_expr)
            y_expr = self._parse(y_expr)
            if substitute_vars:
                x_expr = self._substitute_variables(x_expr)
                y_expr = self._substitute_variables(y_expr)

            t = sp.symbols(parameter)
            
            x_free_vars = x_expr.free_symbols
            if len(x_free_vars) > 1:
                var_names = ', '.join(str(v) for v in x_free_vars)
                raise ValueError(f"X expression contains multiple variables ({var_names}). Parametric plotting requires expressions of a single parameter.")
            
            y_free_vars = y_expr.free_symbols
            if len(y_free_vars) > 1:
                var_names = ', '.join(str(v) for v in y_free_vars)
                raise ValueError(f"Y expression contains multiple variables ({var_names}). Parametric plotting requires expressions of a single parameter.")
            
            fx = sp.lambdify(t, x_expr, 'numpy')
            fy = sp.lambdify(t, y_expr, 'numpy')

            param_range = param_range or self.default_range
            num_points = num_points or self.default_points
            ts = np.linspace(float(param_range[0]), float(param_range[1]), num_points)
            xs, ys = fx(ts), fy(ts)

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(xs, ys, label=f"({x_expr}, {y_expr})", linewidth=2)
            ax.set_xlabel(f"x({parameter})", fontsize=12)
            ax.set_ylabel(f"y({parameter})", fontsize=12)
            ax.set_title(title or "Parametric Plot", fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            ax.axis('equal')
            return fig
        except Exception as e:
            raise ValueError(f"Error plotting parametric expression: {e}")

    def create_multi_plot(
        self,
        expressions: List,
        variable: str = 'x',
        x_range: Optional[Tuple[float, float]] = None,
        labels: Optional[List] = None,
        title: Optional[str] = None,
        num_points: int = None,
        substitute_vars: bool = True
    ) -> Figure:
        try:
            x = sp.symbols(variable)
            x_range = x_range or self.default_range
            num_points = num_points or self.default_points
            xs = np.linspace(float(x_range[0]), float(x_range[1]), num_points)

            fig, ax = plt.subplots(figsize=(10, 6))

            for i, expr in enumerate(expressions):
                expr = self._parse(expr)
                if substitute_vars:
                    expr = self._substitute_variables(expr)

                free_vars = expr.free_symbols
                if len(free_vars) > 1:
                    var_names = ', '.join(str(v) for v in free_vars)
                    raise ValueError(f"Expression '{expr}' contains multiple variables ({var_names}). Please use single-variable expressions only.")   

                if len(expr.free_symbols) == 0:
                    const_value = float(expr.evalf())
                    ys = np.full_like(xs, const_value)
                else:
                    f = sp.lambdify(x, expr, 'numpy')
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ys = f(xs)

                label = labels[i] if labels and i < len(labels) else str(expr)
                ax.plot(xs, ys, label=label, linewidth=2)

            ax.set_xlabel(variable, fontsize=12)
            ax.set_ylabel(f"f({variable})", fontsize=12)
            ax.set_title(title or "Multiple Plots", fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            return fig
        except Exception as e:
            raise ValueError(f"Error plotting multiple expressions: {e}")

class PlotWindowManager:
    
    @staticmethod
    def create_plot_window(parent_widget, figure: Figure, window_title: str = "Plot"):
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
    
        dialog = QDialog(parent_widget)
        dialog.setWindowTitle(window_title)
        dialog.resize(850, 700)
        dialog.setModal(False)  
        
        layout = QVBoxLayout()
        canvas = FigureCanvasQTAgg(figure)
        toolbar = NavigationToolbar2QT(canvas, dialog)
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        
        layout.addWidget(canvas)
        layout.addWidget(toolbar)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        
        dialog.exec()  
    
        return dialog