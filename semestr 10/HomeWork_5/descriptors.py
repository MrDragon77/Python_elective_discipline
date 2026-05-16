import os
import numpy as np
import cv2


#FileNotEmpty : дескриптор — файл не должен быть пустым
class FileNotEmpty:
    def __set_name__(self, owner, name):
        self._attr = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self._attr)

    def __set__(self, obj, value):
        if isinstance(value, str) and os.path.isfile(value):
            if os.path.getsize(value) == 0:
                raise ValueError(f"File is empty: '{value}'")
        obj.__dict__[self._attr] = value


#MinColorCount : дескриптор — изображение должно содержать > 2 уникальных цветов
class MinColorCount:
    def __set_name__(self, owner, name):
        self.attr_name = '_checked_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.attr_name, None)

    def __set__(self, obj, value):
        if isinstance(value, np.ndarray) and value.size > 0:
            if len(value.shape) == 3:
                flat = value.reshape(-1, value.shape[-1])
                n_colors = len(np.unique(flat, axis=0))
            else:
                n_colors = len(np.unique(value.ravel()))
            if n_colors <= 2:
                raise ValueError(f"Too few unique colors: {n_colors} (need > 2)")
        setattr(obj, self.attr_name, value)


#NormalizedImage : дескриптор — автоматически приводит изображение к размеру 256x256
class NormalizedImage:
    def __set_name__(self, owner, name):
        self._store = '_norm_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._store, None)

    def __set__(self, obj, value):
        if isinstance(value, str):
            img = cv2.imread(value)
            if img is None:
                raise ValueError(f"Cannot read image: '{value}'")
            value = cv2.resize(img, (256, 256))
        elif isinstance(value, np.ndarray):
            value = cv2.resize(value, (256, 256))
        setattr(obj, self._store, value)


#ImageRecord : контейнер с тремя дескрипторами для валидации и загрузки изображения
class ImageRecord:
    path = FileNotEmpty()
    data = NormalizedImage()
    validated = MinColorCount()

    def load(self, filepath):
        self.path = filepath
        self.data = filepath
        self.validated = self.data
        return self.validated
