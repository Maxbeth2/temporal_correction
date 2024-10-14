from utils.act_fx_iter import ActFxs
import numpy as np
from utils.nw_utils import norm_w, np_vec
from utils.draw_utils import _draw_axis, AXIS_COLORS
from vpython import cylinder, arrow, vec, color, curve

class Layer:
    def __init__(self, dim, udim=0, bdim=0, pos=None):#--------------------------------------INIT

        self.udim = udim
        self.dim = dim
        self.bdim = bdim

        self.af = ActFxs()

        self.Zf_tm1 = np.zeros(shape=(dim,1))
        self.Y_tm1 = np.zeros(shape=(dim,1))
        #TODO top layer is a special case of layer which sets this to 0 and receives 0 as td input
        self.U = np.random.laplace(loc=0, scale=0.5, size=(dim,udim))
        self.V = np.random.laplace(loc=0, scale=0.5, size=(dim,dim))
        norm_w(self.V)
        ## O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-
        self.Z = np.random.laplace(loc=0, scale=0.5, size=(dim,1))
        ## O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-O-
        self.M = np.random.laplace(loc=0, scale=0.5, size=(dim,bdim))
        self.Zf = np.zeros(shape=(dim,1))
        self.Y = np.zeros(shape=(dim,1))
        self.d = np.zeros(shape=(dim,1))
        self.ev = np.zeros(shape=(dim,1))
        self.W = np.random.laplace(loc=0, scale=0.5, size=(bdim,dim))
        self.xmu = np.zeros(shape=(bdim,1))
        self.E = np.random.laplace(loc=0, scale=0.5, size=(dim,bdim))
        self.e = np.zeros(shape=(bdim,1))

        self.inp = np.zeros(shape=(bdim,1))
        self.inp_tm1 = np.zeros(shape=(bdim,1))


        if pos != None:
            self._init_render_info(pos=pos)

        self.pos = pos

        # ------------------------------------------------------------------------------
    

        self.U_cont = np.zeros(shape=(dim,1))
        self.V_cont = np.zeros(shape=(dim,1))
        self.M_cont = np.zeros(shape=(dim,1))

        self.mod_M = 0.5
        self.updating = True
    
    

    def infer_predict(self, bu_in, td_in):
        """
        bu_in is typically Y_tm1 of Z_lm1
        td_in is typically Y_tm1 of Z_lp1
        """

        self.U_cont = np.dot(self.U, td_in)
        self.V_cont = np.dot(self.V, self.Y_tm1)
        self.M_cont = np.dot(self.M, bu_in) * self.mod_M
        self.Z = np.add(
            np.add(
            self.U_cont,
            self.V_cont
            ),
            self.M_cont
        )
    
        self.Zf = self.af.run(self.Z)

        self.xmu = np.dot(self.W, self.Zf)

    def correct(self, Z_lm1):
        self.e = np.subtract(Z_lm1, self.xmu)

        self.d = np.dot(self.W.T, self.e) * 0.5 #TODO
        self.Y = self.af.run(
            np.add(self.Z, self.d))
        self.ev = np.subtract(self.Y, self.Zf)

    def update(self, bu_in, td_in):
        dU = np.outer(self.ev, td_in)
        dV = np.outer(self.ev, self.Y_tm1)
        dM = np.outer(self.ev, bu_in)
        dW = np.outer(self.e, self.Zf)

        if self.updating:
            self.U += dU * 0.1
            self.V += dV * 0.1
            self.M += dM * 0.1
            self.W += dW * 0.1

        norm_w(self.U)
        norm_w(self.V)
        norm_w(self.M)
        norm_w(self.W)

    def store_state(self):
        self.Y_tm1 = self.Y
        self.Zf_tm1 = self.Zf
        self.inp_tm1 = self.inp













    def _init_render_info(self, pos):
        print("Initializing render")
        _draw_axis(pos=pos)
        # Vectors

        self.R_e = cylinder(pos=pos, size=vec(1,0.01,0.01), color=color.red, axis=vec(1,0,0))
        self.R_Z = arrow(pos=pos, shaftwidth=0.01, color=color.yellow, axis=vec(1,0,0), emissive=False)
        self.R_U_cont = arrow(pos=pos, shaftwidth=0.01, color=color.gray(0.5), axis=vec(1,0,0), emissive=True)
        self.R_V_cont = arrow(pos=pos, shaftwidth=0.01, color=color.orange, axis=vec(1,0,0), emissive=True)
        self.R_M_cont = arrow(pos=pos, shaftwidth=0.01, color=color.green, axis=vec(1,0,0), emissive=True)
        self.R_Zneg = cylinder(pos=pos, size=vec(1,0.01,0.01), color=vec(1,0.5,0.5), axis=vec(1,0,0), emissive=True)
        self.R_Zf = cylinder(pos=pos, size=vec(1,0.01,0.01), color=color.red, axis=vec(1,0,0))
        self.R_Y = cylinder(pos=pos, size=vec(1,0.01,0.01), color=color.cyan, axis=vec(2,2,5))
        self.R_inp = arrow(pos=pos, shaftwidth=0.01, color=color.cyan, axis=np_vec(self.inp, dim=self.bdim), opacity=0.5)
        self.R_inpneg = arrow(pos=pos, shaftwidth=0.01, color=color.magenta, axis=-np_vec(self.inp, dim=self.bdim), opacity=0.5)

        self.R_e__ = curve(color=color.red)
        self.R_Z__ = curve(color=color.yellow)
        self.R_Zf__ = curve(color=color.cyan)
        self.R_Y__ = curve(color=color.cyan)

        #^ Matrices
        self.R_V = []
        for m in range(self.dim):
            self.R_V.append(curve(color=color.orange, pos=[pos, vec(0,0,0), vec(0,0,0)], radius=0.003))
        self.R_M= []
        for m in range(self.dim):
            self.R_M.append(curve(color=color.green, pos=[pos, vec(0,0,0), vec(0,0,0)], radius=0.003))
        self.R_U= []
        for m in range(self.dim):
            self.R_U.append(curve(color=color.gray(0.5), pos=[pos, vec(0,0,0), vec(0,0,0)], radius=0.003))



    def render_self(self, *args):
        """
        kwargs are extra vectors to render
        """
        self.R_e.axis = np_vec(self.e, dim=self.e.shape[0])
        self.R_e__.append(np_vec(self.e, self.bdim)+self.pos)
        if self.R_e__.npoints > 360:
            self.R_e__.pop(0)
        self.R_Z.axis = np_vec(self.Z, dim=self.Z.shape[0])
        self.R_Z__.append(np_vec(self.Z, self.dim)+self.pos)
        if self.R_Z__.npoints > 360:
            self.R_Z__.pop(0)
        self.R_U_cont.axis = np_vec(self.U_cont, dim=self.Z.shape[0])
        self.R_V_cont.pos = np_vec(self.U_cont, dim=self.Z.shape[0]) + self.pos
        self.R_V_cont.axis = np_vec(self.V_cont, dim=self.Z.shape[0])
        self.R_M_cont.pos = np_vec(self.V_cont, dim=self.Z.shape[0]) + np_vec(self.U_cont, dim=self.Z.shape[0])
        self.R_M_cont.axis = np_vec(self.M_cont, dim=self.Z.shape[0])
        
        self.R_Zneg.axis = np_vec(-self.Z, dim=self.Z.shape[0])
        self.R_Zf.axis = np_vec(self.Zf, dim=self.Zf.shape[0])
        self.R_Y.axis = np_vec(self.Y, dim=self.Y.shape[0])

        self.R_inp.axis = np_vec(self.inp, dim=self.bdim)
        self.R_inpneg.axis = -np_vec(self.inp, dim=self.bdim)

        proj = np.dot(self.V, self.Z) # dim magnitudes
        Znorm = self.Z / np.linalg.norm(self.Z) # one direction
        projs = []
        for j in range(self.dim):
            zd = Znorm * proj[j,0]
            projs.append(zd)
        


        for m, crv in enumerate(self.R_V):
            crv : curve
            crv.modify(1, pos=np_vec(self.V[m], dim=self.dim))
            # #let this be the projection of Vm on Zf on Vm
            crv.modify(2, pos=np_vec(projs[m], dim=self.dim), color=AXIS_COLORS[m])

        proj = np.dot(self.M, self.inp) # dim magnitudes
        inpnorm = self.inp / (np.linalg.norm(self.inp) +0.000001)# one direction
        projs = []
        for j in range(self.dim):
            id = inpnorm * proj[j,0]
            projs.append(id)

        for m, crv in enumerate(self.R_M):
            crv.modify(1, pos=np_vec(self.M[m], dim=self.bdim)+self.pos)
            crv.modify(2, pos=np_vec(projs[m], dim=self.bdim)+self.pos, color=AXIS_COLORS[m])
            # cyl.axis = np_vec(self.M[m], dim=self.bdim)

        for m, cyl in enumerate(self.R_U):
            cyl.axis = np_vec(self.U[m], dim=self.udim)