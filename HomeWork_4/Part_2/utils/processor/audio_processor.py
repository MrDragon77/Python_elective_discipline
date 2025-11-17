import wave
import struct
import numpy as np
import cv2

def compute_audio_histogram(audio_data, bins=256):
    """
    Вычисление гистограммы для аудио
    Вовзрат - гистограмма
    """
    
    audio_float = audio_data.astype(np.float64)
    min_val = audio_float.min()
    max_val = audio_float.max()
    
    # Если диапазон пустой (все значения одинаковые)
    if max_val == min_val:
        histogram = np.zeros(bins, dtype=np.int64)
        histogram[0] = len(audio_data)  # Все значения в первом бине
        return histogram
    
    # Нормализуем в диапазон [0, bins-1]
    normalized = ((audio_float - min_val) * (bins - 1) / (max_val - min_val))
    
    # Округляем и приводим к целому типу
    normalized = np.round(normalized).astype(np.int32)
    
    # Обрезаем значения на случай выхода за границы из-за округления
    normalized = np.clip(normalized, 0, bins - 1)
    
    # Вычисляем гистограмму
    histogram = np.bincount(normalized, minlength=bins)
    
    return histogram

def quantize_audio(audio_data, bins=256):
    """
    Квантование аудио данных
    """
    if len(audio_data) == 0:
        return audio_data
    
    original_dtype = audio_data.dtype
    audio_float = audio_data.astype(np.float64)

    min_val = audio_float.min()
    max_val = audio_float.max()
    range_val = max_val - min_val

    if range_val == 0:
        return audio_float.copy()

    normalized = (audio_float - min_val) / range_val * (bins - 1)
    quantized_levels = np.round(normalized)
    quantized = (quantized_levels / (bins - 1)) * range_val + min_val

    return quantized.astype(original_dtype)
