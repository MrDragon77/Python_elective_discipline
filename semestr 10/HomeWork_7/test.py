import optimizer 
import importlib
import pkgutil
import math
import numpy as np

_discovered = False
class PreProcessing:

    @staticmethod
    def autodiscover_plugins() -> None:
        global _discovered
        if _discovered:
            return

        for m in pkgutil.iter_modules(optimizer.__path__):
            if m.name.startswith("_"): 
                continue
            importlib.import_module(f"{optimizer.__name__}.{m.name}")
        _discovered = True

if __name__=="__main__":
    
    PreProcessing.autodiscover_plugins()
    #print(optimizer.optimizer.OptimMeta._registry.keys())
    opt = optimizer.optimizer.OptimMeta.get_optim("Nesterov")
    
    # f(x) = sin(x)
    f_grad = lambda x: math.cos(x)
    n_iter = 10
    x = np.array([5.0])
    opt.set_parameters(f_grad, x, lr=0.01,eps=1e-8, n_iterations=500, beta = 0.9, beta2 =0.999)
    best_x = x
    for i in iter(opt):
        best_x = i
    print(best_x)
    