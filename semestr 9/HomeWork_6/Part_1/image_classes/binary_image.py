from image_classes.image import Image
import cv2

class BinaryImage(Image):
    def load(self):
        try:
            image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        except:
            print(f"Ошибка! Не удалось загрузить изображение {self.path}")
        else:
            _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
            return image
        




