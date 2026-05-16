import re

_RU = {
    'size': [
        r'размер\s+изображения\s+(\d+)\s*[xXхХ×]\s*(\d+)',
        r'размер\s+(\d+)\s*[xXхХ×]\s*(\d+)',
        r'(\d+)\s*[xXхХ×]\s*(\d+)\s*пиксел',
    ],
    'count': [
        r'количество\s+(?:объектов|клеток)\s+(?:равно\s+)?(\d+)',
        r'клеток[:\s]+(\d+)',
        r'(\d+)\s+(?:клеток|клетки|объектов)',
    ],
    'gray': [
        r'оттенк\w*\s+серого',
        r'чёрно.?бел',
        r'\bчб\b',
    ],
    'overlap': [
        r'пересечени[ея]\s+(?:объектов\s+)?(?:разрешен|допустим)',
        r'объекты\s+могут\s+пересекаться',
    ],
}

_EN = {
    'size': [
        r'image\s+size\s+(\d+)\s*[xX×]\s*(\d+)',
        r'size\s+(\d+)\s*[xX×]\s*(\d+)',
        r'(\d+)\s*[xX×]\s*(\d+)\s*pixels?',
    ],
    'count': [
        r'number\s+of\s+(?:objects?|cells?)\s+(?:is\s+)?(\d+)',
        r'cells?[:\s]+(\d+)',
        r'(\d+)\s+(?:objects?|cells?)',
    ],
    'gray': [
        r'gr[ae]yscale',
        r'black\s+and\s+white',
        r'\bb&?w\b',
    ],
    'overlap': [
        r'overlap\s+(?:is\s+)?(?:allowed|permitted)',
        r'objects?\s+(?:may|can)\s+overlap',
    ],
}


def parse_params(text: str, lang: str = 'en') -> dict:
    p = _EN if lang == 'en' else _RU
    t = text.lower()
    result: dict = {}

    for pat in p['size']:
        m = re.search(pat, t)
        if m:
            result['image_size'] = [int(m.group(1)), int(m.group(2))]
            break

    for pat in p['count']:
        m = re.search(pat, t)
        if m:
            result['num_objects'] = int(m.group(1))
            break

    result['color_mode'] = 'RGB'
    for pat in p['gray']:
        if re.search(pat, t):
            result['color_mode'] = 'grayscale'
            break

    result['allow_overlap'] = False
    for pat in p['overlap']:
        if re.search(pat, t):
            result['allow_overlap'] = True
            break

    return result
