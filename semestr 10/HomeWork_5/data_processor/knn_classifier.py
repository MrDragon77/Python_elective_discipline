import cv2
import numpy as np
from .processor_plugin import ProcessorBase


#KnnClassifier : классификация KNN по гистограмме оттенков серого
class KnnClassifier(ProcessorBase, name='knn'):
    def __init__(self, k=3):
        self.k = k
        self._features = []
        self._labels = []

    def fit(self, images, labels):
        self._features = [self._extract(img) for img in images]
        self._labels = list(labels)

    def process(self, image):
        if not self._features:
            return {'label': None, 'message': 'not fitted'}

        query = self._extract(image)
        dists = [float(np.linalg.norm(query - f)) for f in self._features]
        top_k = np.argsort(dists)[:self.k]
        k_labels = [self._labels[i] for i in top_k]
        label = max(set(k_labels), key=k_labels.count)
        return {'label': label, 'k_neighbors': k_labels, 'distances': [dists[i] for i in top_k]}

    def _extract(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        small = cv2.resize(gray, (32, 32))
        hist = cv2.calcHist([small], [0], None, [32], [0, 256]).flatten()
        norm = np.linalg.norm(hist)
        return hist / norm if norm > 0 else hist
