import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from function_provider import FunctionProvider, PatternStore, Pattern


class TestPatternStore:
    def test_loads_patterns_from_file(self):
        mock_path = MagicMock()
        mock_path.read_text.return_value = '''
        {"test": [{"name": "test", "pattern": "x+1", "description": "test", "category": "test", "commonness": 50}]}
        '''
        store = PatternStore(mock_path)
        assert len(store.patterns_by_category) == 1
        assert len(store.patterns_by_category["test"]) == 1

    def test_find_matching_patterns_empty_text_returns_empty(self):
        store = PatternStore(Path("nonexistent"))
        assert store.find_matching_patterns("") == []

    def test_find_matching_patterns_returns_exact_matches(self):
        store = self._create_test_store()
        matches = store.find_matching_patterns("quad")
        assert len(matches) == 1
        assert matches[0].name == "quadratic"

    def test_similarity_score_prefix_match(self):
        store = self._create_test_store()
        pattern = store.patterns_by_category["algebraic"][0]
        assert store._similarity_score("quad", pattern) == 1.0

    def test_similarity_score_substring_match(self):
        store = self._create_test_store()
        pattern = store.patterns_by_category["algebraic"][0]
        assert store._similarity_score("atic", pattern) == 0.8

    def _create_test_store(self):
        return PatternStore(Path("test_patterns.json"))


class TestFunctionProvider:
    @pytest.fixture
    def provider(self):
        path = MagicMock()
        path.read_text.return_value = '{"test": []}'
        return FunctionProvider(path)

    def test_get_suggestions_empty_text_returns_empty(self, provider):
        assert provider.get_suggestions("") == []

    def test_record_expression_updates_history_and_usage(self, provider):
        provider.record_expression("sin(x)")
        assert "sin(x)" in provider.history
        assert "sin(x)" in provider.usage
        assert provider.usage["sin(x)"]["count"] == 1

    def test_build_history_suggestions_no_history_returns_empty(self, provider):
        assert provider._build_history_suggestions("test") == []

    @patch.object(FunctionProvider, 'history', ["sin(x)", "cos(x)"])
    def test_build_history_suggestions_filters_by_similarity(self, provider):
        provider.usage["sin(x)"] = {"count": 1, "last_used": time.time()}
        suggestions = provider._build_history_suggestions("si")
        assert len(suggestions) == 1
        assert suggestions[0].label == "sin(x)"

    def test_build_function_suggestions_matches_functions(self, provider):
        suggestions = provider._build_function_suggestions("sin")
        assert len(suggestions) > 0
        assert any(s.label.startswith("sin(x)") for s in suggestions)

    def test_build_constant_suggestions_matches_constants(self, provider):
        suggestions = provider._build_constant_suggestions("pi")
        assert len(suggestions) > 0
        assert any("pi" in s.label for s in suggestions)

    @patch.object(PatternStore, 'find_matching_patterns', return_value=[Pattern("test", "x+1", "test", "test", 50)])
    def test_build_pattern_suggestions_from_store(self, mock_find, provider):
        suggestions = provider._build_pattern_suggestions("test")
        assert len(suggestions) == 1
        assert suggestions[0].value == "x+1"

    def test_history_score_calculates_correctly(self, provider):
        provider.usage["test"] = {"count": 25, "last_used": time.time()}
        score = provider._history_score("test", 0.8)
        assert 0 < score < 200

    def test_frequency_score_normalizes_correctly(self, provider):
        provider.usage["test"] = {"count": 25, "last_used": 0}
        assert provider._frequency_score("test") == 50.0
        provider.usage["test"]["count"] = 100
        assert provider._frequency_score("test") == 100.0

    def test_recency_score_fresh_is_high(self, provider):
        now = time.time()
        provider.usage["test"] = {"count": 0, "last_used": now}
        with patch('time.time', return_value=now):
            assert provider._recency_score("test") == 100.0

    def test_similarity_score_prefix_match(self, provider):
        assert provider._similarity_score("sin", "sin(x)") == 1.0
        assert provider._similarity_score("si", "sin(x)") == 0.6

    def test_get_suggestions_returns_top_n(self, provider):
        provider.history = ["a", "b", "c", "d", "e"]
        for i, expr in enumerate(provider.history):
            provider.usage[expr] = {"count": i+1, "last_used": time.time()}
       
        suggestions = provider.get_suggestions("a", max_results=2)
        assert len(suggestions) == 2

    def test_record_expression_ignores_empty(self, provider):
        initial_len = len(provider.history)
        provider.record_expression("")
        assert len(provider.history) == initial_len

    def test_build_functions_returns_expected_count(self, provider):
        functions = provider._build_functions()
        assert len(functions) > 30

    def test_build_constants_returns_expected(self, provider):
        constants = provider._build_constants()
        assert "pi" in constants
        assert len(constants) == 5


class TestScoringFunctions:
    @pytest.fixture
    def provider(self):
        return FunctionProvider(MagicMock())

    def test_reference_score_with_base_values(self, provider):
        score = provider._reference_score(0.8, 20.0, 20.0)
        assert 0 < score < 100

    def test_pattern_score_combines_commonness_and_similarity(self, provider):
        score = provider._pattern_score(0.9, 80)
        assert score > 80
        assert score < 100


class TestIntegration:
    def test_full_suggestion_pipeline(self):
        path = MagicMock()
        path.read_text.return_value = '{"test": []}'
        provider = FunctionProvider(path)
       
        provider.record_expression("sin(x)")
        suggestions = provider.get_suggestions("sin")
       
        assert len(suggestions) > 0
        assert any("sin" in s.label for s in suggestions)