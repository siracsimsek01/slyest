from pathlib import Path
import json
import time

import pytest

from yourpkg.function_provider import PatternStore, FunctionProvider
from yourpkg.suggestion import SuggestionType


FULL_JSON = {
    "algebraic": [
        {
            "name": "quadratic",
            "pattern": "x**2 + {b}*x + {c}",
            "description": "Quadratic: x² + bx + c",
            "category": "algebra",
            "commonness": 95,
        },
        {
            "name": "linear",
            "pattern": "{m}*x + {b}",
            "description": "Linear: mx + b",
            "category": "algebra",
            "commonness": 98,
        },
        {
            "name": "binomial_expansion_square",
            "pattern": "(x + {a})**2",
            "description": "Binomial square: (x + a)²",
            "category": "algebra",
            "commonness": 90,
        },
        {
            "name": "difference_of_squares",
            "pattern": "(x + {a})*(x - {a})",
            "description": "Difference of squares: x² − a²",
            "category": "algebra",
            "commonness": 90,
        },
        {
            "name": "product_of_binomials",
            "pattern": "(x + {a})*(x + {b})",
            "description": "Binomial product: (x + a)(x + b)",
            "category": "algebra",
            "commonness": 85,
        },
        {
            "name": "rational_function",
            "pattern": "({a}*x + {b})/({c}*x + {d})",
            "description": "Rational: (ax + b)/(cx + d)",
            "category": "algebra",
            "commonness": 80,
        },
        {
            "name": "cubic",
            "pattern": "x**3 + {a}*x**2 + {b}*x + {c}",
            "description": "Cubic: x³ + ax² + bx + c",
            "category": "algebra",
            "commonness": 75,
        },
        {
            "name": "polynomial_degree_4",
            "pattern": "x**4 + {a}*x**3 + {b}*x**2 + {c}*x + {d}",
            "description": "Quartic: x⁴ + ax³ + bx² + cx + d",
            "category": "algebra",
            "commonness": 60,
        },
        {
            "name": "absolute_linear",
            "pattern": "abs({a}*x + {b})",
            "description": "Absolute value: |ax + b|",
            "category": "algebra",
            "commonness": 80,
        },
        {
            "name": "rational_with_square",
            "pattern": "{a}/x**2",
            "description": "Inverse square: a/x²",
            "category": "algebra",
            "commonness": 70,
        },
    ],
    "trigonometric": [
        {
            "name": "sine_function",
            "pattern": "{a}*sin({b}*x + {c})",
            "description": "Sine wave: a·sin(bx + c)",
            "category": "trigonometry",
            "commonness": 95,
        },
        {
            "name": "cosine_function",
            "pattern": "{a}*cos({b}*x + {c})",
            "description": "Cosine wave: a·cos(bx + c)",
            "category": "trigonometry",
            "commonness": 95,
        },
        {
            "name": "tangent_function",
            "pattern": "tan({a}*x + {b})",
            "description": "Tangent: tan(ax + b)",
            "category": "trigonometry",
            "commonness": 80,
        },
        {
            "name": "sin_squared_plus_cos_squared",
            "pattern": "sin(x)**2 + cos(x)**2",
            "description": "Pythagorean identity: sin²(x) + cos²(x) = 1",
            "category": "trigonometry",
            "commonness": 90,
        },
        {
            "name": "sine_sum",
            "pattern": "sin(x) + sin({a}*x)",
            "description": "Sine sum: sin(x) + sin(ax)",
            "category": "trigonometry",
            "commonness": 70,
        },
        {
            "name": "cosine_sum",
            "pattern": "cos(x) + cos({a}*x)",
            "description": "Cosine sum: cos(x) + cos(ax)",
            "category": "trigonometry",
            "commonness": 70,
        },
        {
            "name": "sine_times_cosine",
            "pattern": "sin(x)*cos(x)",
            "description": "Product: sin(x)·cos(x)",
            "category": "trigonometry",
            "commonness": 75,
        },
        {
            "name": "sine_double_angle",
            "pattern": "2*sin(x)*cos(x)",
            "description": "Double angle: 2sin(x)cos(x) = sin(2x)",
            "category": "trigonometry",
            "commonness": 85,
        },
        {
            "name": "cosine_double_angle",
            "pattern": "cos(x)**2 - sin(x)**2",
            "description": "Double angle: cos²(x) − sin²(x) = cos(2x)",
            "category": "trigonometry",
            "commonness": 85,
        },
        {
            "name": "trig_rational",
            "pattern": "sin(x)/cos(x)",
            "description": "Tangent ratio: sin(x)/cos(x) = tan(x)",
            "category": "trigonometry",
            "commonness": 80,
        },
    ],
    "exponential_logarithmic": [
        {
            "name": "exponential_growth",
            "pattern": "{a}*exp({b}*x)",
            "description": "Exponential growth: a·e^(bx)",
            "category": "exponential",
            "commonness": 95,
        },
        {
            "name": "exponential_decay",
            "pattern": "{a}*exp(-{b}*x)",
            "description": "Exponential decay: a·e^(−bx)",
            "category": "exponential",
            "commonness": 95,
        },
        {
            "name": "power_law",
            "pattern": "{a}*x**{b}",
            "description": "Power law: a·x^b",
            "category": "exponential",
            "commonness": 85,
        },
        {
            "name": "logarithmic",
            "pattern": "{a}*log({b}*x) + {c}",
            "description": "Logarithmic: a·log(bx) + c",
            "category": "logarithmic",
            "commonness": 85,
        },
        {
            "name": "natural_logarithmic",
            "pattern": "{a}*ln({b}*x) + {c}",
            "description": "Natural log: a·ln(bx) + c",
            "category": "logarithmic",
            "commonness": 85,
        },
        {
            "name": "compound_interest",
            "pattern": "{p}*(1 + {r})**{n}",
            "description": "Compound interest: P(1 + r)^n",
            "category": "exponential",
            "commonness": 90,
        },
        {
            "name": "continuous_compound_interest",
            "pattern": "{p}*exp({r}*{t})",
            "description": "Continuous interest: Pe^(rt)",
            "category": "exponential",
            "commonness": 85,
        },
        {
            "name": "log_sum",
            "pattern": "log(x) + log({a})",
            "description": "Log sum: log(x) + log(a) = log(xa)",
            "category": "logarithmic",
            "commonness": 70,
        },
        {
            "name": "log_difference",
            "pattern": "log(x) - log({a})",
            "description": "Log difference: log(x) − log(a) = log(x/a)",
            "category": "logarithmic",
            "commonness": 70,
        },
        {
            "name": "log_ratio",
            "pattern": "log(x/{a})",
            "description": "Log of ratio: log(x/a)",
            "category": "logarithmic",
            "commonness": 75,
        },
    ],
    "calculus": [
        {
            "name": "derivative_power_rule",
            "pattern": "{n}*x**({n}-1)",
            "description": "Power rule: d/dx[x^n] = nx^(n−1)",
            "category": "calculus",
            "commonness": 90,
        },
        {
            "name": "derivative_exponential",
            "pattern": "{a}*exp({a}*x)",
            "description": "Exponential derivative: d/dx[e^(ax)] = ae^(ax)",
            "category": "calculus",
            "commonness": 85,
        },
        {
            "name": "derivative_sine",
            "pattern": "{a}*cos({a}*x)",
            "description": "Sine derivative: d/dx[sin(ax)] = a·cos(ax)",
            "category": "calculus",
            "commonness": 85,
        },
        {
            "name": "derivative_cosine",
            "pattern": "-{a}*sin({a}*x)",
            "description": "Cosine derivative: d/dx[cos(ax)] = −a·sin(ax)",
            "category": "calculus",
            "commonness": 85,
        },
        {
            "name": "integral_power",
            "pattern": "x**({n}+1)/({n}+1)",
            "description": "Power integral: ∫x^n dx = x^(n+1)/(n+1) + C",
            "category": "calculus",
            "commonness": 90,
        },
        {
            "name": "integral_exponential",
            "pattern": "(1/{a})*exp({a}*x)",
            "description": "Exponential integral: ∫e^(ax) dx = (1/a)e^(ax) + C",
            "category": "calculus",
            "commonness": 80,
        },
        {
            "name": "integral_sine",
            "pattern": "-(1/{a})*cos({a}*x)",
            "description": "Sine integral: ∫sin(ax) dx = −(1/a)cos(ax) + C",
            "category": "calculus",
            "commonness": 80,
        },
        {
            "name": "integral_cosine",
            "pattern": "(1/{a})*sin({a}*x)",
            "description": "Cosine integral: ∫cos(ax) dx = (1/a)sin(ax) + C",
            "category": "calculus",
            "commonness": 80,
        },
        {
            "name": "chain_rule",
            "pattern": "f'(g(x))*g'(x)",
            "description": "Chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x)",
            "category": "calculus",
            "commonness": 85,
        },
        {
            "name": "product_rule",
            "pattern": "f(x)*g'(x) + f'(x)*g(x)",
            "description": "Product rule: d/dx[f·g] = f·g' + f'·g",
            "category": "calculus",
            "commonness": 85,
        },
    ],
    "statistics": [
        {
            "name": "arithmetic_mean",
            "pattern": "({x1} + {x2} + {x3})/3",
            "description": "Mean: (x₁ + x₂ + x₃)/3",
            "category": "statistics",
            "commonness": 90,
        },
        {
            "name": "weighted_mean",
            "pattern": "({w1}*{x1} + {w2}*{x2})/({w1} + {w2})",
            "description": "Weighted mean: (w₁x₁ + w₂x₂)/(w₁ + w₂)",
            "category": "statistics",
            "commonness": 80,
        },
        {
            "name": "variance_sample",
            "pattern": "sum((x - mean)**2)/({n}-1)",
            "description": "Variance: Σ(x − μ)²/(n−1)",
            "category": "statistics",
            "commonness": 85,
        },
        {
            "name": "standard_deviation",
            "pattern": "sqrt(variance)",
            "description": "Standard deviation: σ = √variance",
            "category": "statistics",
            "commonness": 85,
        },
        {
            "name": "z_score",
            "pattern": "({x} - {mean})/{std}",
            "description": "Z-score: z = (x − μ)/σ",
            "category": "statistics",
            "commonness": 85,
        },
        {
            "name": "linear_regression",
            "pattern": "{slope}*x + {intercept}",
            "description": "Linear regression: ŷ = mx + b",
            "category": "statistics",
            "commonness": 80,
        },
        {
            "name": "probability_binomial",
            "pattern": "nCr({n}, {k})*{p}**{k}*(1-{p})**({n}-{k})",
            "description": "Binomial probability: C(n,k)·p^k·(1−p)^(n−k)",
            "category": "statistics",
            "commonness": 80,
        },
        {
            "name": "probability_geometric",
            "pattern": "(1-{p})**({k}-1)*{p}",
            "description": "Geometric probability: (1−p)^(k−1)·p",
            "category": "statistics",
            "commonness": 75,
        },
        {
            "name": "correlation_coefficient",
            "pattern": "sum((x-mean_x)*(y-mean_y))/sqrt(sum((x-mean_x)**2)*sum((y-mean_y)**2))",
            "description": "Correlation: r = Σ[(x−x̄)(y−ȳ)]/√[Σ(x−x̄)²·Σ(y−ȳ)²]",
            "category": "statistics",
            "commonness": 75,
        },
        {
            "name": "normal_distribution",
            "pattern": "(1/(sqrt(2*pi)*{sigma}))*exp(-({x}-{mu})**2/(2*{sigma}**2))",
            "description": "Normal PDF: (1/σ√2π)·e^(−(x−μ)²/2σ²)",
            "category": "statistics",
            "commonness": 80,
        },
    ],
}


