from text_processor.morse_codec import decode_text, check_is_morse
from text_processor.morse_detect import MorseKNN
from text_processor.lang_detect import LangKNN
from text_processor.params import parse_params


_EN_VOCAB = {'size', 'image', 'cells', 'number', 'color', 'rgb', 'grayscale',
             'overlap', 'pixels', 'generator', 'mode', 'objects', 'count'}
_RU_VOCAB = {'размер', 'изображения', 'клеток', 'количество', 'цветное',
             'серого', 'оттенках', 'пересечение', 'объектов', 'пикселей'}


#TextReader : загрузка и разбор текстовых файлов с конфигурацией генератора
class TextReader:
    def __init__(self):
        self._morse_knn = MorseKNN(k=3)
        self._lang_knn = LangKNN(k=3)

    def read_file(self, filename: str) -> dict:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.parse(text)

    def parse(self, text: str) -> dict:
        was_morse = self._morse_knn.predict(text)

        if was_morse:
            lang = self._guess_morse_lang(text)
            decoded = decode_text(text, lang)
        else:
            lang = self._lang_knn.predict(text)
            decoded = text

        params = parse_params(decoded, lang)

        return {
            '_lang': lang,
            '_was_morse': was_morse,
            '_decoded': decoded,
            **params,
        }

    def _guess_morse_lang(self, morse: str) -> str:
        en_text = decode_text(morse, 'en').lower()
        ru_text = decode_text(morse, 'ru').lower()
        en_score = sum(1 for w in _EN_VOCAB if w in en_text)
        ru_score = sum(1 for w in _RU_VOCAB if w in ru_text)
        return 'ru' if ru_score > en_score else 'en'
