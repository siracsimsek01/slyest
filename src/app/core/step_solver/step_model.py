
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Step:
    """Represents a single step in solving an equation."""
    title: str             
    expression: str        
    explanation: str        
    rule: str              
    is_final: bool = False 
    
    # optional for showing work
    work_shown: Optional[str] = None  

@dataclass
class Solution:
    """complete solution with all steps"""
    equation: str          
    steps: List[Step]       
    final_answer: str    
    success: bool          
    error_message: Optional[str] = None