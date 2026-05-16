from morse_int import MorseInt

#ExprToMorse : конвертирует арифметическое выражение (строка) в Морзе
class ExprToMorse:
    def __init__(self):
        self._ops = {
            '+': '.-.-.',
            '-': '-....-',
            '*': '.-..-.',
            '/': '-..-.',
            '=': '-...-',
        }

    def __call__(self, expression):
        parts = []
        for token in expression.split():
            if token in self._ops:
                parts.append(self._ops[token])
            else:
                morse_digits = []
                for d in token:
                    morse_digits.append(MorseInt._to_morse[d])
                parts.append('   '.join(morse_digits))
        return '       '.join(parts)
