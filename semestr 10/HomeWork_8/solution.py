import os
import time
import random

import cv2
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms

SEED = 42
DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    '..', '08_lecture_cnn_classification_distance_classification', 'EuroSAT', '2750'
)
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

random.seed(SEED)
torch.manual_seed(SEED)

CLASS_NAMES = sorted(os.listdir(DATA_DIR))
CLASS_TO_IDX = {c: i for i, c in enumerate(CLASS_NAMES)}


class EuroSATDataset(Dataset):
    # EuroSAT : RGB satellite images, 10 land-use classes
    def __init__(self, paths, labels, augment=False):
        self.paths = paths
        self.labels = labels

        mean = [0.485, 0.456, 0.406]
        std  = [0.229, 0.224, 0.225]

        if augment:
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.RandomCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.RandomVerticalFlip(),
                transforms.RandomRotation(20),
                transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
                transforms.ToTensor(),
                transforms.Normalize(mean, std),
            ])
        else:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean, std),
            ])

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert('RGB')
        return self.transform(img), torch.tensor(self.labels[idx], dtype=torch.long)


def make_split(data_dir, train_ratio=0.8, seed=SEED):
    rng = random.Random(seed)
    train_paths, train_labels = [], []
    val_paths, val_labels = [], []
    for cls in sorted(os.listdir(data_dir)):
        cls_dir = os.path.join(data_dir, cls)
        files = sorted(
            os.path.join(cls_dir, f)
            for f in os.listdir(cls_dir)
            if f.lower().endswith('.jpg')
        )
        rng.shuffle(files)
        n = int(len(files) * train_ratio)
        for p in files[:n]:
            train_paths.append(p)
            train_labels.append(CLASS_TO_IDX[cls])
        for p in files[n:]:
            val_paths.append(p)
            val_labels.append(CLASS_TO_IDX[cls])
    return train_paths, train_labels, val_paths, val_labels


def train_epoch(model, loader, criterion, optimizer):
    model.train()
    losses = []
    n_correct = 0
    n_total = 0
    for imgs, labels in loader:
        imgs = imgs.to(DEVICE)
        labels = labels.to(DEVICE)
        optimizer.zero_grad()
        out = model(imgs)
        loss = criterion(out, labels)
        loss.backward()
        optimizer.step()
        losses.append(loss.item() * len(labels))
        preds = out.argmax(dim=1)
        n_correct += (preds == labels).sum().item()
        n_total += len(labels)
    return sum(losses) / n_total, n_correct / n_total


def validate(model, loader, criterion):
    model.eval()
    all_losses = []
    hits = 0
    seen = 0
    with torch.no_grad():
        for imgs, labels in loader:
            imgs = imgs.to(DEVICE)
            labels = labels.to(DEVICE)
            out = model(imgs)
            all_losses.append(criterion(out, labels).item() * len(labels))
            hits += (out.argmax(1) == labels).sum().item()
            seen += len(labels)
    return sum(all_losses) / seen, hits / seen


def make_resnet(n_classes):
    m = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    m.fc = torch.nn.Linear(m.fc.in_features, n_classes)
    return m.to(DEVICE)


def load_saved(tag):
    path = os.path.join(MODEL_DIR, f'resnet18_{tag}.pth')
    m = make_resnet(len(CLASS_NAMES))
    m.load_state_dict(torch.load(path, map_location=DEVICE))
    print(f'Loaded model from {path}')
    return m


