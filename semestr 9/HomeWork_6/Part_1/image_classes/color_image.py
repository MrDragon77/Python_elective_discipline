from image_classes.image import Image
import cv2

class ColorImage(Image):
    def load(self):
        try:
            image = cv2.imread(self.path, cv2.IMREAD_COLOR)
        except:
            print(f"Ошибка! Не удалось загрузить изображение {self.path}")
        else:
            return image
