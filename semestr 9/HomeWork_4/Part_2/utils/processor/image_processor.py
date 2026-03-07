import cv2
import numpy as np

def compute_histogram(image, bins=256):
    """
    Вычисление гистограммы для изображения
    Возврат - массив гистограммы
    """

    histogram = cv2.calcHist([image], [0], None, [bins], [0, 256])
    return histogram.flatten()



def histogram_equalization(image):
    """
    Эквализация гистограммы
    Возврат - изображение после эквализации
    """

    height, width = image.shape
    pixel_count = height * width

    #вычисляем гистограмму
    hist = compute_histogram(image)

    #вычисляем CDF (кумулятивная функция распределения)
    cdf = []
    sum_ = 0
    for freq in hist:
        sum_ += freq
        cdf.append(sum_)

    #находим мин ненулевое значение CDF
    cdf_min = min(v for v in cdf if v > 0)

    #создаем lookup table для преобразования
    lookup = [0] * 256
    for i in range(256):
        if pixel_count > cdf_min:
            normalized = (cdf[i] - cdf_min) / (pixel_count - cdf_min)
            lookup[i] = int(normalized * 255)
        else:
            lookup[i] = i
    
    #преобразуем по lokup table
    lookup = np.array(lookup, dtype=np.uint8)
    equalized = lookup[image.flatten()].astype(np.uint8) #индексируем image по lookup
    equalized = equalized.reshape(image.shape)

    return equalized

def gamma_correction(image, gamma=1.0):
    """
    Гамма-коррекция изображения
    Возврат - изображение после коррекции
    """
    
    if gamma == 1.0:
        return image.copy()

    #lookup table
    inv_gamma = 1.0 / gamma
    lookup = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)], dtype=np.uint8)
    corrected = lookup[image]

    return corrected