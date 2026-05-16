import numpy as np
from .optimizer import OptimMeta

class NesterovOptim(OptimMeta, format_name = 'Nesterov'): 
    def __iter__(self):
        return self
    
    def set_parameters(self, f_grad, x_start, lr=0.01,eps=1e-8, n_iterations=500,**kwargs):
        self.x = x_start.copy()
        self.v = np.zeros_like(self.x)
        self.f_grad = f_grad
        self.cur_iter = 0
        self.n_iter = n_iterations
        self.eps = eps
        self.lr = lr
        if 'mu' in kwargs:
            self.mu = kwargs['mu']
        else:
            self.mu = 0.9
        return self
    
    def __next__(self):
        grad = self.f_grad(self.x + self.mu * self.v) 
        if abs(grad) > self.eps and self.cur_iter < self.n_iter:
            self.cur_iter += 1
            self.v = self.mu * self.v - self.lr * grad
            self.x = self.x + self.v
            return self.x
        raise StopIteration
