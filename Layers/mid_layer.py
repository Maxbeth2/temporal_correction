import numpy as np
from Layers.top_layer import *



class MidLayer(TopLayer):
    def __init__(self, dim, udim, bdim):
        super().__init__(self=self, dim=dim, bdim=bdim)
        self.udim = udim
        self.U = np.random.laplace(loc=0, scale=0.5, size=(dim,udim))
        self.U_cont = np.zeros_like(self.Z)

    def integrate(self, bu_in, td_in):
        super().integrate(bu_in)
        self.U_cont = np.dot(self.U, td_in)
        self.Z = np.add(self.Z, self.U_cont)

    def update(self, bu_in, td_in):
        super().update(bu_in)
        dU = np.outer(self.ev, td_in)

        if self.updating:
            self.V += dU * 0.1

        norm_w(self.U)



    def _init_render_info(self, pos):
        super()._init_render_info(pos)
        self.R_U_cont = arrow(pos=pos, shaftwidth=0.02, color=color.gray(0.5), axis=vec(1,0,0), emissive=True)
    
