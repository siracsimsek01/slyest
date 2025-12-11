import re


class MathFormatter:

    SUPERSCRIPTS = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'x': 'ˣ', 'y': 'ʸ', 'i': 'ⁱ', '/': 'ᐟ'
    }

    SUPERSCRIPTS_REVERSE = {v: k for k, v in SUPERSCRIPTS.items()}

    @classmethod
    def to_display(cls, internal_expr: str) -> str:
        if not internal_expr:
            return internal_expr

        result = internal_expr
        result = cls._convert_functions(result)
        result = cls._convert_exponents(result)
        result = cls._hide_implicit_multiplication(result)
        result = result.replace('*', '×')
        return result

    @classmethod
    def to_internal(cls, display_expr: str) -> str:
        if not display_expr:
            return display_expr

        result = display_expr
        result = cls._convert_superscripts_to_power(result)
        result = result.replace('×', '*')
        result = result.replace('÷', '/')
        result = cls._convert_functions_back(result)

        return result

    @classmethod
    def _convert_functions(cls, text: str) -> str:
        text = text.replace('**(1/2)', '√')
        text = text.replace('**(1/3)', '∛')
        text = re.sub(r'\*\*\(1/', '√⁽¹ᐟ', text)
        text = re.sub(r'\bpi\b', 'π', text)
        text = re.sub(r'\bexp\(', 'e^(', text)
        text = re.sub(r'\blog\(([^,]+)\)', r'ln(\1)', text)
        return text

    @classmethod
    def _convert_functions_back(cls, text: str) -> str:
        text = text.replace('√', '**(1/2)')
        text = text.replace('∛', '**(1/3)')
        text = re.sub(r'√⁽¹ᐟ', '**(1/', text)
        text = text.replace('π', 'pi')
        text = re.sub(r'\be\^\(', 'exp(', text)
        text = re.sub(r'\bln\(', 'log(', text)
        return text

    @classmethod
    def _convert_exponents(cls, text: str) -> str:
        def replace_exponent(match):
            exponent = match.group(1)
            superscript = ''
            for char in exponent:
                superscript += cls.SUPERSCRIPTS.get(char, char)
            return superscript

        return re.sub(r'\*\*([0-9]+|[a-z])', replace_exponent, text)

    @classmethod
    def _hide_implicit_multiplication(cls, text: str) -> str:
        
        text = re.sub(r'(\d+)\*([a-zA-Z])', r'\1\2', text)

        
        text = re.sub(r'([a-zA-Z])\*([a-zA-Z])', r'\1\2', text)

        
        text = re.sub(r'(\d+)\*\(', r'\1(', text)

        
        text = re.sub(r'\)\*(\d+)', r')\1', text)

        
        text = re.sub(r'\)\*([a-zA-Z])', r')\1', text)

        
        text = re.sub(r'([a-zA-Z])\*\(', r'\1(', text)
        
        text = re.sub(r'\)\*\(', r')(', text)

        return text

    @classmethod
    def _convert_superscripts_to_power(cls, text: str) -> str:
        superscript_chars = ''.join(cls.SUPERSCRIPTS_REVERSE.keys())

        def replace_superscript_sequence(match):
            superscripts = match.group(0)
            normal = ''
            for char in superscripts:
                normal += cls.SUPERSCRIPTS_REVERSE.get(char, char)
            return f"**{normal}"

        pattern = f'[{re.escape(superscript_chars)}]+'
        return re.sub(pattern, replace_superscript_sequence, text)

    @classmethod
    def format_result(cls, result_text: str) -> str:
        return cls.to_display(result_text)
