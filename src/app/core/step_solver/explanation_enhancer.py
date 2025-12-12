import os
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from .explanation_text_library import ExplanationTexts

try:
    # modern OpenAI SDK
    from openai import OpenAI
    _openai_available = True
except Exception:
    _openai_available = False


@dataclass
class ExplainOutput:
    explanation: str
    hint: Optional[str] = None
    common_mistake: Optional[str] = None
    follow_up: Optional[str] = None

    def to_dict(self) -> Dict:
        # drop None fields
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


class ExplanationEnhancer:
    def __init__(self, api_type: str = "local", api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_type = api_type.lower()
        self.api_key = api_key or os.getenv(f"{api_type.upper()}_API_KEY") if api_type else None
        self.use_api = (self.api_type in {"openai"} and (self.api_key or os.getenv("OPENAI_API_KEY")))
        self.model = model
        self._client = OpenAI(api_key=(self.api_key or os.getenv("OPENAI_API_KEY"))) if (self.use_api and _openai_available) else None
        self._cache: Dict[Tuple, Dict] = {}
        self.library = ExplanationTexts()

    # ---------- Public ----------
    def enhance_all_steps(self, steps: List[Dict], context: Dict) -> List[Dict]:
        out = []
        for step in steps:
            out.append(self.enhance_explanation(step, context))
        return out

    def enhance_explanation(self, step: Dict, context: Dict) -> Dict:
        if not step:
            return step
        enriched = self._enhance_locally(step, context)
        needs_help = context.get("learning_mode", True) and context.get("level", "auto") != "none"
        if self.use_api and needs_help:
            try:
                enriched = self._enhance_with_openai(enriched, context)
            except Exception as e:
                # never fail UX because of API
                enriched.setdefault("meta", {})["llm_error"] = str(e)

        return enriched

    # ---------- Local rules ----------
    def _enhance_locally(self, step: Dict, context: Dict) -> Dict:
        title = (step.get("title") or "").lower()
        expr = step.get("expression", "")
        rule = step.get("rule", "")

        local = ExplainOutput(
            explanation=self._template_explanation(title, expr, rule, context),
            hint=self._generate_hint(title, expr, rule, context),
            common_mistake=self._generate_common_mistake(title, expr, rule),
            follow_up=self._generate_follow_up(title, context)
        )

        step["explanation_pack"] = local.to_dict()
        # for backward compatibility with your UI
        step["explanation"] = local.explanation
        return step

    def _template_explanation(self, title: str, expr: str, rule: str, context: Dict) -> str:
        operation = (context.get("operation") or "calculate").lower()

        if "given expression" in title or "given equation" in title or "given function" in title:
            if operation in ["calculate", "solve", "simplify", "expand", "factor", "differentiate", "integrate", "substitute", "solve 2 equations", "solve quadratic"]:
                return self.library.get_explanation_with_expression(operation, expr)
            return self.library.get_explanation_with_expression("operation: default", expr)

        if "identify" in title:
            if "+" in expr and "-" not in expr.replace("- ", ""):
                n = expr.count("+") + 1
                return self.library.get_explanation_with_n("identify: add", n)
            if "*" in expr or "×" in expr:
                return self.library.get_explanation("identify: multiply")
            if "/" in expr or "÷" in expr:
                return self.library.get_explanation("identify: divide")
            if "-" in expr:
                return self.library.get_explanation("identify: subtract")
            return self.library.get_explanation("identify: default")

        if "calculate result" in title:
           return self.library.get_explanation("calculate result")

        if "simplify" in title:
            if "combine" in rule.lower() or "like terms" in rule.lower():
                return self.library.get_explanation("simplify: combine-if")
            return self.library.get_explanation("simplify: combine-else")

        if "foil" in title.lower() or "foil" in rule.lower():
            if "identify" in title or "binomial" in title:
                return self.library.get_explanation("foil: identify")
            if "apply" in title:
                return self.library.get_explanation("foil: apply")
        
        if "combine all terms" in title:
            return self.library.get_explanation("combine all terms")
        if "expand" in title:
            return self.library.get_explanation("expand: title")
        if "factor" in title:
            return self.library.get_explanation("factor: title")
        if "divide" in title and "both sides" in title:
            return self.library.get_explanation("divide: title")
        if "subtract" in title and "both sides" in title:
            return self.library.get_explanation("subtract: title")
        if "solution" in title or "final" in title:
            return self.library.get_explanation("solution: title")
        return self.library.get_explanation("default")

    def _generate_hint(self, title: str, expr: str, rule: str, context: Dict) -> Optional[str]:
        operation = (context.get("operation") or "").lower()

        if "given" in title and operation in ["solve", "simplify", "expand", "factor", "substitute", "differentiate", "integrate", "solve quadratic", "solve 2 equations"]:
            return self.library.get_hints(operation)
        if "simplify" in title or "combine" in rule.lower():
            return self.library.get_hints("simplify: title")
        if "identify" in title:
            return self.library.get_hints("identify: title")
        if "divide" in title and "both sides" in title:
           return self.library.get_hints("divide: title")
        if "subtract" in title and "both sides" in title:
            return self.library.get_hints("subtract: title")
        if "solution" in title:
            return self.library.get_hints("solution: title")
        return None

    def _generate_common_mistake(self, title: str, expr: str, rule: str) -> Optional[str]:   
        if "simplify" in title or "combine" in rule.lower():
            return self.library.get_warnings("simplify")
        if "expand" in title:
            return self.library.get_warnings("expand")
        if "divide" in title and "both sides" in title:
            return self.library.get_warnings("divide")
        if "subtract" in title and "both sides" in title:
            return self.library.get_warnings("subtract")
        if "factor" in title:
            return self.library.get_warnings("factor")
        if "solve" in title or "solution" in title:
            return self.library.get_warnings("solve")
        if "calculate" in title and ("+" in expr or "-" in expr or "*" in expr or "/" in expr):
            return self.library.get_warnings("calculate")
        if "substitute" in title:
            return self.library.get_warnings("substitute")
        if "differentiate" in title:
            return self.library.get_warnings("differentiate")
        if "integrate" in title:
            return self.library.get_warnings("integrate")
        return None

    def _generate_follow_up(self, title: str, context: Dict) -> Optional[str]:
        operation = (context.get("operation") or "").lower()
        if "solution" in title or "final" in title or "result" in title:
            return self.library.get_follow_ups(operation)
        if "given" in title and operation == "solve":
            return self.library.get_follow_ups("solve: given")
        if "simplify" in title:
            return self.library.get_follow_ups("simplify: title")
        return None

    # ---------- OpenAI ----------
    def _enhance_with_openai(self, step: Dict, context: Dict) -> Dict:
        if not self._client:
            return step

        # cache key
        key = (
            self.model,
            step.get("title"),
            step.get("expression"),
            step.get("rule"),
            context.get("operation"),
            context.get("level"),
        )
        if key in self._cache:
            step["explanation_pack"] = self._cache[key]
            step["explanation"] = step["explanation_pack"]["explanation"]
            return step

        # enforce short, structured, safe outputs
        response = self._client.responses.create(
            model=self.model,                   # pick a small fast model for explanations
            temperature=0,
            seed=42,                            # deterministic pedagogy for same input
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise math tutor. "
                        "Explain each step in 1–2 sentences, no hidden reasoning. "
                        "Prefer plain language, avoid heavy notation unless needed."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps({
                        "step": {
                            "title": step.get("title"),
                            "expression": step.get("expression"),
                            "rule": step.get("rule")
                        },
                        "context": {
                            "operation": context.get("operation"),
                            "level": context.get("level", "GCSE"),   # GCSE/A-level/Uni
                            "style": context.get("style", "student-friendly")
                        }
                    })
                }
            ],
            # ask for structured JSON back
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "ExplainOutput",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "explanation": {"type": "string"},
                            "hint": {"type": "string"},
                            "common_mistake": {"type": "string"},
                            "follow_up": {"type": "string"}
                        },
                        "required": ["explanation"]
                    }
                }
            },
            max_output_tokens=160,
        )

        # parse
        content = response.output[0].content[0].text  # structured JSON string
        data = json.loads(content)

        # merge
        step["explanation_pack"] = data
        step["explanation"] = data["explanation"]

        # cache
        self._cache[key] = data
        return step
