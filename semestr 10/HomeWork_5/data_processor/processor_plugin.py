import numpy as np


class ProcessorBase:
    _registry = {}

    def __init_subclass__(cls, name=None, **kw):
        super().__init_subclass__(**kw)
        if name:
            ProcessorBase._registry[name] = cls

    def process(self, image):
        raise NotImplementedError

    @classmethod
    def get_plugin(cls, name):
        plugin_cls = cls._registry.get(name)
        if not plugin_cls:
            raise ValueError(f"Unknown processor: {name}")
        return plugin_cls()
