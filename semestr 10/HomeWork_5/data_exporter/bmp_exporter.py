import cv2
from .exporter_plugin import ExporterBase


class BmpExporter(ExporterBase, ext='bmp'):
    def export(self, image, path):
        out = path if path.lower().endswith('.bmp') else path + '.bmp'
        return cv2.imwrite(out, image)
