from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import json
import time

from .suggestion import Suggestion, SuggestionType


@dataclass
class Pattern:
    name: str
    template: str
    description: str
    category: str
    commonness: int


class PatternStore:
    def __init__(self, json_path: Path) -> None:
        self.patterns_by_category: Dict[str, List[Pattern]] = {}
        self._load_from_file(json_path)

    def find_matching_patterns(self, partial_text: str) -> List[Pattern]:
        normalized_text = partial_text.lower().strip()
        if not normalized_text:
            return []

        matches: List[Pattern] = []
        for patterns in self.patterns_by_category.values():
            for pattern in patterns:
                if self._matches_text(normalized_text, pattern):
                    matches.append(pattern)

        ranked = sorted(
            matches,
            key=lambda pattern: (
                self._similarity_score(normalized_text, pattern),
                pattern.commonness,
            ),
            reverse=True,
        )
        return ranked

    def _load_from_file(self, json_path: Path) -> None:
        raw = json.loads(json_path.read_text(encoding="utf-8"))
        for category, items in raw.items():
            patterns: List[Pattern] = []
            for item in items:
                patterns.append(
                    Pattern(
                        name=item["name"],
                        template=item["pattern"],
                        description=item["description"],
                        category=item.get("category", category),
                        commonness=int(item.get("commonness", 50)),
                    )
                )
            self.patterns_by_category[category] = patterns

    def _matches_text(self, text: str, pattern: Pattern) -> bool:
        lowered = text.lower()
        return (
            lowered in pattern.name.lower()
            or lowered in pattern.template.lower()
            or lowered in pattern.description.lower()
        )

    def _similarity_score(self, text: str, pattern: Pattern) -> float:
        name = pattern.name.lower()
        body = pattern.template.lower()
        if name.startswith(text):
            return 1.0
        if text in name:
            return 0.8
        if body.startswith(text):
            return 0.6
        if text in body:
            return 0.4
        return 0.0


