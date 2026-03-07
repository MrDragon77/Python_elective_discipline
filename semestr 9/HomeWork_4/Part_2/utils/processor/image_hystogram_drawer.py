import cv2
import numpy as np

def draw_histogram_image(histogram, width=1024, height=1024, 
                        bg_color=(255, 255, 255), hist_color=(0, 0, 255)):
    """
    Отрисовка гистограммы как изображение размером width x height пикселей.
    """
    histogram = histogram.astype(np.float32)

    img_arr = np.zeros((height, width, 3), dtype=np.uint8)
    img_arr[:, :, :] = bg_color

    #нормализуем гистограмму
    if histogram.max() > 0:
        hist_normalized = histogram / histogram.max()
    else:
        hist_normalized = histogram

    #рисуем столбцы гистограммы
    bin_width = width / len(hist_normalized)
    for bin_i in range(len(hist_normalized)):
        x_start = int(bin_i * bin_width)
        x_end = int((bin_i + 1) * bin_width)
        
        bar_height = int(hist_normalized[bin_i] * height)
        y_start = height - bar_height

        img_arr[y_start:height, x_start:x_end] = hist_color

    return img_arr