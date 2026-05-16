import json
import os
import random
from pathlib import Path

import cv2
import numpy as np

from .loader_plugin import DataLoaderMeta


class JsonLoader(DataLoaderMeta, format_name='json'):
    def validate(self, filename: str) -> bool:
        p = Path(filename)
        if not p.exists():
            raise FileNotFoundError(f'File is not found: {p}')
        if p.stat().st_size == 0:
            raise ValueError(f'File is empty: {p}')
        return p.suffix.lower() == '.json'

    def load(self, filename: str) -> np.ndarray:
        if not self.validate(filename):
            return None

        with open(filename, 'r') as f:
            cfg = json.load(f)

        w, h = cfg.get('image_size', [256, 256])
        grayscale = cfg.get('color_mode', 'RGB').lower() == 'grayscale'
        num_objects = cfg.get('num_objects', 3)
        allow_overlap = cfg.get('allow_overlap', True)
        bg_path = cfg.get('background_path', '')
        obj_path = cfg.get('objects_path', '')

        canvas = self._make_canvas(bg_path, w, h)
        placed = []
        obj_files = self._find_images(obj_path)

        for _ in range(num_objects * 20):
            if len(placed) >= num_objects:
                break
            obj = self._pick_object(obj_files)
            oh, ow = obj.shape[:2]
            if ow > w or oh > h:
                obj = cv2.resize(obj, (min(ow, w // 2), min(oh, h // 2)))
                oh, ow = obj.shape[:2]
            x = random.randint(0, w - ow)
            y = random.randint(0, h - oh)
            rect = (x, y, ow, oh)
            if not allow_overlap and self._rects_overlap(rect, placed):
                continue
            self._place_object(canvas, obj, x, y)
            placed.append(rect)

        if grayscale:
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

        return canvas

    def _make_canvas(self, bg_path: str, w: int, h: int) -> np.ndarray:
        imgs = self._find_images(bg_path)
        if imgs:
            return cv2.resize(cv2.imread(random.choice(imgs)), (w, h))
        bg_color = [random.randint(180, 230) for _ in range(3)]
        return np.full((h, w, 3), bg_color, dtype=np.uint8)

    def _find_images(self, folder: str) -> list:
        if not folder or not os.path.isdir(folder):
            return []
        exts = {'.png', '.jpg', '.jpeg', '.bmp'}
        return [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if Path(f).suffix.lower() in exts
        ]

    def _pick_object(self, obj_files: list) -> np.ndarray:
        if obj_files:
            return cv2.imread(random.choice(obj_files))
        size = random.randint(20, 50)
        color = [random.randint(0, 120) for _ in range(3)]
        return np.full((size, size, 3), color, dtype=np.uint8)

    def _rects_overlap(self, rect: tuple, placed: list) -> bool:
        x, y, w, h = rect
        for px, py, pw, ph in placed:
            if x < px + pw and x + w > px and y < py + ph and y + h > py:
                return True
        return False

    def _place_object(self, canvas: np.ndarray, obj: np.ndarray, x: int, y: int) -> None:
        oh, ow = obj.shape[:2]
        if len(obj.shape) == 3:
            canvas[y:y + oh, x:x + ow] = obj
        else:
            canvas[y:y + oh, x:x + ow] = cv2.cvtColor(obj, cv2.COLOR_GRAY2BGR)
