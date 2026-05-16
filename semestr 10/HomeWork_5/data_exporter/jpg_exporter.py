from pathlib import Path
import cv2
import numpy as np
from .exporter_plugin import ExporterBase


class JpgExporter(ExporterBase, ext='jpg'):
    def export(self, image: np.ndarray, path: str) -> bool:
        ext = Path(path).suffix.lower()
        out = path if ext in ('.jpg', '.jpeg') else path + '.jpg'
        return cv2.imwrite(out, image, [cv2.IMWRITE_JPEG_QUALITY, 95])
