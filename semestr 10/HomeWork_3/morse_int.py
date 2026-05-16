#MorseInt : целое число, представленное строкой Морзе
class MorseInt:
    _to_morse = {
        '0': '-----', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..',  '9': '----.',
    }
    _from_morse = {v: k for k, v in _to_morse.items()}
    _MINUS = '-....-'

    def __init__(self, value):
        if isinstance(value, MorseInt):
            self._value = value._value
        elif isinstance(value, int):
            self._value = value
        elif isinstance(value, str):
            self._value = self._decode(value.strip())
        else:
            raise TypeError(f'Cannot create MorseInt from {type(value)}')

    @classmethod
    def _decode(cls, s):
        negative = s.startswith(cls._MINUS)
        if negative:
            s = s[len(cls._MINUS):].strip()
        digits = ''.join(cls._from_morse[code] for code in s.split('   ') if code.strip())
        return -int(digits) if negative else int(digits)

    def _encode(self):
        v = self._value
        prefix = ''
        if v < 0:
            prefix = self._MINUS + '   '
            v = -v
        return prefix + '   '.join(self._to_morse[d] for d in str(v))

    def __str__(self):
        return self._encode()

    def __repr__(self):
        return f'MorseInt({self._value})'

    def __int__(self):
        return self._value

    def __add__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(self._value + v)

    def __radd__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(v + self._value)

    def __sub__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(self._value - v)

    def __rsub__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(v - self._value)

    def __mul__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(self._value * v)

    def __rmul__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(v * self._value)

    def __floordiv__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(self._value // v)

    def __truediv__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return MorseInt(self._value // v)

    def __eq__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return self._value == v

    def __ne__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return self._value != v

    def __lt__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return self._value < v

    def __le__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return self._value <= v

    def __gt__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return self._value > v

    def __ge__(self, other):
        v = other._value if isinstance(other, MorseInt) else int(other)
        return self._value >= v