def run_experiment(augment, n_epochs=5, batch_size=64, lr=1e-3, tag=''):
    save_path = os.path.join(MODEL_DIR, f'resnet18_{tag}.pth')

    # if model already trained — skip training, return dummy curves for display
    if os.path.exists(save_path):
        print(f'\n--- Experiment: {tag} ---')
        print(f'Model already exists at {save_path}, skipping training.')
        model = load_saved(tag)
        _, _, val_paths, val_labels = make_split(DATA_DIR)
        val_ds = EuroSATDataset(val_paths, val_labels, augment=False)
        val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)
        _, va = validate(model, val_loader, torch.nn.CrossEntropyLoss())
        print(f'val acc={va:.3f}')
        dummy = [0.0] * n_epochs
        accs = [va] * n_epochs
        return dummy, dummy, accs, accs

    train_paths, train_labels, val_paths, val_labels = make_split(DATA_DIR)

    train_ds = EuroSATDataset(train_paths, train_labels, augment=augment)
    val_ds = EuroSATDataset(val_paths, val_labels, augment=False)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)

    model = make_resnet(len(CLASS_NAMES))
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    train_losses, val_losses, train_accs, val_accs = [], [], [], []
    best_acc, best_state = 0.0, None

    print(f'\n--- Experiment: {tag} ---')
    print(f'train={len(train_ds)}  val={len(val_ds)}  device={DEVICE}')

    for epoch in range(1, n_epochs + 1):
        t0 = time.time()
        tl, ta = train_epoch(model, train_loader, criterion, optimizer)
        vl, va = validate(model, val_loader, criterion)
        elapsed = time.time() - t0

        train_losses.append(tl)
        val_losses.append(vl)
        train_accs.append(ta)
        val_accs.append(va)

        if va > best_acc:
            best_acc = va
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        print(
            f'  epoch {epoch}/{n_epochs}  '
            f'train loss={tl:.4f} acc={ta:.3f}  '
            f'val loss={vl:.4f} acc={va:.3f}  '
            f'{elapsed:.1f}s'
        )

    os.makedirs(MODEL_DIR, exist_ok=True)
    save_path = os.path.join(MODEL_DIR, f'resnet18_{tag}.pth')
    torch.save(best_state, save_path)
    print(f'best val acc={best_acc:.3f}  saved: {save_path}')

    return train_losses, val_losses, train_accs, val_accs


def save_curves(c_no_aug, c_aug, out_path='training_curves.png'):
    n = len(c_no_aug[0])
    H, W = 450, 700
    canvas = np.full((H * 2, W, 3), 250, dtype=np.uint8)

    def to_x(i, total, w=W):
        return int(40 + i / max(total - 1, 1) * (w - 60))

    def to_y(v, vmin, vmax, h, y_off=0):
        return y_off + h - 30 - int((v - vmin) / (vmax - vmin + 1e-8) * (h - 50))

    def draw_line(vals, color, vmin, vmax, y_off, h=H):
        for i in range(1, len(vals)):
            x1, x2 = to_x(i - 1, len(vals)), to_x(i, len(vals))
            y1 = to_y(vals[i - 1], vmin, vmax, h, y_off)
            y2 = to_y(vals[i],     vmin, vmax, h, y_off)
            cv2.line(canvas, (x1, y1), (x2, y2), color, 2)

    # top panel: val accuracy
    cv2.putText(canvas, 'Validation Accuracy', (W // 2 - 80, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    draw_line(c_no_aug[3], (30, 120, 200), 0, 1, 0)
    draw_line(c_aug[3],    (200, 80, 30),  0, 1, 0)
    cv2.putText(canvas, 'no augmentation', (W - 160, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (30, 120, 200), 1)
    cv2.putText(canvas, 'with augmentation', (W - 160, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (200, 80, 30), 1)
    # x-axis ticks
    for i in range(n):
        x = to_x(i, n)
        cv2.putText(canvas, str(i + 1), (x - 4, H - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (80, 80, 80), 1)
    cv2.putText(canvas, 'epoch', (W // 2 - 20, H - 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)

    # bottom panel: train loss
    cv2.putText(canvas, 'Train Loss', (W // 2 - 50, H + 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    all_losses = c_no_aug[0] + c_aug[0]
    lmin, lmax = min(all_losses), max(all_losses)
    draw_line(c_no_aug[0], (30, 120, 200), lmin, lmax, H)
    draw_line(c_aug[0],    (200, 80, 30),  lmin, lmax, H)
    for i in range(n):
        x = to_x(i, n)
        cv2.putText(canvas, str(i + 1), (x - 4, H * 2 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (80, 80, 80), 1)
    cv2.putText(canvas, 'epoch', (W // 2 - 20, H * 2 - 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)

    cv2.imwrite(out_path, canvas)
    print(f'{out_path} saved')


if __name__ == '__main__':
    print(f'Device: {DEVICE}')
    print(f'Classes ({len(CLASS_NAMES)}): {CLASS_NAMES}')

    c_no_aug = run_experiment(augment=False, n_epochs=5, batch_size=64, tag='no_aug')
    c_aug    = run_experiment(augment=True,  n_epochs=5, batch_size=64, tag='aug')

    save_curves(c_no_aug, c_aug)

    print('\nSummary:')
    print(f'no_aug : best val acc = {max(c_no_aug[3]):.3f}')
    print(f'aug    : best val acc = {max(c_aug[3]):.3f}')
