import numpy as np
from .morse_codec import check_is_morse


#MorseKNN : KNN-классификатор для определения — морзе или обычный текст
class MorseKNN:
    def __init__(self, k=3):
        self.k = k
        self._train_x = []
        self._train_y = []

        plain = [
            'image size 256x256 number of cells 5 rgb',
            'size 128x128 cells 3 grayscale mode',
            'generator config width 512 height 512',
            'размер изображения 256x256 количество клеток 7',
            'конфигурация генератора размер 128 клеток 4',
        ]
        morse = [
            '... .. --.. . / ..--- ..... -.... / -.-. . .-.. .-.. ... / .....',
            '.. -- .- --. . / ... .. --.. . / ..--- ..... -....',
            '... .. --.. . / .---- ..--- ---.. -..- .---- ..--- ---.. / -.-. . .-.. .-.. ...',
        ]
        texts = plain + morse
        labels = [False] * len(plain) + [True] * len(morse)
        self.fit(texts, labels)

    def fit(self, texts, labels):
        self._train_x = [self._features(t) for t in texts]
        self._train_y = list(labels)

    def predict(self, text):
        if check_is_morse(text):
            return True
        q = self._features(text)
        dists = [float(np.linalg.norm(q - f)) for f in self._train_x]
        top_k = np.argsort(dists)[:self.k]
        votes = [self._train_y[i] for i in top_k]
        return sum(votes) > len(votes) / 2

    def _features(self, text):
        n = max(len(text), 1)
        dot_r   = text.count('.') / n
        dash_r  = text.count('-') / n
        slash_r = text.count('/') / n
        alpha_r = sum(c.isalpha() for c in text) / n
        digit_r = sum(c.isdigit() for c in text) / n
        return np.array([dot_r, dash_r, slash_r, alpha_r, digit_r], dtype=np.float32)
