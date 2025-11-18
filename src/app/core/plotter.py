"""
plotting functions - creates graphs of expressions
"""

from typing import Union, Tuple, Optional
import sympy as sp
from matplotlib.figure import Figure


class ExpressionPlotter:
    """handles creating graphs and plots"""

    def __init__(self):
        """setup default plotting settings"""
        self.default_range = (-10, 10)
        self.default_points = 1000

    def create_plot(
        self,
        expr: Union[str, sp.Expr],
        variable: str = 'x',
        x_range: Optional[Tuple[float, float]] = None,
        title: Optional[str] = None,
        num_points: int = None
    ) -> Figure:
        """
        create a 2d plot of an expression like x^2 or sin(x)

        TODO:
        - convert string to sympy expr if needed
        - use matplotlib to create figure with plot
        - add grid, axes, labels
        - handle errors nicely
        - return Figure object
        """
        # TODO: implement plotting logic
        pass

    def create_parametric_plot(
        self,
        x_expr: Union[str, sp.Expr],
        y_expr: Union[str, sp.Expr],
        parameter: str = 't',
        param_range: Optional[Tuple[float, float]] = None,
        title: Optional[str] = None,
        num_points: int = None
    ) -> Figure:
        """

        TODO:
        - convert both x_expr and y_expr
        - generate t values from param_range
        - lambdify both expressions
        - plot (x_vals, y_vals)
        """
        # TODO: implement parametric plotting
        pass

    def create_multi_plot(
        self,
        expressions: list,
        variable: str = 'x',
        x_range: Optional[Tuple[float, float]] = None,
        labels: Optional[list] = None,
        title: Optional[str] = None,
        num_points: int = None
    ) -> Figure:
        """
        plot multiple expressions on same graph to compare them

        TODO:
        - loop through expressions list
        - plot each one with different color
        - add legend with labels
        - make sure they all fit on same axes
        """
        # TODO: implement multi-plot
        pass
