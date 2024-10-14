import numpy as np
from vpython import vec, vector

def norm_w(w):
    norm_0 = np.linalg.norm(w[:,0])
    norm_1 = np.linalg.norm(w[:,1])
    if norm_0 > 1:
        w[:,0] /= norm_0
    if norm_1 > 1:
        w[:,1] /= norm_1

def t_v(vec, ):
    """
    transforms a vector to make it suitable for drawing
    """
    vec = np.reshape(vec, (2,))
    x = vec[0] * 250
    y = vec[1] * -250
    a = np.array([[x,y]])
    return a


def d_v(vec):
    """
    takes in a 2D vector and returns a tuple suitable for drawing
    """
    x = vec[0,0]
    y = vec[0,1]
    return (float(x), float(y))

def np_vec(v, dim=3):
    if dim == 2:
        v = v.reshape((2,1))
        return vec(v[0,0], v[1,0], 0)
    if dim == 3:
        v = v.reshape((3,1))
        return vec(v[0,0], v[1,0], v[2,0])
    

def vec_np(v, dim=3):
    v : vector
    if dim == 2:
        npv = np.array([[v.x, v.y]])
        return npv
    if dim == 3:
        npv = np.array([[v.x, v.y, v.z]])
        return npv
