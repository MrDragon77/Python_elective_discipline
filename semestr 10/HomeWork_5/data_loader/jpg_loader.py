from pathlib import Path
import numpy as np
import cv2
from .loader_plugin import DataLoaderMeta

class JPGLoader(DataLoaderMeta, format_name = 'jpg'):
    #format_name = '.png'
    def validate(self, filename: str) -> bool:
        p = Path(filename)
        if not p.exists():
            raise FileNotFoundError(f'File is not found: {p}')
        if p.stat().st_size == 0:
            raise ValueError(f'File is empty: {p}')

        ext = p.suffix.lower()

        if ext == ".jpg" or ext == '.jpeg':
            return True
        return False

    def load(self, filename: str) -> np.ndarray:
        if self.validate(filename):
            return cv2.imread(filename)

        return None

if __name__=="__main__":
    plugin = DataLoaderMeta.get_plugin('png')
    #print(DataLoaderPlugin._registry.keys())

    data = plugin.load('./data/COVID-1.png')
    print(type(data))
