import cv2
import numpy as np
from image_converter import ImageConverter
from image_classes.binary_image import BinaryImage
from image_classes.color_image import ColorImage
from image_classes.monochrome_image import MonochromeImage

def main():
    color_image = ColorImage(path="image.jpg")
    #Исходное
    color_image.show()
    
    #Цветное -> Монохром
    monochrome_image = ImageConverter.color_to_monochrome(color_image)
    monochrome_image.show()
    
    #Монохром -> Монохром
    monochrome_image_2 = ImageConverter.monochrome_to_monochrome(monochrome_image)
    monochrome_image_2.show()
    
    #Монохром -> Цветное
    color_image_2 = ImageConverter.monochrome_to_color(monochrome_image_2)
    color_image_2.show()
    
    #Монохром -> Бинарное
    binary_image = ImageConverter.monochrome_to_binary(monochrome_image_2, threshold=128)
    binary_image.show()
    
    #Бинарное -> Монохром
    monochrome_image_3 = ImageConverter.binary_to_monochrome(binary_image)
    monochrome_image_3.show()
    
    #Цветное -> Цветное
    color_image_3 = ImageConverter.color_to_color(color_image)
    color_image_3.show()
    
    #Цветное -> Бинарное
    binary_image_2 = ImageConverter.color_to_binary(color_image)
    binary_image_2.show()

    #Бинарное -> Цветное
    color_image_4 = ImageConverter.binary_to_color(binary_image)
    color_image_4.show()
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
