
import sys
sys.path.insert(0, '/Users/simsek/dev/Group_Project')

from src.app.core.autocomplete.function_provider import FunctionProvider
from src.app.core.autocomplete.suggestion import Suggestion, SuggestionType

def test_function_provider():

    print("=" * 80)
    print("AUTOCOMPLETE TEST SUITE")
    print("=" * 80)

    provider = FunctionProvider()

 
    print("\n📝 Test 1: Function Suggestions")
    print("-" * 80)
    print("Query: 's'")
    suggestions = provider.get_suggestions("s", max_results=10)
    print(f"Found {len(suggestions)} suggestions:")
    for i, sug in enumerate(suggestions, 1):
        print(f"  {i}. {sug.icon} {sug.display_label:30s} [{sug.type_name:10s}] score: {sug.score:.1f}")

    print("\n📝 Test 2: More Specific Query")
    print("-" * 80)
    print("Query: 'sin'")
    suggestions = provider.get_suggestions("sin", max_results=10)
    print(f"Found {len(suggestions)} suggestions:")
    for i, sug in enumerate(suggestions, 1):
        print(f"  {i}. {sug.icon} {sug.display_label:30s} [{sug.type_name:10s}] score: {sug.score:.1f}")

    print("\n📝 Test 3: Constants")
    print("-" * 80)
    print("Query: 'p'")
    suggestions = provider.get_suggestions("p", max_results=10)
    print(f"Found {len(suggestions)} suggestions:")
    for i, sug in enumerate(suggestions, 1):
        print(f"  {i}. {sug.icon} {sug.display_label:30s} [{sug.type_name:10s}] score: {sug.score:.1f}")

    print("\n📝 Test 4: Pattern Suggestions")
    print("-" * 80)
    print("Query: 'quad'")
    suggestions = provider.get_suggestions("quad", max_results=10)
    print(f"Found {len(suggestions)} suggestions:")
    for i, sug in enumerate(suggestions, 1):
        label = sug.display_label[:50] + "..." if len(sug.display_label) > 50 else sug.display_label
        print(f"  {i}. {sug.icon} {label:50s} [{sug.type_name:10s}] score: {sug.score:.1f}")

    print("\n📝 Test 5: History")
    print("-" * 80)
    provider.record_expression("sin(x) + cos(x)")
    provider.record_expression("sin(x)**2")
    provider.record_expression("sqrt(x)")
    print("Recorded expressions: sin(x) + cos(x), sin(x)**2, sqrt(x)")
    print("\nQuery: 'sin'")
    suggestions = provider.get_suggestions("sin", max_results=10)
    print(f"Found {len(suggestions)} suggestions:")
    for i, sug in enumerate(suggestions, 1):
        print(f"  {i}. {sug.icon} {sug.display_label:30s} [{sug.type_name:10s}] score: {sug.score:.1f}")

    print("\n📝 Test 6: Empty Query")
    print("-" * 80)
    print("Query: ''")
    suggestions = provider.get_suggestions("", max_results=10)
    print(f"Found {len(suggestions)} suggestions (should be 0)")
    
    print("\n📝 Test 7: Suggestion Properties")
    print("-" * 80)
    test_sug = Suggestion(
        text="sin",
        type=SuggestionType.FUNCTION,
        score=95.0,
        description="sine function",
        category="trigonometry"
    )
    print(f"Text: {test_sug.text}")
    print(f"Type: {test_sug.type_name}")
    print(f"Score: {test_sug.score}")
    print(f"Icon: {test_sug.icon}")
    print(f"Badge Color: {test_sug.type_badge_color}")
    print(f"Display Label: {test_sug.display_label}")
    print(f"Description: {test_sug.description}")
    print(f"Repr: {test_sug}")

    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 80)
    print("\n💡 To test in GUI:")
    print("   1. Run: python -m src.app.main")
    print("   2. Type 's' in the expression input")
    print("   3. See autocomplete suggestions appear!")
    print("   4. Use ↑/↓ to navigate, Enter to select, Esc to close")
    print("   5. Try typing: sin, cos, pi, quad, x**2")
    print("\n")

if __name__ == "__main__":
    test_function_provider()
