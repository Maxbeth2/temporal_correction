import math as m
import numpy as np
class ActFxs:
    def __init__(self):
        self.fxs = {"id": self.identity, "tanh": self.tanh, "sign": self.sign}
        self.index = 1
        self.n = len(self.fxs)
        self.key = list(self.fxs.keys())[self.index]

    def run(self, x):
        return self.fxs[self.key](x)

    def next(self):
        self.index += 1
        self.index %= self.n
        self.key = list(self.fxs.keys())[self.index]
        print(self.key)

    def select(self, name):
        pass

    def tanh(self, x):
        return np.tanh(x)
    
    def sign(self,x):
        return np.sign(x)
    
    def identity(self, x):
        return x

if __name__ == "__main__":
    af = ActFxs()
    print(af.key)
    act = af.run(np.ones((2,1)))
    print(act)
    af.next()
    act = af.run(np.ones((2,1)))
    print(act)
    af.next()
    act = af.run(np.ones((2,1)))
    print(act)


    