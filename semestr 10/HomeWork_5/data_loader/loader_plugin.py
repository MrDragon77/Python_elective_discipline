from abc import ABC, abstractmethod
import numpy as np

class DataLoaderMeta(ABC):
    """Basic class-loader"""
    _registry = {}

    def __init_subclass__(cls, format_name=None, **kw):
        super().__init_subclass__(**kw)

        if format_name:
            DataLoaderMeta._registry[format_name] = cls

    @abstractmethod
    def load(self, filename: str) -> np.ndarray:
        """Data loading"""
        ...

    @abstractmethod
    def validate(self, filename: str) -> bool:
        """Check input data"""
        ...

    @classmethod
    def get_plugin(cls, format_name: str):
        plugin_cls = cls._registry.get(format_name)
        if not plugin_cls:
            raise ValueError(f"Unknown format: {format_name}")
        return plugin_cls()
