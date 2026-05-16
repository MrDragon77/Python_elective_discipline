import importlib
import pkgutil

import data_loader
import data_exporter
import data_processor


_discovered: dict = {}


def autodiscover(package) -> None:
    name = package.__name__
    if _discovered.get(name):
        return
    for m in pkgutil.iter_modules(package.__path__):
        if not m.name.startswith('_'):
            importlib.import_module(f'{name}.{m.name}')
    _discovered[name] = True


if __name__ == '__main__':
    import numpy as np

    # Task 1: Descriptors
    print('Task 1: Descriptors')
    from descriptors import ImageRecord, NormalizedImage, MinColorCount

    rec = ImageRecord()
    img = rec.load('./data/COVID-1.png')
    print(f'ImageRecord.load → shape={img.shape}')

    class Holder:
        data = NormalizedImage()

    h = Holder()
    h.data = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    print(f'NormalizedImage  → resized to {h.data.shape}')

    class CV:
        img = MinColorCount()

    cv_obj = CV()
    binary = np.zeros((50, 50, 3), dtype=np.uint8)
    binary[:25] = 255
    try:
        cv_obj.img = binary
        print('MinColorCount    → no error (unexpected)')
    except ValueError as e:
        print(f'MinColorCount    → ValueError: {e}')

    # Task 2a: Loaders
    print('\nTask 2a: Loaders')
    from data_loader.loader_plugin import DataLoaderMeta

    autodiscover(data_loader)
    print(f'Registered loaders: {list(DataLoaderMeta._registry.keys())}')

    img = DataLoaderMeta.get_plugin('png').load('./data/COVID-1.png')
    print(f'PNG  → shape={img.shape}')

    synth = DataLoaderMeta.get_plugin('json').load('./data/config.json')
    print(f'JSON → synthetic image shape={synth.shape}')

    # Task 2b: Processors
    print('\nTask 2b: Processors')
    from data_processor.processor_plugin import ProcessorBase

    autodiscover(data_processor)
    print(f'Registered processors: {list(ProcessorBase._registry.keys())}')

    result = ProcessorBase.get_plugin('count').process(img)
    print(f'BlobCounter  → {result["num_objects"]} object(s) found')

    knn = ProcessorBase.get_plugin('knn')
    knn.fit([img, img], ['covid', 'covid'])
    pred = knn.process(img)
    print(f'KnnClassifier → predicted label: "{pred["label"]}"')

    # Task 2c: Exporters
    print('\nTask 2c: Exporters')
    from data_exporter.exporter_plugin import ExporterBase

    autodiscover(data_exporter)
    print(f'Registered exporters: {list(ExporterBase._registry.keys())}')

    for fmt in ('png', 'jpg', 'bmp', 'json'):
        ok = ExporterBase.get_plugin(fmt).export(img, f'./data/output.{fmt}')
        print(f'{fmt.upper()} exporter → {"ok" if ok else "failed"}')
