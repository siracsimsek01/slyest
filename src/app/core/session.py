"""Session management for the application. This file keeps track of all the calculations """

from typing import List, Dict, Any, Optional
from datetime import datetime
import sympy as sp
import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

class HistoryEntry:
    
    def __init__(self, operation: str, input_expr: str, result: sp.Expr, optional_input_expr=None, timestamp: Optional[datetime] = None):
        self.operation = operation  # simplify, differentiate
        self.input_expr = input_expr  # The expression before calculation
        self.optional_input_expr = optional_input_expr
        self.result = result  # The resulting expression
        self.timestamp = timestamp if timestamp else datetime.now()  # When it was done
        
    
    def to_dict(self) -> Dict[str, Any]:
        """Turn this entry into a dictionary so we can save it to a file."""
        return {
            'operation': self.operation,
            'input_expr': self.input_expr,
            'optional_input_expr': self.operation,
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }

    def __str__(self) -> str:
        """Make it look nice when we print it."""
        if self.optional_input_expr:
            return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.operation}: {self.input_expr}| {self.optional_input_expr} → {self.result}"
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.operation}: {self.input_expr} → {self.result}"
    
    
class SessionManager:
    
    def __init__(self, max_history: int = 100):
        self.history: List[HistoryEntry] = [] # empty history list to store
        self.max_history = max_history  # Limit how many entries we keep
        self.session_start = datetime.now() # remembers when the session started
        
    def get_history(self, limit: Optional[int] = None) -> List[HistoryEntry]:
        if limit:
            return self.history[-limit:]  # return the last 'limit' entries
        return self.history.copy()
    
    def get_entry(self, index: int) -> HistoryEntry:
        return self.history[index]
    
    def get_last_result(self) -> Optional[sp.Expr]:
        if self.history:
            return self.history[-1].result
        return None
    
    def clear_history(self):
        
        self.history.clear()
        
    def export_history(self, format, name, calculation_list):
        if format == 'txt':
            return self.export_text(name, calculation_list)
        elif format == 'pdf':
            return self.export_pdf()
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
    def export_text(self, name, calculation_list):
        os.makedirs("HistoryFiles", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.txt"
        filepath = os.path.join("HistoryFiles", filename)
        with open(filepath, "w", encoding="utf-8") as file:
            for index, item in enumerate(calculation_list):
                file.write(str(index + 1) + ". " + item + "\n")
        return filepath
    
    def export_pdf(self, name, calculation_list):
        pdf_file_name = f'{name}.pdf'
        title = 'Calculation History'
        max_width = 500
        font = "Times-Roman"
        font_size = 12

        pdf = canvas.Canvas(pdf_file_name)
        pdf.drawCentredString(300, 770, title)
        pdf.setFillColorRGB(0, 0, 255)
        pdf.line(30, 750, 550, 750)

        text = pdf.beginText(40, 720)
        text.setFont(font, font_size)
        text.setLeading(20)
        text.setFillColor(colors.black)

        for index, line in enumerate(calculation_list):
            numbered_line = f"{index + 1}. {line}"
            wrapped_lines = self.wrap_text(numbered_line, font, font_size, max_width)
            for wrapped_line in wrapped_lines:
                text.textLine(wrapped_line)
            
        pdf.drawText(text)
        pdf.save()
        return pdf_file_name
    
    def wrap_text(self, text, font, font_size, max_width):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = current + (" " if current else "") + word
            if stringWidth(test, font, font_size) <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines