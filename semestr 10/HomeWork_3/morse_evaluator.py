from morse_int import MorseInt

#MorseEvaluator : декодирует Морзе-выражение и вычисляет результат (если есть =)
class MorseEvaluator:
    def __init__(self):
        self._ops = {
            '.-.-.':  '+',
            '-....-': '-',
            '.-..-.' : '*',
            '-..-.':  '/',
            '-...-':  '=',
        }

    def __call__(self, morse_expr):
        tokens = morse_expr.split('       ')
        decoded = []
        for token in tokens:
            token = token.strip()
            if token in self._ops:
                decoded.append(self._ops[token])
            else:
                digits = ''
                for c in token.split('   '):
                    if c.strip():
                        digits += MorseInt._from_morse[c]
                decoded.append(digits)

        lines = ['Decoded:        ' + ' '.join(decoded)]

        if decoded and decoded[-1] == '=':
            result = int(eval(' '.join(decoded[:-1])))
            lines.append('Arabic result:  ' + str(result))
            lines.append('Morse result:   ' + MorseInt(result)._encode())

        return '\n'.join(lines)
