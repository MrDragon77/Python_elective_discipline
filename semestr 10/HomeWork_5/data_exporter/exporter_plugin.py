import numpy as np


class ExporterBase:
    _registry = {}

    def __init_subclass__(cls, ext=None, **kw):
        super().__init_subclass__(**kw)
        if ext:
            ExporterBase._registry[ext] = cls

    def export(self, image, path):
        raise NotImplementedError

    @classmethod
    def get_plugin(cls, ext):
        plugin_cls = cls._registry.get(ext)
        if not plugin_cls:
            raise ValueError(f"Unknown export format: {ext}")
        return plugin_cls()
