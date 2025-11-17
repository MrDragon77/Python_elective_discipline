import wave
import struct
import numpy as np
import cv2

def draw_audio_histogram(histogram, width=1024, height=1024,
                         bg_color=(255, 255, 255), hist_color=(255, 0, 0)):
    """
    Отрисовка гистограммы аудио как изображение
    """

    if isinstance(histogram, list):
        histogram = np.array(histogram, dtype=np.float32)
    else:
        histogram = histogram.astype(np.float32)

    img_arr = np.zeros((height, width, 3), dtype=np.uint8)
    img_arr[:, :] = bg_color

    if histogram.max() > 0:
        hist_normalized = histogram / histogram.max()
    else:
        hist_normalized = histogram

    bin_width = width / 256

    for bin_idx in range(256):
        x_start = int(bin_idx * bin_width)
        x_end = int((bin_idx + 1) * bin_width)
        bar_height = int(hist_normalized[bin_idx] * height)
        y_start = height - bar_height
        img_arr[y_start:height, x_start:x_end] = hist_color

    return img_arr
