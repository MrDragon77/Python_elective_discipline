import cv2
import numpy as np
from image_classes.binary_image import BinaryImage
from image_classes.color_image import ColorImage
from image_classes.monochrome_image import MonochromeImage

class ImageConverter:
    @staticmethod
    def monochrome_to_monochrome(monochrome_image: MonochromeImage) -> MonochromeImage:
        if monochrome_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        return MonochromeImage(image=cv2.equalizeHist(monochrome_image.image))
    
    @staticmethod
    def color_to_color(color_image: ColorImage) -> ColorImage:
        if color_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        channels = cv2.split(color_image.image)
        equalized_channels = [cv2.equalizeHist(i) for i in channels]
        return ColorImage(image=cv2.merge(equalized_channels))
    
    @staticmethod
    def binary_to_binary(binary_image: BinaryImage) -> BinaryImage:
        if binary_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        return binary_image

    @staticmethod
    def color_to_monochrome(color_image: ColorImage) -> MonochromeImage:
        if color_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        return MonochromeImage(image=cv2.cvtColor(color_image.image, cv2.COLOR_BGR2GRAY))
    
    @staticmethod
    def _create_monochrome_to_color_palette():
        try:
            palette = {}
            for gray in range(256):
                t = gray / 255.
                blue = int(255 * (1 - t))
                green = 0
                red = int(255 * t)
                palette[gray] = (blue, green, red)
            return palette
        except:
            print("Ошибка во время вычисления палитры")
    @staticmethod
    def monochrome_to_color(monochrome_image: MonochromeImage, palette = None) -> ColorImage:
        if monochrome_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        if palette is None:
            palette = ImageConverter._create_monochrome_to_color_palette()
        h, w = monochrome_image.image.shape
        color_image = np.zeros((h, w, 3), dtype=np.uint8)
        for gray, color in palette.items():
            mask = (monochrome_image.image == gray)
            color_image[mask] = color
        return ColorImage(image=color_image)
    
    @staticmethod
    def monochrome_to_binary(monochrome_image: MonochromeImage, threshold = 128) -> BinaryImage:
        if monochrome_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        if threshold > 255:
            threshold = 255
        if threshold < 0:
            threshold = 0
        _, binary_image = cv2.threshold(monochrome_image.image, threshold, 255, cv2.THRESH_BINARY)
        return BinaryImage(image=binary_image)
    
    @staticmethod
    def binary_to_monochrome(binary_image: BinaryImage) -> MonochromeImage:
        if binary_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        dist = cv2.distanceTransform(binary_image.image, cv2.DIST_L2, 3)
        norm_dist = cv2.normalize(dist, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        return MonochromeImage(image=norm_dist)
    
    @staticmethod
    def color_to_binary(color_image: ColorImage) -> BinaryImage:
        if color_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        monochrome_image = ImageConverter.color_to_monochrome(color_image)
        binary_image = ImageConverter.monochrome_to_binary(monochrome_image)
        return binary_image
    
    @staticmethod
    def binary_to_color(binary_image: BinaryImage) -> ColorImage:
        if binary_image is None:
            raise ValueError("Ошибка! Изображение пустое")
        monochrome_image = ImageConverter.binary_to_monochrome(binary_image)
        color_image = ImageConverter.monochrome_to_color(monochrome_image)
        return color_image





