from typing import List, Dict
from collections import Counter
from .suggestion import Siggestion, Suggestion, SuggestionType

class HistoryProvider:
    # Provides suggestions from calculation history with frequency tracking
    def __init__(self, history_panel=None):
        self.history_panel = history_panel
        self.usage_frequency: Counter() # tracks how often each expression is used
        self.recency_scores = {}  # tracks recency of each expression
        
        def get_suggestions(self, partial_text: str, max_results: int = 5) -> List[Suggestion]: 
            """
        get history based suggestions with smart ranking
        
        algorithm:
        1. get all history items from history_panel
        2. filter expressions that contain partial_text (fuzzy match)
        3. score based on: frequency + recency + similarity
        4. return top N suggestions
        
        scoring formula:
        score = (frequency_score * 0.4) + (recency_score * 0.3) + (similarity_score * 0.3)
        """
        # TODO: Implement smart scoring algorithm
        pass
    
        def record_usage(self, expression: str):
            """record that an expression was used"""
        self.usage_frequency[expression] += 1
        self.recency_scores[expression] = datetime.now().timestamp()
        
        def _calculate_frequency_score(self, expression: str) -> float:
            """calculate score based on usage frequency (0-100))"""
            # TODO: normalize frequency counts to 0-100 scale
            pass
        
        def _calculate_recency_score(self, expression: str) -> float:
             """Calculate score based on how recently used (0-100)"""
        # TODO: Use exponential decay: newer = higher score
        pass