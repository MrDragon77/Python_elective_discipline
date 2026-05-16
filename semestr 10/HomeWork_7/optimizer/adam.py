
import numpy as np
from .optimizer import OptimMeta

class AdamOptim(OptimMeta, format_name = 'Adam'):
    def __iter__(self):
        return self
        
    def set_parameters(self, f_grad, x_start, lr=0.01,eps=1e-8, n_iterations=500,**kwargs):
        self.x = x_start.copy()
        self.v = np.zeros_like(self.x)
        self.m = np.zeros_like(self.x)  # Первый момент (среднее градиента)
        self.f_grad = f_grad
        self.cur_iter = 1
        self.n_iter = n_iterations+1
        self.eps = eps
        self.lr = lr
        if 'beta' in kwargs:
            self.beta = kwargs['beta']
        else:
            self.beta = 0.9
        
        if 'beta2' in kwargs:
            self.beta2 = kwargs['beta2']
        else:
            self.beta2 = 0.999
        return self
    
    def __next__(self):
        grad = self.f_grad(self.x)
        if abs(grad) > self.eps and self.cur_iter < self.n_iter:
        
            self.m = self.beta * self.m + (1 - self.beta) * grad
            self.v = self.beta2 * self.v + (1 - self.beta2) * (grad**2)
            
            m_hat = self.m / (1 - self.beta**self.cur_iter)
            v_hat = self.v / (1 - self.beta2**self.cur_iter)

            step = self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

            
            self.x -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
            
            return self.x
        raise StopIteration