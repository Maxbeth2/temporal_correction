from utils.act_fx_iter import ActFxs
import numpy as np
from utils.nw_utils import norm_w, np_vec, vec_np
from utils.draw_utils import _draw_axis, AXIS_COLORS, FULL_REV
from vpython import cylinder, arrow, vec, color, curve, keysdown
from abc import ABC, abstractmethod


class IsoLayer(ABC):
    def __init__(self, dim):
        
        self.dim = dim
        self.af = ActFxs()

        self.Zf_tm1 = np.zeros(shape=(dim,1))
        self.Y_tm1 = np.zeros(shape=(dim,1))

        self.V = np.random.laplace(loc=0, scale=0.5, size=(dim,dim))
        norm_w(self.V)
        ## O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-
        self.Z = np.random.laplace(loc=0, scale=0.5, size=(dim,1))
        ## O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-
        self.Zf = np.zeros(shape=(dim,1))
        self.Y = np.zeros(shape=(dim,1))
        self.d = np.zeros(shape=(dim,1))
        self.ev = np.zeros(shape=(dim,1))

        self.V_cont = np.zeros(shape=(dim,1))

        self.updating = False

    def clamp(self, X):
        self.Z = X
        

    def integrate(self):
        self.V_cont = np.dot(self.V, self.Y_tm1) #/ 2 # makes
        np.dot(self.V, self.Y_tm1, out=self.Z)
    
    def activate(self):
        self.Zf = self.af.run(self.Z)

    # @abstractmethod
    def correct(self):
        pass

    # @abstractmethod
    def update(self):
        pass
    


    # ? RENDERING FUNCTIONS
    # ? RENDERING FUNCTIONS
    # ? RENDERING FUNCTIONS
    # ? RENDERING FUNCTIONS


    def _init_render_info(self, pos):
        self.pos = pos

        print("Initializing render")
        _draw_axis(pos=pos)
        # Vectors
        self.pilot_index = 0
        self.pilot = np.ones((self.dim,1))
        self.R_pilot = arrow(pos=pos, shaftwidth=0.02, color=color.white, axis=vec(1,0,0), emissive=True, opacity=0.5)
        self.R_pilot__ = curve(color=color.white)
        
        self.R_V_cont = arrow(pos=pos, shaftwidth=0.02, color=color.orange, axis=vec(1,0,0), emissive=True)
        
        self.R_Z = arrow(pos=pos, shaftwidth=0.02, color=color.yellow, axis=vec(1,0,0), emissive=True)
        self.R_Zneg = cylinder(pos=pos, size=vec(1,.02,.02), color=vec(1,0.5,0.5), axis=vec(1,0,0), emissive=True)


        self.R_Zf = cylinder(pos=pos, size=vec(1,.01,.01), color=color.cyan, axis=vec(1,0,0), visible=False)
        
        self.R_Y = cylinder(pos=pos, size=vec(1,.01,.01), color=color.magenta, axis=vec(2,2,5), visible=False)


        self.R_Z__ = curve(color=color.yellow)
        self.R_Zf__ = curve(color=color.cyan)
        self.R_Y__ = curve(color=color.purple)


        self.R_V = []
        for m in range(self.dim):
            self.R_V.append(curve(color=color.orange, pos=[pos, vec(0,0,0), vec(0,0,0)], radius=0.01, visible=False))

        for m, crv in enumerate(self.R_V):
            crv : curve
            crv.modify(0, radius=0.003)
            crv.modify(2, radius=0.004)
        
        



    def render_self(self):

        self.R_pilot.axis = np_vec(self.pilot, dim=self.Z.shape[0])

        self.R_Z.axis = np_vec(self.Z, dim=self.Z.shape[0])
        self.R_Z__.append(np_vec(self.Z, self.dim)+self.pos)
        if self.R_Z__.npoints > FULL_REV:
            self.R_Z__.pop(0)
        self.R_V_cont.axis = np_vec(self.V_cont, dim=self.Z.shape[0])
        self.R_Zneg.axis = np_vec(-self.Z, dim=self.Z.shape[0])
        self.R_Zf.axis = np_vec(self.Zf, dim=self.Zf.shape[0])
        self.R_Y.axis = np_vec(self.Y, dim=self.Y.shape[0])
        self.R_Y__.append(np_vec(self.Y, self.dim)+self.pos)
        if self.R_Y__.npoints > FULL_REV:
            self.R_Y__.pop(0)



        proj = np.dot(self.V, self.Z) # dim magnitudes
        if np.linalg.norm(self.Z) == 0:
            Znorm = np.ones_like(self.Z)
        else:
            Znorm = self.Z / np.linalg.norm(self.Z) # one direction
        projs = []
        for j in range(self.dim):
            zd = Znorm * proj[j,0]
            projs.append(zd)
    
        for m, crv in enumerate(self.R_V):
            crv : curve
            crv.modify(1, pos=np_vec(self.V[m], dim=self.dim)+self.pos)
            # #let this be the projection of Vm on Zf on Vm
            crv.modify(2, pos=np_vec(projs[m], dim=self.dim)+self.pos, color=AXIS_COLORS[m])


    def paint_trajectory(self, x=None, A=None):
        self.R_pilot__.clear()
        length = 15
        transformed_point = np.copy(self.pilot)
        self.R_pilot__.append(np_vec(transformed_point, dim=self.pilot.shape[0])+self.pos)
        
        for _ in range(length):
            print(transformed_point.shape)
            transformed_point = np.dot(self.V, transformed_point)
            self.R_pilot__.append(np_vec(transformed_point, dim=self.pilot.shape[0])+self.pos)
        
        self.R_pilot__.modify(0, color=color.blue, diameter=0.05)




    def _b_Z_invis(self):
        self.R_Z.visible = not self.R_Z.visible
        self.R_Z__.visible = self.R_Z.visible
        self.R_Zneg.visible = self.R_Z.visible

    def _b_V_invis(self):
        for crv in self.R_V:
            crv : curve
            crv.visible = not crv.visible

    def _c_steer_pilot(self, axis='x', dir=1):
        
        self.paint_trajectory()
        if 'right' in keysdown():
            self.pilot = vec_np(self.R_Z__.point(self.pilot_index)['pos'], dim=self.dim).T
            # print(self.R_Z__.point(self.pilot_index)['pos'].x)