@pytest.fixture
def patterns_path(tmp_path: Path) -> Path:
    path = tmp_path / "patterns.json"
    path.write_text(json.dumps(FULL_JSON), encoding="utf-8")
    return path


@pytest.fixture
def provider(patterns_path: Path) -> FunctionProvider:
    return FunctionProvider(patterns_path=patterns_path)


def test_pattern_store_loads_all_top_level_keys(patterns_path: Path) -> None:
    store = PatternStore(patterns_path)

    assert set(store.patterns_by_category.keys()) == {
        "algebraic",
        "trigonometric",
        "exponential_logarithmic",
        "calculus",
        "statistics",
    }

    algebraic = store.patterns_by_category["algebraic"]
    assert any(p.name == "linear" for p in algebraic)
    assert any(p.name == "quadratic" for p in algebraic)

    trig = store.patterns_by_category["trigonometric"]
    assert any(p.name == "sine_function" for p in trig)


@pytest.mark.parametrize(
    "query,expected_names",
    [
        ("linear", {"linear", "linear_regression"}),
        ("quadratic", {"quadratic"}),
        ("sine", {"sine_function", "sine_sum", "sine_times_cosine", "sine_double_angle", "derivative_sine", "integral_sine"}),
        ("normal", {"normal_distribution"}),
        ("variance", {"variance_sample"}),
        ("product rule", {"product_rule"}),
    ],
)
def test_pattern_store_matching_with_full_patterns(
    patterns_path: Path,
    query: str,
    expected_names: set,
) -> None:
    store = PatternStore(patterns_path)

    matches = store.find_matching_patterns(query)
    names = {p.name for p in matches}

    assert expected_names.issubset(names)


