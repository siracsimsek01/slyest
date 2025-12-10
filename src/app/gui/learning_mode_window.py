from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from ..core.step_solver.operation_router import OperationRouter
from ..core.math_formatter import MathFormatter

class LearningModeWindow(QDialog):
    def __init__(self, operation, input_expression, result, optional_input, parent=None):
        super().__init__(parent)
        self.apply_stylesheet()
        self.setWindowTitle("Learning Mode")
        self.setGeometry(400, 300, 800, 600)
        self.operation = operation
        self.input_expression = input_expression
        self.result = result
        self.optional_input = optional_input
        self.router = OperationRouter()
        self.steps_data = self.generate_steps()
        self.initialise_ui()
        
    def apply_stylesheet(self):
        self.setStyleSheet(f"""
                QDialog {{
                    background-color: #1C1C1E;
                    color: white;
                }}

                QLabel#learning {{
                    background-color: #2C2C2E;
                    color: #FFFFFF;
                    border-radius: 12px;
                    padding: 20px;
                    font-size: 13pt;
                }}
                QLabel#name {{
                    color: #FFFFFF;
                    font-size: 13pt;
                    font-weight: bold;
                }}
                QLabel#expression {{
                    color: #E5E5E7;
                    font-size: 12pt;
                    font-family: 'SF Mono', 'Courier New', monospace;
                    background-color: #3A3A3C;
                    padding: 8px 12px;
                    border-radius: 6px;
                }}
                QLabel#header {{
                    color: #8E8E93;
                    font-size: 11pt;
                    font-weight: 500;
                }}
                QScrollArea {{
                    background-color: #2C2C2E;
                    border: none;
                    border-radius: 12px;
                }}
                QScrollArea > QWidget {{
                    background-color: transparent;
                }} """)

    def generate_steps(self):
        internal_input = MathFormatter.to_internal(self.input_expression)
        internal_optional = MathFormatter.to_internal(self.optional_input)
        return self.router.generate_steps(self.operation, internal_input, internal_optional)

    def format_steps(self):
        if not self.steps_data.get('success', False):
            error_msg = self.steps_data.get('error', 'unknown error')
            return f'''
            <div style="background-color: #3A3A3C; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="color: #FF453A; font-size: 48px; margin-bottom: 10px;">⚠</div>
                <div style="color: #FF453A; font-size: 14pt; font-weight: bold;">Error</div>
                <div style="color: #E5E5E7; margin-top: 10px;">{error_msg}</div>
            </div>
            '''

        steps = self.steps_data.get('steps', [])
        if not steps:
            return '<div style="color: #8E8E93; text-align: center; padding: 40px;">No steps available</div>'

        html_parts = []
        for i, step in enumerate(steps, 1):
            title = step.get('title', '')
            expression = step.get('expression', '')
            explanation = step.get('explanation', '')
            rule = step.get('rule', '')
            is_final = step.get('is_final', False)

            # Get additional explanation fields
            explanation_pack = step.get('explanation_pack', {})
            hint = explanation_pack.get('hint', '')
            common_mistake = explanation_pack.get('common_mistake', '')
            follow_up = explanation_pack.get('follow_up', '')

            formatted_expr = MathFormatter.to_display(expression)

            if is_final:
                step_accent = '#34C759'
                step_bg = '#1C3A28'
                border_style = f'border: 2px solid {step_accent};'
                icon = '✓'
            else:
                step_accent = '#007AFF'
                step_bg = '#1C2C3A'
                border_style = f'border: 1px solid #3A3A3C;'
                icon = str(i)

            # Build hint section if available
            hint_html = ''
            if hint:
                hint_html = f'''
                <div style="
                    background-color: rgba(52, 199, 89, 0.15);
                    border-left: 3px solid #34C759;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 12px 0;
                    color: #D1F2E0;
                    font-size: 11pt;
                ">
                    {hint}
                </div>
                '''

            # Build common mistake section if available
            mistake_html = ''
            if common_mistake:
                mistake_html = f'''
                <div style="
                    background-color: rgba(255, 69, 58, 0.15);
                    border-left: 3px solid #FF453A;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 12px 0;
                    color: #FFD1CE;
                    font-size: 11pt;
                ">
                    {common_mistake}
                </div>
                '''

            # Build follow-up section if available
            followup_html = ''
            if follow_up:
                followup_html = f'''
                <div style="
                    background-color: rgba(255, 159, 10, 0.15);
                    border-left: 3px solid #FF9F0A;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 12px 0;
                    color: #FFE4C4;
                    font-size: 11pt;
                ">
                    {follow_up}
                </div>
                '''

            # Special handling for FOIL steps to show in columns
            if "apply foil" in title.lower() and "\n" in formatted_expr:
                # Parse FOIL breakdown
                foil_parts = formatted_expr.split('\n')
                foil_boxes = ""
                for part in foil_parts:
                    if part.strip():
                        foil_boxes += f'''
                        <div style="
                            background-color: #1C1C1E;
                            border: 2px solid {step_accent};
                            border-radius: 10px;
                            padding: 14px;
                            margin: 8px 0;
                            font-family: 'SF Mono', 'Courier New', monospace;
                            font-size: 14pt;
                            color: #FFFFFF;
                        ">
                            {part}
                        </div>
                        '''
                expression_box = f'''
                <div style="
                    background-color: #2C2C2E;
                    border-radius: 12px;
                    padding: 16px;
                    margin: 12px 0;
                ">
                    <div style="
                        color: {step_accent};
                        font-weight: bold;
                        font-size: 12pt;
                        margin-bottom: 10px;
                    ">FOIL Breakdown:</div>
                    {foil_boxes}
                </div>
                '''
            else:
                expression_box = f'''
                <div style="
                    background-color: #2C2C2E;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 12px 0;
                    font-family: 'SF Mono', 'Courier New', monospace;
                    font-size: 20pt;
                    color: #FFFFFF;
                    text-align: center;
                    border-left: 4px solid {step_accent};
                    box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
                ">
                    {formatted_expr}
                </div>
                '''

            html = f'''
            <div style="
                background: linear-gradient(135deg, {step_bg} 0%, {step_bg}dd 100%);
                {border_style}
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                position: relative;
            ">
                <!-- Step number badge -->
                <div style="
                    position: absolute;
                    top: -10px;
                    left: 20px;
                    background-color: {step_accent};
                    color: white;
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 18px;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.3);
                    border: 3px solid #1C1C1E;
                ">{icon}</div>

                <!-- Title -->
                <div style="
                    color: #FFFFFF;
                    font-size: 16pt;
                    font-weight: 700;
                    text-transform: capitalize;
                    margin: 10px 0 16px 0;
                    padding-left: 50px;
                    letter-spacing: 0.5px;
                ">
                    {title}
                </div>

                <!-- Expression box -->
                {expression_box}

                <!-- Main explanation -->
                <div style="
                    color: #E5E5E7;
                    font-size: 12pt;
                    line-height: 1.7;
                    margin: 16px 0;
                    padding: 16px;
                    background-color: rgba(255,255,255,0.06);
                    border-radius: 10px;
                    border-left: 3px solid {step_accent};
                ">
                    <div style="color: {step_accent}; font-weight: 600; margin-bottom: 8px;">📝 Explanation:</div>
                    {explanation}
                </div>

                {hint_html}
                {mistake_html}
                {followup_html}

                <!-- Rule badge -->
                <div style="
                    color: #8E8E93;
                    font-size: 10pt;
                    margin-top: 12px;
                    padding: 8px 12px;
                    background-color: rgba(255,255,255,0.03);
                    border-radius: 6px;
                    display: inline-block;
                    font-style: italic;
                ">
                    📘 {rule}
                </div>
            </div>
            '''
            html_parts.append(html)

        return ''.join(html_parts)

    def create_info_row(self, label_text: str, value_text: str) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(10)

        label = QLabel(label_text)
        label.setObjectName("header")
        label.setFixedWidth(180)

        value = QLabel(value_text)
        value.setObjectName("expression")
        value.setWordWrap(True)

        row.addWidget(label)
        row.addWidget(value, 1)
        return row

    def initialise_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        window_layout = QVBoxLayout()
        window_layout.setSpacing(12)

        window_layout.addLayout(self.create_info_row("Operation:", self.operation.upper()))
        window_layout.addLayout(self.create_info_row("Input:", self.input_expression))

        if self.optional_input:
            window_layout.addLayout(self.create_info_row("Optional Input:", self.optional_input))

        window_layout.addLayout(self.create_info_row("Answer:", self.result))

        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #3A3A3C;")
        window_layout.addWidget(separator)

        learning_hint_layout = QVBoxLayout()
        learning_hint_layout.setSpacing(12)

        hinting_label = QLabel("Solution Steps")
        hinting_label.setObjectName("name")
        hinting_label.setStyleSheet("font-size: 16pt; font-weight: bold; margin-top: 8px;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(300)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        learning_hints = QLabel(self.format_steps())
        learning_hints.setObjectName("learning")
        learning_hints.setWordWrap(True)
        learning_hints.setTextFormat(Qt.TextFormat.RichText)

        scroll_layout.addWidget(learning_hints)
        scroll_area.setWidget(scroll_content)

        learning_hint_layout.addWidget(hinting_label)
        learning_hint_layout.addWidget(scroll_area)

        window_layout.addLayout(learning_hint_layout)

        layout.addLayout(window_layout)

    def create_label(self, text, object_name, width=None):
        label = QLabel(text)
        label.setObjectName(object_name)
        if width:
            label.setFixedWidth(width)
        return label

    def create_box_layout(self, label_name, label_value, width):
        layout = QHBoxLayout()
        layout.addWidget(self.create_label(label_name, "name", width))
        layout.addWidget(self.create_label(label_value, "expression"))
        return layout