from text_processor.morse_codec import encode_text, decode_text, check_is_morse
from text_processor.morse_detect import MorseKNN
from text_processor.lang_detect import LangKNN
from text_processor.params import parse_params
from description_gen import generate_description
from text_reader import TextReader


if __name__ == '__main__':

    # Morse codec
    original = 'SIZE 256 CELLS 5'
    encoded = encode_text(original)
    decoded = decode_text(encoded)
    print(f'Morse codec:\noriginal : {original}\nencoded  : {encoded}\ndecoded  : {decoded}\nis_morse : {check_is_morse(encoded)}')

    # Morse KNN detector
    print('\nMorse KNN detector:')
    mknn = MorseKNN(k=3)
    samples = [
        ('... .. --.. .', True),
        ('image size 256x256 cells 5', False),
        ('.-. --. -.', True),
        ('размер изображения 128x128', False),
    ]
    for text, expected in samples:
        pred = mknn.predict(text)
        print(f'"{text[:30]:<30}" -> morse={pred} (expected={expected})')

    # Language KNN detector
    print('\nLanguage KNN detector:')
    lknn = LangKNN(k=3)
    lang_samples = [
        ('image size 256x256 number of cells 5 rgb', 'en'),
        ('размер изображения 256x256 количество клеток 7', 'ru'),
        ('grayscale mode overlap not allowed', 'en'),
        ('цветное rgb пересечение запрещено', 'ru'),
    ]
    for text, expected in lang_samples:
        pred = lknn.predict(text)
        print(f'"{text[:35]:<35}" -> lang={pred} (expected={expected})')

    # Parameter extraction
    en_text = 'Image size 128x128 pixels. Number of cells 3. RGB color mode. Overlap is not allowed.'
    ru_text = 'Размер изображения 256x256 пикселей. Количество клеток 7. Цветное RGB. Пересечение запрещено.'
    print(f'\nParameter extraction:\nEN: {parse_params(en_text, "en")}\nRU: {parse_params(ru_text, "ru")}')

    # Description generator
    en_desc = generate_description([256, 256], 5, grayscale=False, allow_overlap=True, lang='en')
    ru_desc = generate_description([128, 128], 3, grayscale=True, allow_overlap=False, lang='ru')
    print(f'\nDescription generator:\nEN: {en_desc}\nRU: {ru_desc}')

    # TextReader on files
    print('\nTextReader on files:')
    reader = TextReader()
    for fname in ('data/sample_en.txt', 'data/sample_ru.txt', 'data/sample_morse_en.txt'):
        result = reader.read_file(fname)
        info = {k: v for k, v in result.items() if not k.startswith('_')}
        print(f'{fname}\nlang={result["_lang"]} morse={result["_was_morse"]} params={info}')
