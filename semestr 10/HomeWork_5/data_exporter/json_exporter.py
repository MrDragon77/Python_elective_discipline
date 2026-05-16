import json
import numpy as np
from .exporter_plugin import ExporterBase


class JsonExporter(ExporterBase, ext='json'):
    def export(self, image, path):
        out = path if path.lower().endswith('.json') else path + '.json'
        channels = image.shape[2] if len(image.shape) == 3 else 1
        img_3d = image if len(image.shape) == 3 else image[:, :, np.newaxis]

        stats = []
        for i in range(channels):
            ch = img_3d[:, :, i]
            stats.append({
                'ch': i,
                'mean': round(float(ch.mean()), 3),
                'std': round(float(ch.std()), 3),
                'min': int(ch.min()),
                'max': int(ch.max()),
            })

        info = {
            'shape': list(image.shape),
            'dtype': str(image.dtype),
            'channels': channels,
            'stats': stats,
        }
        with open(out, 'w') as f:
            json.dump(info, f, indent=2)
        return True
