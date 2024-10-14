import pygame as pg
import pygame_textinput
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import ButtonArray, Button

import time as t
import math as m
import numpy as np
from multiprocessing.connection import Pipe
from utils.nw_utils import *
from processes.plot_var import PlotVar
from target import Network, Target


if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((1200,900), display=0)

    surface_0 = pg.Surface((600,600))
    surface_1 = pg.Surface((600,600))


    pg.font.init()
    font = pg.font.Font('freesansbold.ttf', 13)

    textinput = pygame_textinput.TextInputVisualizer()
    textinput.cursor_width = 12
    textinput.value = "seed:13"
    textinput.font_color = (255,255,255)
    textinput.cursor_color = (200,255,200)

    slider = Slider(screen, 50, 700, 500, 20, min=1, max=65, step=1)
    slider.value = 65

    clock = pg.time.Clock()

    wx, wy = pg.display.get_window_size()
    _C = np.array([[wx/2, wy/2]])


    JUMP = 1


    ## INITIALIZE NETWORK

    Nw = Network(solved=False,hdim=2)
    T = Target()


    ## BOOLS ------------------
    ## ------------------------
    global updating, normalizing_w, spinning, manual_y
    updating = True
    normalizing_x = True
    normalizing_w = True
    spinning = True
    running = True
    manual_y = False

    def switch_u():
        global updating
        updating = not updating
    def switch_w():
        global normalizing_w
        normalizing_w = not normalizing_w
    def switch_s():
        global spinning
        spinning = not spinning

    def switch_y():
        global manual_y
        manual_y = not manual_y

    

    bbarr = ButtonArray(
        screen,
        150,
        50,
        400,
        50,
        (3,1),
        border=10,
        texts=('Update','normW','Spin'),
        onClicks=(lambda: switch_u(),
                  lambda: switch_w(),  
                  lambda: switch_s()
                  )
    )

    global plot, snd, rec
    snd, rec = Pipe()
    plot = PlotVar(rec)
    plot.start()


    def launch_plot():
        global plot, snd, rec
        if plot != None:
            plot.terminate()
        snd.close()
        rec.close()
        snd, rec = Pipe()
        plot = PlotVar(rec)
        plot.start()

    bb = Button(screen, 100, 100, 100, 50, False, 
                onClick= lambda: launch_plot())
    # ------------------------
    theta = m.pi/60

    def draw_text(text, center):
        t = font.render(text, True, (255,255,255), None)
        tr = t.get_rect()
        tr.center = center
        screen.blit(t, tr)

    def render_info():
        draw_text(text=f"U, Updating: {updating}",
                center=(65,60))
        draw_text(text=f"S, Spinning: {spinning}",
                center=(65,80))
        draw_text(text=f"W, NormW: {normalizing_w}",
                center=(55,120))
        draw_text(text=f"E, E mag: {round(np.linalg.norm(Nw.e),4)}",
                center=(55,140))
        
        # draw_text(text=f"Det_w: {round(np.linalg.det(Nw.W),4)}",
        #         center=(700,100))
        
    def draw_network(screen, net : Network):
        wx0, wy0 = screen.get_size()
        _Ct = np.array([[wx0/2, wy0/2]])
        pg.draw.circle(screen, (200,200,200), d_v(_Ct), radius=250, width=3)
        

        # M
        pg.draw.line(screen, (50,200,50), 
                    start_pos=d_v(_Ct), 
                    end_pos=d_v(_Ct+t_v(net.M[0,0:2])), 
                    width=5)
        pg.draw.line(screen, (50,250,50), 
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(net.M[1,0:2])), 
                    width=5)
        # dM
        pg.draw.line(screen, (100,200,100), 
                    start_pos=d_v(_Ct+t_v(net.M[0,0:2])),
                    end_pos=d_v(_Ct+t_v(net.M[0,0:2] + net.dM[0,0:2] * 3)),
                    width=5)
        pg.draw.line(screen, (100,250,120), 
                    start_pos=d_v(_Ct+t_v(net.M[1,0:2])), 
                    end_pos=d_v(_Ct+t_v(net.M[1,0:2] + net.dM[1,0:2] * 3)),
                    width=5)
        # V
        pg.draw.line(screen, (200,100,100), 
                    start_pos=d_v(_Ct), 
                    end_pos=d_v(_Ct+t_v(net.V[0,0:2])), 
                    width=5)
        pg.draw.line(screen, (250,150,150), 
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(net.V[1,0:2])), 
                    width=5)
        # dV
        pg.draw.line(screen, (200,100,200), 
                    start_pos=d_v(_Ct+t_v(net.V[0,0:2])), 
                    end_pos=d_v(_Ct+t_v(net.V[0,0:2] + net.dV[0,0:2] * 3)), 
                    width=5)
        pg.draw.line(screen, (200,100,200),
                    start_pos=d_v(_Ct+t_v(net.V[1,0:2])),
                    end_pos=d_v(_Ct+t_v(net.V[1,0:2] + net.dV[1,0:2] * 3)), 
                    width=5)
        
        # W
        pg.draw.line(screen, (100,100,100),
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(net.W[0,0:2])),
                    width=3)
        pg.draw.line(screen, (150,150,150),
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(net.W[1,0:2])),
                    width=3)
        
        # dW
        pg.draw.line(screen, (100,100,200),
                    start_pos=d_v(_Ct+t_v(net.W[0,0:2])),
                    end_pos=d_v(_Ct+t_v(net.W[0,0:2] + net.dW[0,0:2] * 3)),
                    width=5)
        pg.draw.line(screen, (100,100,200),
                    start_pos=d_v(_Ct+t_v(Nw.W[1,0:2])),
                    end_pos=d_v(_Ct+t_v(net.W[1,0:2] + net.dW[1,0:2] * 3)),
                    width=5)
        
        # # WT
        # pg.draw.line(screen, (150,150,200),
        #             start_pos=d_v(_Ct), 
        #             end_pos=d_v(_Ct+t_v(Nw.W.T[0])), 
        #             width=3)
        # pg.draw.line(screen, (100,100,200), 
        #             start_pos=d_v(_Ct), 
        #             end_pos=d_v(_Ct+t_v(Nw.W.T[1])), 
        #             width=3)

        
        
        # target
        pg.draw.line(screen, (0,200,200),
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(T.vec)),
                    width=5)

        # Z
        pg.draw.line(screen, (200,200,0), 
                    start_pos=d_v(_Ct), 
                    end_pos=d_v(_Ct+t_v(Nw.Z[0:2])),
                    width=7)
        pg.draw.line(screen, (200,150, 150),
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(-Nw.Z[0:2])),
                    width=5)
        pg.draw.line(screen, (200,0,200),
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(Nw.Zf[0:2])),
                    width=3)
        
        # Y
        pg.draw.line(screen, (200,250, 250),
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(Nw.Y[0:2])),
                    width=5)
        # err_v
        pg.draw.line(screen, (250,200,80),
                    start_pos=d_v(_Ct),
                    end_pos=d_v(_Ct+t_v(Nw.ev[0:2])),
                    width=5)
        # d
        pg.draw.line(screen, (200,100,200),
                    start_pos=d_v(_Ct+t_v(Nw.Zf[0:2])),
                    end_pos=d_v(_Ct+t_v(Nw.Zf[0:2])+t_v(Nw.d[0:2])),
                    width=3)
        
        # error
        pg.draw.line(screen, (200,0,0), 
                    start_pos=d_v(_Ct), 
                    end_pos=d_v(_Ct+t_v(Nw.e[0:2])), 
                    width=3)
        
        # x_mu
        pg.draw.line(screen, (50,250,50), 
                    start_pos=d_v(_Ct), 
                    end_pos=d_v(_Ct+t_v(Nw.x_mu[0:2])), 
                    width=2)



    while running:
        t.sleep(1/m.pow(slider.value,2))
        screen.fill((0,0,0))
        surface_0.fill((0,0,50))
        surface_1.fill((0,50,0))
        
        events = pg.event.get()
        screen.blit(textinput.surface, (100, 600))
        pygame_widgets.update(events)

        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if pg.key.get_mods() & pg.KMOD_CTRL:
                    if event.key == pg.K_w:
                        normalizing_w = not normalizing_w
                    if event.key == pg.K_f:
                        Nw.FB = not Nw.FB
                    if event.key == pg.K_u:
                        updating = not updating
                    if event.key == pg.K_j:
                        if JUMP == 1:
                            JUMP = 0
                        elif JUMP == 0:
                            JUMP = 1
                    if event.key == pg.K_s:
                        spinning = not spinning
                    if event.key == pg.K_y:
                        manual_y = not manual_y


                    if event.key == pg.K_e:
                        plot.terminate()
                        snd.close()
                        rec.close()
                        snd, rec = Pipe()
                        plot = PlotVar(rec)
                        plot.start()
                        
                        

                    if event.key == pg.K_SPACE:
                        try:
                            seedstr = textinput.value.split(":")[1]
                            seed = int(seedstr)
                        except:
                            seed = 123
                else:
                    textinput.update(events)


        draw_network(surface_0, net=Nw)
        draw_network(surface_1, net=Nw)
        screen.blit(surface_0, (0,0))
        screen.blit(surface_1, (600,0))
        render_info()

        beta = 0.5
        for _ in range(JUMP):
            if spinning:
                T.beat()
            Nw.run(T.vec)


            dic = {
                "err_mag": np.linalg.norm(Nw.e),
                "Z_mag": np.linalg.norm(Nw.Z),
                "dWx_mag": np.linalg.norm(Nw.dW[0]),
                "dWy_mag": np.linalg.norm(Nw.dW[1]),
            }


            if plot.is_alive:
                snd.send(dic)
            
            JUMP = 1

        
        clock.tick()
        pg.display.update()