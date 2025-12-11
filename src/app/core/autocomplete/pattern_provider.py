"""
Pattern Provider - Suggests common mathematical patterns
"""
import json
import re
from typing import List, Dict, Optional
from pathlib import Path
from .suggestion import Suggestion, SuggestionType

try:
    from sympy.parsing.sympy_parser import parse_expr
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False


class PatternProvider:

    def __init__(self, patterns_file: str = None):
        if patterns_file is None:
            # default to patterns.json in same directory
            patterns_file = Path(__file__).parent / "patterns.json"

        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                self.patterns = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {patterns_file} not found. Pattern suggestions disabled.")
            self.patterns = {}

        # pre-compile regex patterns for fast matching
        self.compiled_patterns = self._compile_patterns()

    def get_suggestions(self, partial_text: str) -> List[Suggestion]:
        if not partial_text or len(partial_text) < 2:
            return []

        suggestions = []

        # try matching against each pattern category
        for category, pattern_list in self.patterns.items():
            for pattern_def in pattern_list:
                # calculate how well partial matches this pattern
                match_result = self._match_pattern(partial_text, pattern_def)

                if match_result and match_result['score'] > 30:
                    suggestion = Suggestion(
                        text=pattern_def['pattern'],
                        type=SuggestionType.PATTERN,
                        score=match_result['score'],
                        description=pattern_def.get('description', ''),
                        category=category
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _match_pattern(self, partial: str, pattern_def: Dict) -> Optional[Dict]:
        pattern_template = pattern_def['pattern']
        commonness = pattern_def.get('commonness', 50)

        if self._simple_prefix_match(partial, pattern_template):
            score = 70 + (commonness * 0.3)  # Boost common patterns
            return {'score': score, 'completion': pattern_template}

        #  Structural matching uses SymPy)
        if HAS_SYMPY:
            structural_score = self._structural_match(partial, pattern_template)
            if structural_score > 0:
                score = structural_score + (commonness * 0.2)
                return {'score': min(100, score), 'completion': pattern_template}

        # Token-based matching (fallback)
        token_score = self._token_match(partial, pattern_template)
        if token_score > 30:
            score = token_score + (commonness * 0.2)
            return {'score': score, 'completion': pattern_template}

        return None

    def _simple_prefix_match(self, partial: str, pattern: str) -> bool:
        # normalize: remove spaces, convert ** to ^, etc.
        partial_norm = partial.replace(' ', '').replace('^', '**')
        pattern_norm = pattern.replace(' ', '').replace('{', '').replace('}', '')

        # remove placeholder brackets for comparison
        pattern_norm = re.sub(r'\{[a-z]\}', '?', pattern_norm)

        return pattern_norm.startswith(partial_norm)

    def _structural_match(self, partial: str, pattern: str) -> float:
        """
        match based on mathematical structure 

        Uses SymPy to parse expressions and compare structure
        Example:
        partial: "x**2 + 5"
        pattern: "x**2 + {b}*x + {c}"
        match: Yes (both are polynomials starting with x**2)
        """
        try:
            partial_expr = parse_expr(partial.replace('^', '**'))

            pattern_for_parse = re.sub(r'\{([a-z])\}', r'\1', pattern)
            pattern_expr = parse_expr(pattern_for_parse.replace('^', '**'))

    
            partial_terms = str(partial_expr).split('+')
            pattern_terms = str(pattern_expr).split('+')

            # Check if partial's terms are subset of pattern's terms
            matching_terms = 0
            for p_term in partial_terms:
                p_term = p_term.strip()
                for pat_term in pattern_terms:
                    pat_term = pat_term.strip()
                    # Check if structure matches (ignore coefficient values)
                    if self._terms_structurally_similar(p_term, pat_term):
                        matching_terms += 1
                        break

            if matching_terms > 0:
                score = (matching_terms / len(partial_terms)) * 80
                return score

        except Exception:
            pass

        return 0.0

    def _terms_structurally_similar(self, term1: str, term2: str) -> bool:
        """
        Check if two terms have similar structure

        Example: "5*x" is similar to "b*x"
        """
        # remove numeric coefficients and compare
        term1_stripped = re.sub(r'\d+', 'N', term1)
        term2_stripped = re.sub(r'[a-z](?![a-z])', 'N', term2)  # single letters become N

        return term1_stripped == term2_stripped

    def _token_match(self, partial: str, pattern: str) -> float:
        partial_tokens = self._extract_tokens(partial)
        pattern_tokens = self._extract_tokens(pattern)

        if not partial_tokens:
            return 0.0

        # calculate overlap
        matches = sum(1 for token in partial_tokens if token in pattern_tokens)
        score = (matches / len(partial_tokens)) * 60

        return score

    def _extract_tokens(self, expr: str) -> List[str]:
        # remove numbers
        expr = re.sub(r'\d+', '', expr)

        # find operators
        operators = re.findall(r'[\+\-\*/\^]|\*\*', expr)

        # find functions (sin, cos, tan, sqrt, etc.)
        functions = re.findall(r'(sin|cos|tan|sqrt|log|ln|exp)', expr.lower())


        variables = re.findall(r'[a-z]', expr.lower())

        return operators + functions + variables

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """
        Convert pattern templates to regex for fast matching
        """
        compiled = {}

        for category, pattern_list in self.patterns.items():
            for pattern_def in pattern_list:
                pattern_str = pattern_def['pattern']
                name = pattern_def.get('name', pattern_str)

                try:
                    # Escape special regex characters
                    regex_pattern = re.escape(pattern_str)

                    # Replace escaped placeholders with regex groups
                    regex_pattern = re.sub(r'\\{[a-z]\\}', r'(\\w+|\\d+)', regex_pattern)

                    # Allow flexible whitespace
                    regex_pattern = regex_pattern.replace(r'\ ', r'\s*')

                    compiled[name] = re.compile(regex_pattern)

                except Exception as e:
                    print(f"Warning: Could not compile pattern '{name}': {e}")

        return compiled

    def _calculate_pattern_score(self, partial: str, pattern: Dict) -> float:
    
        pattern_str = pattern['pattern']
        commonness = pattern.get('commonness', 50)

        if pattern_str.startswith(partial):
            coverage_score = (len(partial) / len(pattern_str)) * 50
        else:
            coverage_score = 0


        commonness_score = commonness * 0.3
        structural_score = self._structural_match(partial, pattern_str)

        # Combined score
        total_score = coverage_score + commonness_score + structural_score

        return min(100, total_score)

    def get_patterns_by_category(self, category: str) -> List[Dict]:
        return self.patterns.get(category, [])

    def get_all_categories(self) -> List[str]:
        return list(self.patterns.keys())
