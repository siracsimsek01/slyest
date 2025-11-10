"""Session management for the application. This file keeps track of all the calculations """

from typing import List, Dict, Any, Optional
from datetime import datetime
import sympy as sp

class HistoryEntry:
    
    def __init__(self, operation: str, input_expr: str, result: sp.Expr, timestamp: Optional[datetime] = None):
        self.operation = operation  # simplify, differentiate
        self.input_expr = input_expr  # The expression before calculation
        self.result = result  # The resulting expression
        self.timestamp = timestamp if timestamp else datetime.now()  # When it was done
        
    
    def to_dict(self) -> Dict[str, Any]:
        """Turn this entry into a dictionary so we can save it to a file."""
        return {
            'operation': self.operation,
            'input_expr': self.input_expr,
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }

    def __str__(self) -> str:
        """Make it look nice when we print it."""
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.operation}: {self.input_expr} → {self.result}"
    
    
class SessionManager:
    
    def __init__(self, max_history: int = 100):
        #   Start a new session and get ready to track history with 100 entries
        self.history: List[HistoryEntry] = [] # empty history list to store
        self.max_history = max_history  # Limit how many entries we keep
        self.session_start = datetime.now() # remembers when the session started
        
    def get_history(self, limit: Optional[int] = None) -> List[HistoryEntry]:
        """Get the calculation history. Can limit how many entries to return."""
        if limit:
            return self.history[-limit:]  # return the last 'limit' entries
        return self.history.copy()
    
    def get_entry(self, index: int) -> HistoryEntry:
        """Get a specific history entry by its index."""
        return self.history[index]
    
    def get_last_result(self) -> Optional[sp.Expr]:
        """Get the result of the last calculation, if any."""
        if self.history:
            return self.history[-1].result
        return None
    
    def clear_history(self):
        """Clear all history entries."""
        self.history.clear()
        
    def export_history(self, format: str = 'text') -> str:
        
        if format == 'text':
            return self._export_text()
        elif format == 'latex':
            return self._export_latex()
        elif format == 'json':
            return self._export_json()
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
    