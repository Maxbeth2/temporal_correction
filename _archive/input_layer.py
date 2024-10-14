from utils.act_fx_iter import ActFxs
import numpy as np
from utils.nw_utils import norm_w, np_vec
from utils.draw_utils import _draw_axis, AXIS_COLORS
from vpython import cylinder, arrow, vec, color, curve

class InputLayer:
    def __init__(self, dim, udim, pos=None):
        self.dim = dim
        self.udim = udim
        self.af = ActFxs()

        self.x = np.ones(shape=(dim,1))
        self.x_tm1 = np.ones(shape=(dim,1))
        self.pos = pos
        if pos is not None:
            self._init_render_info(pos=pos)
    
    def store_state(self):
        self.x_tm1 = self.x

    def _init_render_info(self, pos):
        _draw_axis(pos)
        self.R_x = arrow(pos=pos, shaftwidth=0.01, color=color.cyan)
        self.R_x__ = curve(color=color.cyan)
        self.R_x_tm1 = arrow(pos=pos, shaftwidth=0.01, color=color.yellow)
        self.R_xmu = arrow(pos=pos, shaftwidth=0.01, color=color.green)
        self.R_e = arrow(pos=pos, shaftwidth=0.01, color=color.red)
    
    def render_self(self):
        self.R_x.axis = np_vec(self.x, dim=self.dim)
        self.R_x__.append(np_vec(self.x)+self.pos)
        if self.R_x__.npoints > 360:
            self.R_x__.pop(0)
