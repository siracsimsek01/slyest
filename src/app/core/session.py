from typing import List, Dict, Any, Optional
from datetime import datetime
import sympy as sp
import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from .math_formatter import MathFormatter

class HistoryEntry:
    def __init__(self, operation: str, input_expr: str, result: sp.Expr, optional_input_expr=None, timestamp: Optional[datetime] = None, variables: Optional[Dict[str, str]] = None):
        self.operation = operation
        self.input_expr = input_expr
        self.optional_input_expr = optional_input_expr
        self.result = result
        self.timestamp = timestamp if timestamp else datetime.now()
        self.variables = variables if variables else {} 
        
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'operation': self.operation,
            'input_expr': self.input_expr,
            'optional_input_expr': self.optional_input_expr, 
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat(),
            'variables': self.variables
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["operation"],
            data["input_expr"],
            data["result"],
            data.get("optional_input_expr"),
            data.get("variables") # Load from JSON
        )

    def __str__(self) -> str:
        # Base string
        base = f"[{self.timestamp.strftime('%H:%M:%S')}] {self.operation}: {self.input_expr}"
        
        if self.optional_input_expr:
            base += f" | {self.optional_input_expr}"
            
        base += f" → {self.result}"
        # Example output: ... -> 25 [ a = 5, b = 10 ]
        if self.variables:
            vars_str = ", ".join([f"{k} = {v}" for k, v in self.variables.items()])
            base += f" [ {vars_str} ]"
            
        return MathFormatter.to_display(base)
class SessionManager:
    def __init__(self, max_history: int = 100):
        self.history: List[HistoryEntry] = []
        self.max_history = max_history
        self.session_start = datetime.now()
        
    def get_history(self, limit: Optional[int] = None) -> List[HistoryEntry]:
        if limit:
            return self.history[-limit:]
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
            return self.export_pdf(name, calculation_list)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def export_text(self, name, calculation_list):
        filepath = self.create_text_file(name)
        self.write_text_file(filepath, calculation_list)
        return filepath
    
    def create_text_file(self, name):
        os.makedirs("HistoryFiles", exist_ok = True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.txt"
        return os.path.join("HistoryFiles", filename)
    
    def write_text_file(self, filepath, calculation_list):
        with open(filepath, "w", encoding = "utf-8") as file:
            for index, item in enumerate(calculation_list):
                file.write(str(index + 1) + ". " + str(item) + "\n")
    
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
            numbered_line = f"{index + 1}. {str(line)}"
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