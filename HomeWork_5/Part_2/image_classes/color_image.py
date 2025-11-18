from image_classes.image import Image
import cv2

class ColorImage(Image):
    def load(self):
        image = cv2.imread(self.path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Ошибка! Не удалось загрузить изображение {self.path}")
        return image