class FunctionProvider:
    decay_half_life_seconds = 60 * 60 * 24

    def __init__(self, patterns_path: Path) -> None:
        self.functions: Dict[str, str] = self._build_functions()
        self.constants: Dict[str, str] = self._build_constants()
        self.categories: Dict[str, str] = self._build_categories()
        self.history: List[str] = []
        self.usage: Dict[str, Dict[str, float]] = {}
        self.pattern_store = PatternStore(patterns_path)

    def get_suggestions(self, partial_text: str, max_results: int = 5) -> List[Suggestion]:
        normalized_text = partial_text.strip()
        if not normalized_text:
            return []

        history_suggestions = self._build_history_suggestions(normalized_text)
        function_suggestions = self._build_function_suggestions(normalized_text)
        constant_suggestions = self._build_constant_suggestions(normalized_text)
        pattern_suggestions = self._build_pattern_suggestions(normalized_text)

        all_suggestions = (
            history_suggestions
            + function_suggestions
            + constant_suggestions
            + pattern_suggestions
        )

        ranked = sorted(all_suggestions, key=lambda suggestion: suggestion.score, reverse=True)
        return ranked[:max_results]

    def record_expression(self, expression: str) -> None:
        normalized_expression = expression.strip()
        if not normalized_expression:
            return

        self.history.append(normalized_expression)
        self._increment_usage(normalized_expression)

    def _build_history_suggestions(self, partial_text: str) -> List[Suggestion]:
        seen = set()
        suggestions: List[Suggestion] = []

        for expression in reversed(self.history):
            if expression in seen:
                continue
            seen.add(expression)

            similarity = self._similarity_score(partial_text, expression)
            if similarity == 0.0:
                continue

            score = self._history_score(expression, similarity)
            suggestions.append(
                Suggestion(
                    label=expression,
                    value=expression,
                    type=SuggestionType.HISTORY,
                    score=score,
                )
            )

        return suggestions

    def _build_function_suggestions(self, partial_text: str) -> List[Suggestion]:
        suggestions: List[Suggestion] = []

        for name, description in self.functions.items():
            similarity = self._similarity_score(partial_text, name)
            if similarity == 0.0:
                continue

            label = f"{name}(x) - {description}"
            score = self._reference_score(similarity, base_frequency=20.0, base_recency=20.0)

            suggestions.append(
                Suggestion(
                    label=label,
                    value=name,
                    type=SuggestionType.FUNCTION,
                    score=score,
                )
            )

        return suggestions

    def _build_constant_suggestions(self, partial_text: str) -> List[Suggestion]:
        suggestions: List[Suggestion] = []

        for name, description in self.constants.items():
            similarity = self._similarity_score(partial_text, name)
            if similarity == 0.0:
                continue

            label = f"{name} - {description}"
            score = self._reference_score(similarity, base_frequency=10.0, base_recency=10.0)

            suggestions.append(
                Suggestion(
                    label=label,
                    value=name,
                    type=SuggestionType.CONSTANT,
                    score=score,
                )
            )

        return suggestions

    def _build_pattern_suggestions(self, partial_text: str) -> List[Suggestion]:
        patterns = self.pattern_store.find_matching_patterns(partial_text)
        suggestions: List[Suggestion] = []

        for pattern in patterns:
            label = f"{pattern.template}  [{pattern.description}]"
            similarity = self.pattern_store._similarity_score(partial_text, pattern)
            score = self._pattern_score(similarity, pattern.commonness)

            suggestions.append(
                Suggestion(
                    label=label,
                    value=pattern.template,
                    type=SuggestionType.PATTERN,
                    score=score,
                )
            )

        return suggestions

    def _history_score(self, expression: str, similarity: float) -> float:
        frequency_score = self._frequency_score(expression)
        recency_score = self._recency_score(expression)
        similarity_score = similarity * 100.0
        return (
            frequency_score * 0.4
            + recency_score * 0.3
            + similarity_score * 0.3
        )

    def _reference_score(self, similarity: float, base_frequency: float, base_recency: float) -> float:
        similarity_score = similarity * 100.0
        return (
            base_frequency * 0.4
            + base_recency * 0.3
            + similarity_score * 0.3
        )

    def _pattern_score(self, similarity: float, commonness: int) -> float:
        similarity_score = similarity * 100.0
        commonness_score = float(commonness)
        return commonness_score * 0.5 + similarity_score * 0.5

    def _frequency_score(self, expression: str) -> float:
        entry = self.usage.get(expression)
        if not entry:
            return 0.0

        count = entry.get("count", 0)
        capped_count = min(count, 50)
        return (capped_count / 50.0) * 100.0

    def _recency_score(self, expression: str) -> float:
        entry = self.usage.get(expression)
        if not entry:
            return 0.0

        last_used = entry.get("last_used", 0.0)
        age = max(0.0, time.time() - last_used)

        decay_factor = 0.5 ** (age / self.decay_half_life_seconds)
        return 100.0 * decay_factor

    def _similarity_score(self, partial_text: str, candidate: str) -> float:
        lowered_partial = partial_text.lower()
        lowered_candidate = candidate.lower()

        if not lowered_partial or not lowered_candidate:
            return 0.0
        if lowered_candidate.startswith(lowered_partial):
            return 1.0
        if lowered_partial in lowered_candidate:
            return 0.6
        return 0.0

    def _increment_usage(self, expression: str) -> None:
        entry = self.usage.setdefault(expression, {"count": 0, "last_used": 0.0})
        entry["count"] += 1
        entry["last_used"] = time.time()

    def _build_functions(self) -> Dict[str, str]:
        return {
            "add": "addition",
            "sub": "subtraction",
            "mul": "multiplication",
            "div": "division",
            "pow": "power",
            "sqrt": "square root",
            "cbrt": "cube root",
            "exp": "exponential",
            "log": "logarithm base 10",
            "ln": "natural logarithm",
            "sin": "sine",
            "cos": "cosine",
            "tan": "tangent",
            "cot": "cotangent",
            "sec": "secant",
            "csc": "cosecant",
            "asin": "inverse sine",
            "acos": "inverse cosine",
            "atan": "inverse tangent",
            "sinh": "hyperbolic sine",
            "cosh": "hyperbolic cosine",
            "tanh": "hyperbolic tangent",
            "asinh": "inverse hyperbolic sine",
            "acosh": "inverse hyperbolic cosine",
            "atanh": "inverse hyperbolic tangent",
            "abs": "absolute value",
            "floor": "floor",
            "ceil": "ceiling",
            "round": "round",
            "mean": "mean",
            "sum": "sum",
            "min": "minimum",
            "max": "maximum",
            "gamma": "gamma function",
            "factorial": "factorial",
        }

    def _build_constants(self) -> Dict[str, str]:
        return {
            "pi": "pi",
            "e": "e",
            "tau": "tau",
            "phi": "golden ratio",
            "oo": "infinity",
        }

    def _build_categories(self) -> Dict[str, str]:
        return {
            "sin": "trigonometry",
            "cos": "trigonometry",
            "tan": "trigonometry",
            "cot": "trigonometry",
            "sec": "trigonometry",
            "csc": "trigonometry",
            "asin": "trigonometry",
            "acos": "trigonometry",
            "atan": "trigonometry",
            "sinh": "trigonometry",
            "cosh": "trigonometry",
            "tanh": "trigonometry",
            "asinh": "trigonometry",
            "acosh": "trigonometry",
            "atanh": "trigonometry",
            "pow": "powers",
            "sqrt": "roots",
            "cbrt": "roots",
            "exp": "exponentials",
            "log": "logarithms",
            "ln": "logarithms",
            "abs": "algebra",
            "floor": "rounding",
            "ceil": "rounding",
            "round": "rounding",
            "mean": "statistics",
            "sum": "statistics",
            "min": "statistics",
            "max": "statistics",
            "gamma": "special",
            "factorial": "special",
        }
