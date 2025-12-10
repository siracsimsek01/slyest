from explanation_enhancer import ExplanationEnhancer
import json
steps = [
    {"title": "Given Expression", "expression": "2x + 3x", "rule": ""},
    {"title": "Simplify", "expression": "2x + 3x → 5x", "rule": "combine_like_terms"},
]
context = {"operation": "simplify", "level": "GCSE", "learning_mode": True}

enh = ExplanationEnhancer(api_type="openai", model="gpt-4o-mini")
out = enh.enhance_all_steps(steps, context)
print(json.dumps(out, indent=2))
