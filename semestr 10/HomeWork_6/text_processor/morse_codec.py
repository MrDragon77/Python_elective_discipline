import re

EN_CODE = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',
    'F': '..-.', 'G': '--.',  'H': '....', 'I': '..',   'J': '.---',
    'K': '-.-',  'L': '.-..', 'M': '--',   'N': '-.',   'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/',
}

RU_CODE = {
    'А': '.-',   'Б': '-...', 'В': '.--',  'Г': '--.',  'Д': '-..',
    'Е': '.',    'Ж': '...-', 'З': '--..',  'И': '..',  'Й': '.---',
    'К': '-.-',  'Л': '.-..', 'М': '--',   'Н': '-.',   'О': '---',
    'П': '.--.', 'Р': '.-.',  'С': '...',  'Т': '-',    'У': '..-',
    'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----',
    'Щ': '--.-', 'Ъ': '--.--','Ы': '-.--', 'Ь': '-..-', 'Э': '..-..',
    'Ю': '..--', 'Я': '.-.-',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/',
}

EN_DECODE = {v: k for k, v in EN_CODE.items()}
RU_DECODE = {v: k for k, v in RU_CODE.items()}


def encode_text(text: str, lang: str = 'en') -> str:
    table = EN_CODE if lang == 'en' else RU_CODE
    tokens = []
    for ch in text.upper():
        if ch == ' ':
            tokens.append('/')
        elif ch in table:
            tokens.append(table[ch])
    return ' '.join(tokens)


def decode_text(morse: str, lang: str = 'en') -> str:
    table = EN_DECODE if lang == 'en' else RU_DECODE
    result = []
    for token in morse.strip().split():
        if token == '/':
            result.append(' ')
        else:
            result.append(table.get(token, '?'))
    return ''.join(result)


def check_is_morse(text: str) -> bool:
    s = text.strip()
    if not s:
        return False
    return bool(re.fullmatch(r'[.\-/ \t\n]+', s)) and ('.' in s or '-' in s)
