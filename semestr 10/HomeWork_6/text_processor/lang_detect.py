from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier


#LangKNN : определение языка текста через TF-IDF + KNN
class LangKNN:
    def __init__(self, k=3):
        self.k = k
        self._vec = TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=200)
        self._clf = KNeighborsClassifier(n_neighbors=k)

        ru_samples = [
            'размер изображения количество клеток цветное',
            'конфигурация генератора пересечение объектов запрещено',
            'изображение в оттенках серого пиксели',
            'параметры генератора ширина высота клеток',
            'цветное rgb пересечение разрешено размер',
            'количество объектов режим серый чёрно белый',
            'генератор данных размер изображения клеток',
            'пиксели оттенки серого пересечение объектов',
            'конфигурация размер количество клеток режим',
            'изображение цветное rgb количество клеток пять',
        ]
        en_samples = [
            'image size number of cells rgb color mode',
            'generator configuration overlap allowed pixels',
            'grayscale image width height cells count',
            'image generator parameters color mode overlap',
            'size in pixels number of objects rgb',
            'cells count grayscale mode overlap not allowed',
            'configuration image generator width height',
            'number objects color rgb grayscale pixels',
            'image size parameters cells overlap settings',
            'generator config rgb grayscale overlap cells',
        ]
        texts = ru_samples + en_samples
        labels = ['ru'] * len(ru_samples) + ['en'] * len(en_samples)
        self.fit(texts, labels)

    def fit(self, texts, labels):
        X = self._vec.fit_transform(texts)
        self._clf.fit(X, labels)

    def predict(self, text):
        if any('Ѐ' <= c <= 'ӿ' for c in text):
            return 'ru'
        if text.isascii():
            return 'en'
        X = self._vec.transform([text])
        return self._clf.predict(X)[0]
