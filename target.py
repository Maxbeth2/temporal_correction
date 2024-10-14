import numpy as np
import random as r

from utils.nw_utils import np_vec

from math import pi, cos, sin

from vpython import cylinder, arrow, curve, vec, color




class Target:
    def __init__(self, speed_r_s=(pi/180)):
        self.phase = 0
        self.vec = np.random.laplace(loc=0, scale=0.5, size=(3,1))
        self.set_speed(speed_r_s)

    def set_speed(self, speed_r_s):
        self.speed = speed_r_s
        self.rot_mat = np.array([[cos(speed_r_s), -sin(speed_r_s), 0],
                                 [sin(speed_r_s), cos(speed_r_s), 0],
                                 [0, 0, 1]])
        
    def rotate(self):
        self.vec = np.dot(self.rot_mat, self.vec)
    
    def beat(self, noise_mag=0):
        self.phase += self.speed
        self.phase %= (2*pi)
        self.vec = np.array([[sin(self.phase)],
                             [cos(self.phase)],
                             [0]])
        self.vec += np.array([[sin(self.phase*3)],
                             [0],
                             [0]])
        self.vec += np.array([  [r.random()*noise_mag],
                                [r.random()*noise_mag],
                                [0]])
        
        self.vec *= 0.2
        

from utils.act_fx_iter import ActFxs
from utils.nw_utils import norm_w







#########################

#########################
#########################
#########################
##########
##########
####################
##########
##############################












#########################
####################

##################################################


#########################


#########################

############################################################

#########################














#####INPUT
#####
##############################
#####
###################################
#####
#########################
#####
##############################
#####
















































class Network:
    def __init__(self, seed=68, solved=False, hdim=2):
        self.hdim = hdim
        self.af = ActFxs()
        np.random.seed(seed=seed)

         # learnable params
        self.W = np.random.laplace(loc=0, scale=0.5, size=(2,hdim)) # prediction
        self.V = np.random.laplace(loc=0, scale=0.5, size=(hdim,hdim)) # transition of latent state
        speed_r_s=(pi/180)
        if solved:
            self.W = np.array([[cos(speed_r_s), -sin(speed_r_s)],
                                    [sin(speed_r_s), cos(speed_r_s)]])
            self.V = np.array([[cos(speed_r_s), -sin(speed_r_s)],
                                    [sin(speed_r_s), cos(speed_r_s)]])
        self.M = np.random.laplace(loc=0, scale=0.5, size=(hdim,2)) # transition of latent state given obs

        norm_w(self.V)
        norm_w(self.W)
        norm_w(self.M)

        self.dM = np.zeros_like(self.M)
        self.dV = np.zeros_like(self.V)
        self.dW = np.zeros_like(self.W)
        # what would have been a better transition?????
        #NOTE better transition determined by ev
        # Y_tm1 should have transitioned into Y rather than Zf

        # latent var
        self.Zf_tm1 = np.random.laplace(loc=0, scale=0.5, size=(hdim,1))
        self.Z = np.copy(self.Zf_tm1)
        self.Zf = np.copy(self.Z)
        # prediction
        self.x_mu = np.random.laplace(loc=0, scale=0.5, size=(2,1))

        # error computation
        self.e = np.random.laplace(loc=0, scale=0.5, size=(2,1))
        self.d = np.random.laplace(loc=0, scale=0.5, size=(hdim,1))
        self.ev = np.random.laplace(loc=0, scale=0.5, size=(hdim,1))
        # corrected state
        self.Y = np.copy(self.Z)
        self.Y_tm1 = np.copy(self.Z)
        self.x_obs = np.zeros(shape=(2,1))

        self.FB = False
       

        # Z transition
        # Z is a function of its past. It transitions following a transition matrix V
        # if V is the identity matrix, it stays the same
        # if V is a scaling matrix, it will decay or grow exponentially
        # if V is a rotational matrix, Z will oscillate around an origin

        # Z could be limited by some activation function or be normalized
    def reinit__(self, seed=68, solved=False, hdim=2):
        self.__init__(seed=seed, solved=solved, hdim=hdim)

    def run(self, target):
        # store prev state
        self.Zf_tm1 = self.Zf
        self.Y_tm1 = self.Y


        #transition
        # self.Z = np.dot(self.V, self.Y)
        if self.FB:
            self.Z = np.add(np.dot(self.V, self.Y), np.dot(self.M, self.x_mu))
        else: 
            self.Z = np.add(np.dot(self.V, self.Y)*2.0, np.dot(self.M, self.x_obs)*.2) / (self.hdim-1)
        self.Zf = self.af.run(self.Z)

        # was the transition good?
        self.x_mu = np.dot(self.W, self.Zf)
        self.e = np.subtract(target, self.x_mu) # yes/no

        if self.FB:
            self.e = np.zeros((2,1))

        # correct the state
        self.d = np.dot(self.W.T, self.e) * 0.1
        self.Y = self.af.run(np.add(self.Z, self.d))
        self.ev = np.subtract(self.Y, self.Zf_tm1)
        # Zf_tm1 should have transitioned to Y
        # take the error and use it to update V

        self.dM = np.outer(self.ev, self.x_obs)
        if self.FB:
            self.dM = np.zeros_like(self.dM)
        self.dV = np.outer(self.ev, self.Y_tm1)
        # next time Zf_tm1 is the state, it should transition to
        # something more alike to Y
        self.V += self.dV * 0.01
        self.M += self.dM * 0.01

        self.dW = np.outer(self.e, self.Zf)
        self.W += self.dW * 0.01

        self.x_obs = target

        norm_w(self.V)
        norm_w(self.W)
        norm_w(self.M)
