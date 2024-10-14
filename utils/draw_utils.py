from vpython import color, vec, cylinder

FULL_REV = 360

AXIS_COLORS = {0:color.red, 1:color.green, 2:color.blue}

KB_ROW_1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o','p']

KB_ROW_2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']

def _draw_axis(pos=vec(0,0,0)):
    cylinder(pos=pos, size=vec(1,.01,.01), color=AXIS_COLORS[0], axis=vec(1,0,0), opacity=0.3, emissive=True)
    cylinder(pos=pos, size=vec(1,.01,.01), color=AXIS_COLORS[1], axis=vec(0,1,0), opacity=0.3, emissive=True)
    cylinder(pos=pos, size=vec(1,.01,.01), color=AXIS_COLORS[2], axis=vec(0,0,1), opacity=0.3, emissive=True)

