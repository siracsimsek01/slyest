import re
import json
from typing import List, Optional
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from .suggestion import Suggestion, SuggestionType
from .function_provider import FunctionProvider
from .history_provider import HistoryProvider
from .pattern_provider import PatternProvider

class AutocompleteManager(QObject):


    suggestions_ready = pyqtSignal(list)

    def __init__(self, engine, history_panel):
        super().__init__()

        # initialize providers
        self.function_provider = FunctionProvider()
        self.history_provider = HistoryProvider(history_panel)
        self.pattern_provider = PatternProvider()

        self.engine = engine
        self.current_input = ""
        self.min_chars_trigger = 2  
        # debouncing for performance
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self._do_search)
        self.debounce_delay = 150  # ms

        self.pending_text = ""

    def on_text_changed(self, text: str):
        self.pending_text = text

        # if too short hide immediately
        if len(text) < self.min_chars_trigger:
            self.suggestions_ready.emit([])
            return

        # restart debounce timer
        self.debounce_timer.stop()
        self.debounce_timer.start(self.debounce_delay)

    def _do_search(self):
        text = self.pending_text
        self.current_input = text

        # extract token at cursor (HARD)
        current_token = self._get_current_token(text)

        # query all providers
        func_suggestions = self.function_provider.get_suggestions(current_token)
        hist_suggestions = self.history_provider.get_suggestions(current_token)
        pattern_suggestions = self.pattern_provider.get_suggestions(text)

        final_suggestions = self._merge_and_rank([
            func_suggestions,
            hist_suggestions,
            pattern_suggestions
        ])

        self.suggestions_ready.emit(final_suggestions[:10])

    def _get_current_token(self, text: str, cursor_pos: Optional[int] = None) -> str:
        if not text:
            return ""

        # if cursor position not provided, assume end of string
        if cursor_pos is None:
            cursor_pos = len(text)

        # define delimiters: operators, parentheses, spaces
        # keep ** together as single operator
        delimiters = r'[\+\-\*/\(\)\s,=]'

        # split on delimiters but keep position info
        tokens = []
        current_token = ""

        for i, char in enumerate(text):
            if re.match(delimiters, char):
                if current_token:
                    tokens.append((current_token, i - len(current_token), i))
                    current_token = ""
            else:
                current_token += char

        if current_token:
            tokens.append((current_token, len(text) - len(current_token), len(text)))

        # find token at cursor position
        for token, start, end in tokens:
            if start <= cursor_pos <= end:
                return token

        # fallback: return last token
        if tokens:
            return tokens[-1][0]

        return text.strip()

    def _merge_and_rank(self, suggestion_lists: List[List[Suggestion]]) -> List[Suggestion]:
        # flatten all suggestions into one list
        all_suggestions = []
        for suggestion_list in suggestion_lists:
            all_suggestions.extend(suggestion_list)

        if not all_suggestions:
            return []

        # remove duplicates keep highest score
        seen = {}
        for suggestion in all_suggestions:
            if suggestion.text not in seen or suggestion.score > seen[suggestion.text].score:
                seen[suggestion.text] = suggestion

        unique_suggestions = list(seen.values())

        # apply advanced ranking adjustments
        for suggestion in unique_suggestions:

            #  exact prefix match boost
            if self.current_input and suggestion.text.lower().startswith(self.current_input.lower()):
                suggestion.score += 20

            # variable exists in session
            if suggestion.type == SuggestionType.VARIABLE:
                variables = self.engine.list_variables()
                if suggestion.text in variables:
                    suggestion.score += 10

            # recently used (check usage_count)
            if suggestion.usage_count > 0:
                # logarithmic boost for frequency
                import math
                boost = min(15, 5 * math.log(suggestion.usage_count + 1))
                suggestion.score += boost

            # length penalty (prefer shorter suggestions)
            word_count = len(suggestion.text.split())
            if word_count > 3:
                penalty = (word_count - 3) * 2
                suggestion.score -= penalty

            # type priority
            type_bonus = {
                SuggestionType.FUNCTION: 5,
                SuggestionType.PATTERN: 3,
                SuggestionType.CONSTANT: 8,
                SuggestionType.HISTORY: 2,
                SuggestionType.VARIABLE: 1
            }
            suggestion.score += type_bonus.get(suggestion.type, 0)

        # sort by score (descending)
        ranked = sorted(unique_suggestions, key=lambda s: s.score, reverse=True)

        return ranked

    def on_suggestion_accepted(self, suggestion: Suggestion):
        # record in history provider
        if suggestion.type in (SuggestionType.HISTORY, SuggestionType.PATTERN):
            self.history_provider.record_usage(suggestion.text)

        # increment usage count
        suggestion.usage_count += 1

    def save_learning_data(self, filepath: str = "autocomplete_data.json"):
        """
        persist learned usage patterns to disk

        saves:
        - frequency data
        - recency scores
        - usage counts
        """
        try:
            data = {
                'usage_frequency': dict(self.history_provider.usage_frequency),
                'recency_scores': dict(self.history_provider.recency_scores)
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"saved learning data to {filepath}")
        except Exception as e:
            print(f"error saving learning data: {e}")

    def load_learning_data(self, filepath: str = "autocomplete_data.json"):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            # restore to history provider
            from collections import Counter
            self.history_provider.usage_frequency = Counter(data.get('usage_frequency', {}))
            self.history_provider.recency_scores = data.get('recency_scores', {})

            print(f"loaded learning data from {filepath}")
        except FileNotFoundError:
            print(f"no learning data found at {filepath}, starting fresh")
        except Exception as e:
            print(f"error loading learning data: {e}")

    def get_variable_suggestions(self) -> List[Suggestion]:
        """
        get suggestions for all defined variables
        useful for variable chip display
        """
        variables = self.engine.list_variables()
        suggestions = []

        for var_name, var_value in variables.items():
            suggestions.append(Suggestion(
                text=var_name,
                type=SuggestionType.VARIABLE,
                score=80,
                description=f"{var_name} = {var_value}",
                category='variable'
            ))

        return suggestions

    def clear_cache(self):
        self.current_input = ""
        self.pending_text = ""
