from vpython import scene, vec, rate, Mouse, keysdown, slider, wtext, canvas
import numpy as np
scene
from target import Target
from Layers.top_layer import TopLayer
from Layers.iso_layer import IsoLayer
from Layers.mid_layer import MidLayer
from utils.nw_utils import np_vec
from controller import Controller

np.random.seed(46)

# SETUP :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
scene.width = 1200
scene.height = 700
scene.range = 1.5

scene.forward = vec(0,0,-1)

upos = vec(0,0,-1)
midpos = vec(0,0,0)
bpos = vec(0,0,1)

# SETUP :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



t = Target()


l0 = IsoLayer(dim=3)
l0._init_render_info(pos=bpos)
l1 = TopLayer(dim=3, bdim=3)
l1._init_render_info(pos=midpos)

c = Controller(layers=[l0, l1])


    


print(scene.title_anchor)

while True:
    c.control()

    # if 'v' in keysdown():
    #     scene.follow(l1.R_V_cont)
    # if 'm' in keysdown():
    #     scene.follow(l1.R_M_cont)

    if 'p' not in keysdown():
        t.beat()
        l1.integrate(l0.Z)
        old = l0.Z
        l1.predict()
        l0.clamp(t.vec)
        l1.correct(l0.Z)
        l1.update(old)
        l1.store_state()

        l0.render_self()
        l1.render_self()


