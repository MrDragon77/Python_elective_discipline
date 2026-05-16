import os
import csv
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

PATCH_SIZE = 16
DARK_THRESHOLD = 180
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'hw2', 'my_blood_dataset')


def load_dataset(data_dir):
    labels_path = os.path.join(data_dir, 'labels.csv')
    images, counts = [], []
    with open(labels_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_path = os.path.join(data_dir, row['filename'])
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
                counts.append(int(row['cell_count']))
    return images, counts


#BloodImage : изображение маска крови в виде бинарных патчей
class BloodImage:
    def __init__(self, img, pred_count=None):
        self._img = img
        self.pred_count = pred_count
        self._patch_bits = self._compute_patch_bits()
        self.dark_count = int(self._patch_bits.sum())

    def _compute_patch_bits(self):
        gray = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        H, W = gray.shape
        ps = PATCH_SIZE
        rows, cols = H // ps, W // ps
        bits = [
            1 if gray[r*ps:(r+1)*ps, c*ps:(c+1)*ps].mean() < DARK_THRESHOLD else 0
            for r in range(rows) for c in range(cols)
        ]
        return np.array(bits, dtype=np.uint8)

    def get_features(self):
        return self._patch_bits.astype(np.float32)

    def __str__(self):
        return ''.join(map(str, self._patch_bits))

    def __repr__(self):
        return f'BloodImage(dark_patches={self.dark_count}, pred={self.pred_count})'

    def __gt__(self, other):
        return self.pred_count > other.pred_count

    def __lt__(self, other):
        return self.pred_count < other.pred_count

    def __eq__(self, other):
        return self.pred_count == other.pred_count


if __name__ == '__main__':
    print('Loading dataset...')
    images, counts = load_dataset(DATA_DIR)
    print(f'Loaded {len(images)} images')

    print('Extracting features...')
    blood_images = [BloodImage(img) for img in images]

    X = np.array([bi.get_features() for bi in blood_images])
    y = np.array(counts)
    print(f'Feature matrix: {X.shape}, labels range: [{y.min()}, {y.max()}]')

    # a. __str__ representation
    print(f'\na. Binary string (first image):')
    print(f'   {str(blood_images[0])}')

    X_train, X_test, y_train, y_test, bi_train, bi_test = train_test_split(
        X, y, blood_images, test_size=0.25, random_state=0
    )

    # b. Train KNN
    knn = KNeighborsRegressor(n_neighbors=10)
    knn.fit(X_train, y_train)
    y_pred = np.round(knn.predict(X_test)).astype(int)

    bi_test_pred = [BloodImage(bi._img, pred_count=int(p))
                    for bi, p in zip(bi_test, y_pred)]

    # c. MSE metrics
    errors_sq = (y_pred - y_test) ** 2
    print(f'\nc. MSE metrics:')
    print(f'   Mean MSE: {errors_sq.mean():.4f}')
    print(f'   Min  MSE: {errors_sq.min():.4f}')
    print(f'   Max  MSE: {errors_sq.max():.4f}')

    # d. Magic methods
    a, b = bi_test_pred[0], bi_test_pred[1]
    print(f'\nd. Magic methods (pred A={a.pred_count}, pred B={b.pred_count}):')
    print(f'   A > B : {a > b}')
    print(f'   A < B : {a < b}')
    print(f'   A == B: {a == b}')

    # e. % correctly predicted where dark_count != true_count
    correct_mask = (y_pred == y_test)
    correct_count = correct_mask.sum()
    print(f'\ne. Correctly predicted: {correct_count}/{len(y_test)}')
    if correct_count > 0:
        mismatch = sum(
            1 for i, ok in enumerate(correct_mask)
            if ok and bi_test_pred[i].dark_count != y_test[i]
        )
        pct = 100.0 * mismatch / correct_count
        print(f'   dark_patch_count != true_count: {mismatch}/{correct_count} = {pct:.1f}%')
    else:
        print('   No correctly predicted samples.')
