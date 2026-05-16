import random


def generate_description(image_size, num_cells, grayscale=False, allow_overlap=True, lang='en'):
    w, h = image_size
    if lang == 'ru':
        color = 'в оттенках серого' if grayscale else 'цветное RGB'
        overlap = 'разрешено' if allow_overlap else 'запрещено'
        templates = [
            f'Конфигурация: размер {w}x{h}, количество клеток {num_cells}, режим {color}, пересечение {overlap}.',
            f'Параметры генератора — размер изображения {w}x{h}, клеток: {num_cells}, {color}, пересечение {overlap}.',
            f'Настройки: {w}x{h} пикселей, {num_cells} клеток, {color}, пересечение объектов {overlap}.',
        ]
    else:
        color = 'grayscale' if grayscale else 'RGB color'
        overlap = 'allowed' if allow_overlap else 'not allowed'
        templates = [
            f'Image generator config: size {w}x{h}, {num_cells} cells, {color}, overlap {overlap}.',
            f'Generator settings — {w}x{h} pixels, cell count: {num_cells}, mode: {color}, overlap: {overlap}.',
            f'Parameters: image size {w}x{h}, number of cells {num_cells}, {color} mode, overlap {overlap}.',
        ]
    return random.choice(templates)
