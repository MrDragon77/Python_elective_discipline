import cv2

class Image:
    counter = 0
    def __init__(self, path = None, image = None):
        if path is not None:
            self.path = path
            self.image = self.load()
        else:
            self.path = "image" + str(Image.counter) + ".jpg"
            self.image = image
        self.id = Image.counter
        Image.counter += 1
    def load(self):
        try:
            image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        except:
            print(f"Ошибка! Не удалось загрузить изображение {self.path}")
    def save(self, save_path = None):
        if self.image is None:
            raise ValueError("Ошибка! Нет изображения для сохранения")
        if save_path is None:
            save_path = self.path
        
        try:
            cv2.imwrite(save_path, self.image)
        except:
            print(f"Ошибка! Не удалось сохранить изображение {self.path}")
    def show(self):
        if self.image is None:
            raise ValueError("Ошибка! Нет изображения для показа")
        cv2.imshow("Image" + str(self.id), self.image)
