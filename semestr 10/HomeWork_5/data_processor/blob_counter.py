import cv2
import numpy as np
from .processor_plugin import ProcessorBase


#BlobCounter : подсчёт объектов через findContours
class BlobCounter(ProcessorBase, name='count'):
    MIN_AREA = 50

    def process(self, image: np.ndarray) -> dict:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bboxes = []
        for cnt in contours:
            if cv2.contourArea(cnt) >= self.MIN_AREA:
                x, y, w, h = cv2.boundingRect(cnt)
                bboxes.append((x, y, w, h))

        return {'num_objects': len(bboxes), 'bboxes': bboxes}