def test_pattern_store_ranking_uses_commonness(patterns_path: Path) -> None:
    store = PatternStore(patterns_path)

    matches = store.find_matching_patterns("linear")
    names_in_order = [p.name for p in matches]
    assert names_in_order.index("linear") < names_in_order.index("linear_regression")


def test_get_suggestions_empty_input_returns_empty_list(provider: FunctionProvider) -> None:
    assert provider.get_suggestions("") == []
    assert provider.get_suggestions("   ") == []


@pytest.mark.parametrize("text", ["sin", "Sin", "SIN"])
def test_function_suggestions_are_case_insensitive(provider: FunctionProvider, text: str) -> None:
    suggestions = provider.get_suggestions(text)
    assert any(s.text == "sin" and s.type == SuggestionType.FUNCTION for s in suggestions)


def test_constant_suggestions_include_pi(provider: FunctionProvider) -> None:
    suggestions = provider.get_suggestions("pi")
    assert any(s.text == "pi" and s.type == SuggestionType.CONSTANT for s in suggestions)


def test_pattern_suggestions_include_trig_identity(provider: FunctionProvider) -> None:
    suggestions = provider.get_suggestions("sin(x)**2 + cos(x)**2")
    assert any(
        s.type == SuggestionType.PATTERN
        and s.description == "Pythagorean identity: sin²(x) + cos²(x) = 1"
        for s in suggestions
    )


