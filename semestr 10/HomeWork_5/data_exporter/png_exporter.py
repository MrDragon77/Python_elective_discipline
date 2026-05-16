import cv2
from .exporter_plugin import ExporterBase


class PngExporter(ExporterBase, ext='png'):
    def export(self, image, path):
        out = path if path.lower().endswith('.png') else path + '.png'
        return cv2.imwrite(out, image)
