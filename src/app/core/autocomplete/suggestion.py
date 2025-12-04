from dataclasses import dataclass
from typing import Optional
from enum import Enum

class SuggestionType(Enum):
    FUNCTION="function"
    VARIABLE="variable"
    CONSTANT="constant"
    HISTORY="history"
    PATTERN="pattern"
    
@dataclass
class Suggestion:
    """Represents a single autocomplete suggestion."""
    ## TODO: Add fields as necessary
  
    
    def __repr__(self):
        ## TODO: Implement representation
        pass