def test_pattern_suggestions_ranking_uses_commonness(provider: FunctionProvider) -> None:
    suggestions = provider.get_suggestions("sin(")
    pattern_suggestions = [s for s in suggestions if s.type == SuggestionType.PATTERN]
    names = [s.text for s in pattern_suggestions]
    assert names and names[0] == "{a}*sin({b}*x + {c})"


def test_max_results_limits_output(provider: FunctionProvider) -> None:
    suggestions = provider.get_suggestions("x", max_results=3)
    assert len(suggestions) <= 3


def test_record_expression_updates_history_and_usage(provider: FunctionProvider) -> None:
    provider.record_expression("sin(x)")
    provider.record_expression("sin(x)")

    assert provider.history[-1] == "sin(x)"

    usage = provider.usage.get("sin(x)")
    assert usage is not None
    assert usage["count"] == 2
    assert usage["last_used"] > 0.0


def test_history_suggestions_include_recent_expressions(provider: FunctionProvider) -> None:
    provider.record_expression("sin(x)")
    provider.record_expression("cos(x)")

    suggestions = provider.get_suggestions("sin")

    assert any(s.text == "sin(x)" and s.type == SuggestionType.HISTORY for s in suggestions)


def test_history_suggestions_ordered_by_recency(provider: FunctionProvider) -> None:
    provider.record_expression("sin(x)")
    provider.record_expression("cos(x)")

    now = time.time()
    provider.usage["sin(x)"]["last_used"] = now - 10
    provider.usage["cos(x)"]["last_used"] = now - 3600

    suggestions = provider.get_suggestions("x")
    hist = [s for s in suggestions if s.type == SuggestionType.HISTORY]

    if len(hist) >= 2:
        assert hist[0].text == "sin(x)"


def test_similarity_score_prefers_prefix_matches(provider: FunctionProvider) -> None:
    full = "sin"
    assert provider._similarity_score("s", full) == 1.0
    assert provider._similarity_score("in", full) == 0.6
    assert provider._similarity_score("x", full) == 0.0


def test_pattern_score_combines_similarity_and_commonness(provider: FunctionProvider) -> None:
    high = provider._pattern_score(similarity=1.0, commonness=100)
    low = provider._pattern_score(similarity=0.0, commonness=100)
    assert high > low
