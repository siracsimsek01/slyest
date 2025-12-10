from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class SuggestionType(Enum):
    FUNCTION = "function"
    VARIABLE = "variable"
    CONSTANT = "constant"
    HISTORY = "history"
    PATTERN = "pattern"

@dataclass
class Suggestion:
    text: str  
    type: SuggestionType 
    score: float = 0.0  
    label: Optional[str] = None 
    description: Optional[str] = None 
    category: Optional[str] = None  
    usage_count: int = 0 
    icon: Optional[str] = None  

    def __post_init__(self):
        if self.label is None:
            self.label = self.text

        if self.icon is None:
            icon_map = {
                SuggestionType.FUNCTION: "🔵",
                SuggestionType.VARIABLE: "🟢",
                SuggestionType.CONSTANT: "🟣",
                SuggestionType.HISTORY: "🕐",
                SuggestionType.PATTERN: "📐"
            }
            self.icon = icon_map.get(self.type, "•")

    def __repr__(self):
        return f"Suggestion(text={self.text!r}, type={self.type.value}, score={self.score:.1f})"

    @property
    def display_label(self) -> str:
        return self.label or self.text

    @property
    def type_name(self) -> str:
        return self.type.value.capitalize()

    @property
    def type_badge_color(self) -> str:
        color_map = {
            SuggestionType.FUNCTION: "#007AFF",  # blue
            SuggestionType.VARIABLE: "#34C759",  # green
            SuggestionType.CONSTANT: "#AF52DE",  # purple
            SuggestionType.HISTORY: "#FF9F0A",   # orange
            SuggestionType.PATTERN: "#FF453A"    # red
        }
        return color_map.get(self.type, "#8E8E93")