from Layers.iso_layer import *
from utils.draw_utils import _draw_axis, AXIS_COLORS




class TopLayer(IsoLayer):
    def __init__(self, dim, bdim):
        super().__init__(dim=dim)
        self.bdim = bdim
        
        self.M = np.random.laplace(loc=0, scale=0.5, size=(dim,bdim))
        norm_w(self.M)
        
        self.W = np.random.laplace(loc=0, scale=0.5, size=(bdim,dim))
        self.xmu = np.zeros(shape=(bdim,1))
        self.E = np.random.laplace(loc=0, scale=0.5, size=(dim,bdim))
        self.e = np.zeros(shape=(bdim,1))

        self.ev = np.zeros(shape=(dim,1))
        self.ev_tm1 = np.zeros(shape=(dim,1))
        self.ev_d = np.zeros(shape=(dim,1))

        self.inp = np.zeros(shape=(bdim,1))
        self.inp_tm1 = np.zeros(shape=(bdim,1))

        
        self.M_cont = np.zeros(shape=(dim,1))
        self.mod_M = 0.5
        self.updating = True

    

    def integrate(self, bu_in):
        super().integrate()
        self.M_cont = np.dot(self.M, bu_in)
        np.add(self.Z, self.M_cont, out=self.Z)

    def predict(self):
        super().activate()
        self.xmu = np.dot(self.W, self.Zf)

    def correct(self, Z_lm1):
        self.e = np.subtract(Z_lm1, self.xmu)

        # self.d = np.dot(self.W.T, self.e) * 0.5 #TODO

        self.d = np.dot(self.E, self.e) * 0.5

        self.Y = self.af.run(
            np.add(self.Z, self.d))
        self.ev = np.subtract(self.Y, self.Zf)
        self.ev_d = self.ev - self.ev_tm1

    def update(self, bu_in):
        dV = np.outer(self.ev, self.Y_tm1)
        dM = np.outer(self.ev, bu_in)
        dW = np.outer(self.e, self.Zf)
        dE = np.outer(self.ev_d, self.e)

        if self.updating:
            self.V += dV * 0.1
            self.M += dM * 0.1
            self.W += dW * 0.1
            self.E += dE * 0.1
        
        self.M *= 0.9999
        self.W *= 0.9999
        self.V *= 0.9999
        self.E *= 0.9999

        norm_w(self.V)
        norm_w(self.M)
        norm_w(self.W)
    
    def store_state(self):
        self.Y_tm1 = self.Y
        self.Zf_tm1 = self.Zf
        self.inp_tm1 = self.inp
        self.ev_tm1 = self.ev






    # ? RENDERING FUNCTIONS
    # ? RENDERING FUNCTIONS
    # ? RENDERING FUNCTIONS
    # ? RENDERING FUNCTIONS




    def _init_render_info(self, pos):
        super()._init_render_info(pos)
        for crv in self.R_V:
            crv : curve
            crv.visible = True
        # self.R_e = cylinder(pos=pos, size=vec(1,.02,.02), color=color.red, axis=vec(1,0,0))
        self.R_e = arrow(pos=pos, shaftwidth=0.005, headwidth=0.01, color=color.red, axis=vec(1,0,0))

        self.R_M_cont = arrow(pos=pos, shaftwidth=0.02, color=color.green, axis=vec(1,0,0), emissive=True)
        self.R_inp = arrow(pos=pos, shaftwidth=0.02, color=color.cyan, axis=np_vec(self.inp, dim=self.bdim), opacity=0.5)
        self.R_inpneg = arrow(pos=pos, shaftwidth=0.02, color=color.magenta, axis=-np_vec(self.inp, dim=self.bdim), opacity=0.5)
        
        self.R_e__ = curve(color=color.red)
        
        self.R_M= []
        for m in range(self.dim):
            self.R_M.append(curve(color=color.green, pos=[pos, vec(0,0,0), vec(0,0,0)], radius=0.01))
        
        for m, crv in enumerate(self.R_M):
            crv : curve
            crv.modify(0, radius=0.003)
            crv.modify(2, radius=0.004)

        
        self.R_xmu = arrow(pos=pos, shaftwidth=0.005, headwidth=0.01, color=color.green, axis=vec(1,0,0))
        self.R_xmu__ = curve(color=color.green)

        self.projection_rods = curve(color=color.white, visible=False)

        self.clock = 0




    def render_self(self):
        """
        args are extra vectors to render
        """
        super().render_self()
        self.R_e.axis = np_vec(self.e, dim=self.e.shape[0])
        self.R_e__.append(np_vec(self.e, self.bdim)+self.pos)
        if self.R_e__.npoints > 360:
            self.R_e__.pop(0)

        
        self.R_M_cont.pos = np_vec(self.V_cont, dim=self.Z.shape[0]) + self.pos
        self.R_M_cont.axis = np_vec(self.M_cont, dim=self.Z.shape[0])
        
        self.R_inp.axis = np_vec(self.inp, dim=self.bdim)
        self.R_inpneg.axis = -np_vec(self.inp, dim=self.bdim)

        
        proj = np.dot(self.M, self.inp) # dim magnitudes
        inpnorm = self.inp / (np.linalg.norm(self.inp) + 0.0000001) # one direction
        projs = []
        for j in range(self.dim):
            id = inpnorm * proj[j,0]
            projs.append(id)

        for m, crv in enumerate(self.R_M):
            crv.modify(1, pos=np_vec(self.M[m], dim=self.bdim)+self.pos)
            crv.modify(2, pos=np_vec(projs[m], dim=self.bdim)+self.pos, color=AXIS_COLORS[m])

            # cyl.axis = np_vec(self.M[m], dim=self.bdim)
        self.render_projection()


    def render_projection(self):
        self.R_xmu.axis = np_vec(self.xmu, dim=self.bdim)
        self.R_xmu__.append(np_vec(self.xmu, self.bdim)+self.pos)
        if self.R_xmu__.npoints > 360:
            self.R_xmu__.pop(0)
        
        if self.clock % 19 == 0:
            self.clock = 0
            self.projection_rods.append(np_vec(self.Z, dim=self.dim)+self.pos)
            self.projection_rods.append(np_vec(self.xmu, dim=self.bdim)+self.pos)
            if self.projection_rods.npoints > 36:
                self.projection_rods.pop(0)
                self.projection_rods.pop(0)

        self.clock +=1


    def _b_proj_vis(self):
        self.projection_rods.visible = not self.projection_rods.visible