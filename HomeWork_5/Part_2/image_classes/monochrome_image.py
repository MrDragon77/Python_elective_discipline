from image_classes.image import Image
import cv2

class MonochromeImage(Image):
    def load(self):
        image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Ошибка! Не удалось загрузить изображение {self.path}")
        return image
