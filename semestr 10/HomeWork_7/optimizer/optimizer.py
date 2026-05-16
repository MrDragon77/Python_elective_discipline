
from abc import ABC, abstractmethod
import numpy as np

class OptimMeta(ABC):
    """Basic class-loader"""
    _registry = {}

    def __init_subclass__(cls, format_name=None, **kw):
        super().__init_subclass__(**kw)

        if format_name:
            OptimMeta._registry[format_name] = cls

    @abstractmethod
    def __next__(self, filename: str) -> np.ndarray:
        ...

    @abstractmethod
    def __iter__(self):
        ...
    @abstractmethod
    def set_parameters(self, f_grad, x_start, lr=0.01,eps=1e-8, n_iterations=500,**kwargs) -> np.ndarray:
        ...

    @classmethod
    def get_optim(cls, format_name: str):
        plugin_cls = cls._registry.get(format_name)
        if not plugin_cls:
            raise ValueError(f"Unknown optimizer: {format_name}")
        return plugin_cls()