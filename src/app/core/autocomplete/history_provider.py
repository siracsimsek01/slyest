from typing import List, Dict
from collections import Counter
from datetime import datetime
import math
from .suggestion import Suggestion, SuggestionType

try:
    from rapidfuzz import fuzz
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False
    print("warning: rapidfuzz not installed. run: pip install rapidfuzz")


class HistoryProvider:
    def __init__(self, history_panel=None):
        self.history_panel = history_panel
        self.usage_frequency = Counter()  
        self.recency_scores = {}  

    def get_suggestions(self, partial_text: str, max_results: int = 5) -> List[Suggestion]:
        """
        get history based suggestions with smart ranking

        algorithm:
        1. get all history items from history_panel
        2. filter expressions that match partial_text (fuzzy matching)
        3. score based on: frequency + recency + similarity
        4. return top N suggestions

        scoring formulae:
        score = (frequency_score * 0.4) + (recency_score * 0.3) + (similarity_score * 0.3)

        returns:
            list of Suggestion objects sorted by score = highest first
        """
        if not self.history_panel or not partial_text:
            return []

        suggestions = []
        history_expressions = self._get_history_expressions()

        if not history_expressions:
            return []

        for expr in history_expressions:
            similarity_score = self._calculate_similarity_score(partial_text, expr)
            
            if similarity_score < 40:
                continue

            
            frequency_score = self._calculate_frequency_score(expr)
            recency_score = self._calculate_recency_score(expr)
            final_score = (
                similarity_score * 0.3 +
                frequency_score * 0.4 +
                recency_score * 0.3
            )
            suggestion = Suggestion(
                text=expr,
                type=SuggestionType.HISTORY,
                score=final_score,
                description=f"Used {self.usage_frequency.get(expr, 1)} time(s)",
                category="history",
                usage_count=self.usage_frequency.get(expr, 1)
            )

            suggestions.append(suggestion)

        suggestions.sort(key=lambda s: s.score, reverse=True)
        return suggestions[:max_results]

    def _get_history_expressions(self) -> List[str]:
        if not hasattr(self.history_panel, 'calculation_history'):
            return []

        expressions = []
        for item_text in self.history_panel.calculation_history:
            # parse operation: expression = result format
            if '=>' in item_text:
                parts = item_text.split('=>')[0].strip()
                if ':' in parts:
                    expr = parts.split(':', 1)[1].strip()
                else:
                    expr = parts.strip()
            elif '=' in item_text:
                expr = item_text.split('=')[0].strip()
            else:
                expr = item_text.strip()

            # remove optional expression part if present
            if ',' in expr:
                expr = expr.split(',')[0].strip()

            if expr:
                expressions.append(expr)

        return list(set(expressions))  # remove duplicates

    def _calculate_similarity_score(self, partial: str, full: str) -> float:
        partial_lower = partial.lower()
        full_lower = full.lower()

        if full_lower.startswith(partial_lower): # exact prefix match
            return 100.0

        # contains as substring
        if partial_lower in full_lower:
            # score based on how early it appears
            position = full_lower.index(partial_lower)
            position_score = 100 - (position / len(full_lower) * 20)
            return min(95.0, position_score)

        # fuzzy matching (handles typos)
        if HAS_RAPIDFUZZ:
            token_score = fuzz.token_set_ratio(partial_lower, full_lower)
            partial_score = fuzz.partial_ratio(partial_lower, full_lower)
            return max(token_score, partial_score)
        else:
            overlap = sum(1 for c in partial_lower if c in full_lower)
            return (overlap / len(partial_lower)) * 70

    def _calculate_frequency_score(self, expression: str) -> float:
        """
        calculate score based on usage frequency (0-100)

        formulae: score = 100 * (log(count + 1) / log(max_count + 1))
        this gives:
        - 1 use: 0-30 points
        - 5 uses: 60 points
        - 10 uses: 80 points
        - 20+ uses: 100 points
        """
        count = self.usage_frequency.get(expression, 1)

        if not self.usage_frequency:
            return 50.0  # default if no history

        max_count = max(self.usage_frequency.values())

        if max_count == 1:
            return 50.0  # all equal returns middle score

        # logarithmic scaling
        score = 100 * (math.log(count + 1) / math.log(max_count + 1))

        return score

    def _calculate_recency_score(self, expression: str) -> float:
        if expression not in self.recency_scores:
            return 0.0  # never used before

        last_used_timestamp = self.recency_scores[expression]
        current_timestamp = datetime.now().timestamp()

        # calculate hours ago
        seconds_ago = current_timestamp - last_used_timestamp
        hours_ago = seconds_ago / 3600

        # exponential decay (half-life of 24 hours)
        decay_constant = 24.0
        score = 100 * math.exp(-hours_ago / decay_constant)

        return score

    def record_usage(self, expression: str):
        self.usage_frequency[expression] += 1
        self.recency_scores[expression] = datetime.now().timestamp()

    def get_top_expressions(self, n: int = 10) -> List[tuple]:
        return self.usage_frequency.most_common(n)

    def clear_old_entries(self, days: int = 30):
        cutoff_timestamp = datetime.now().timestamp() - (days * 24 * 3600)

        old_expressions = [
            expr for expr, timestamp in self.recency_scores.items()
            if timestamp < cutoff_timestamp
        ]

        for expr in old_expressions:
            del self.recency_scores[expr]
            if expr in self.usage_frequency:
                del self.usage_frequency[expr]
