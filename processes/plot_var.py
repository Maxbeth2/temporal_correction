import multiprocessing as mp
from multiprocessing.connection import Pipe, Connection
import pyqtgraph as pg
from pyqtgraph import examples

# examples.run()
# exit()
from pyqtgraph.Qt import QtCore

class PlotVar(mp.Process):
    def __init__(self,
                 input_pipe : Connection):
        mp.Process.__init__(self)
        self.inpp = input_pipe
        
    def run(self):
        app = pg.mkQApp("Plotting Example")
        win = pg.GraphicsLayoutWidget(show=True, title="Plotting var")
        win.resize(1000,720)
        win.setWindowTitle('Plotting var')
        pg.setConfigOptions(antialias=True)
        
        err_plot = win.addPlot(title="norm(e(t))")
        err_curve = err_plot.plot(pen='r')
        err_data = []

        win.nextRow()

        Z_plot = win.addPlot(title="norm(Z(t))")
        Z_curve = Z_plot.plot(pen='y')
        Z_data = []

        win.nextRow()

        dWx_plot = win.addPlot(title="norm(dWx(t))")
        dWx_curve = dWx_plot.plot(pen='g')
        dWx_data = []

        win.nextRow()

        dWy_plot = win.addPlot(title="norm(dWy(t))")
        dWy_curve = dWy_plot.plot(pen='b')
        dWy_data = []

        def update():
            while self.inpp.poll():
                dic = self.inpp.recv()
                
                err_mag = dic["err_mag"]
                err_data.append(err_mag)
                
                Z_mag = dic["Z_mag"]
                Z_data.append(Z_mag)
                
                dWx_mag = dic["dWx_mag"]
                dWx_data.append(dWx_mag)
                
                dWy_mag = dic["dWy_mag"]
                dWy_data.append(dWy_mag)
            
            err_disp = err_data
            Z_disp = Z_data
            dWx_disp = dWx_data
            dWy_disp = dWy_data

            if len(err_data) > 2000:
                err_disp = err_data[len(err_data)-2000:]
                Z_disp = Z_data[len(Z_data)-2000:]
                dWx_disp = dWx_data[len(dWx_data)-2000:]
                dWy_disp = dWy_data[len(dWy_data)-2000:]
            err_curve.setData(err_disp)
            Z_curve.setData(Z_disp)
            dWx_curve.setData(dWx_disp)
            dWy_curve.setData(dWy_disp)


        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(50)
        pg.exec()


import math as m
import time as t  

if __name__ == '__main__':

    snd, rec = Pipe()
    plotter = PlotVar(rec)
    plotter.start()

    while True:
        snd.send(m.sin(t.time()))
        t.sleep(1/1000)