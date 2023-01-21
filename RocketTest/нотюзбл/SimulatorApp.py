# from PyQt5.QtWidgets import *
#
# from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

# import math
# import numpy as np
# import random as rd
# from matplotlib.animation import FuncAnimation
# import sympy as sp
# import pprint
import time
# from Planetary import *
# #from matplotlib.backends.backend_qt5agg import FigureCanvas
#
# from matplotlib.figure import Figure

import spacewidget
import pickle
import numpy as np
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import LoadSystem as design  # Это наш конвертированный файл дизайна
from Planetary import Planet, PlanetSystem, Rocket, Rot2D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        FileName = ""
        QtWidgets.QMainWindow.__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.LoadButton.clicked.connect(self.LoadButtonClicked)
        self.StartButton.clicked.connect(self.StartButtonClicked)
        self.dt = 0.01

        # self.addToolBar(NavigationToolbar())


    def LoadButtonClicked(self):
        Filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")[0]
        if( Filename[-5]+Filename[-4]+Filename[-3]+Filename[-2]+Filename[-1]!=".psys"):
            print("Wrong file type, it must be *.psys")
            return
        self.Filename = Filename


    def StartButtonClicked(self):
        print("Opened File: ", self.Filename)
        with open(self.Filename, 'rb') as file:
            PS = pickle.load(file)['PS']
        self.SpaceWidget.canvas.axes.clear()
        PS.GetEquationsOfMovement()
        self.SpaceWidget.canvas.axes.axis('equal')
        self.SpaceWidget.canvas.axes.set(xlim=[-5, 5], ylim=[-5, 5])

        X_r = 0
        Y_r = 0
        VX_r = 0
        VY_r = 0
        if PS.rocket != 'Null':
            X_r = PS.rocket.X
            Y_r = PS.rocket.Y
            VX_r = PS.rocket.Vx
            VY_r = PS.rocket.Vy


        Xs = np.array([planet.X for planet in PS.Planets])
        Ys = np.array([planet.Y for planet in PS.Planets])

        VXs = np.array([planet.Vx for planet in PS.Planets])
        VYs = np.array([planet.Vy for planet in PS.Planets])

        PS.DrawSystem(self.SpaceWidget.canvas.axes)
        self.SpaceWidget.canvas.show()


        dt = 0.01


        Phi_r = 0
        F_r = 0
        def KadrPlanet(i):
            global Xs, Ys, VXs, VYs, PS, X_r, Y_r, VX_r, VY_r, Phi_r, F_r

            res = PS.EquationsOfMovement(Xs, Ys, VXs, VYs)
            k1_dX, k1_dY, k1_dVx, k1_dVy = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

            res = PS.EquationsOfMovement(Xs + k1_dX * dt / 2, Ys + k1_dY * dt / 2, VXs + k1_dVx * dt / 2,
                                         VYs + k1_dVy * dt / 2)
            k2_dX, k2_dY, k2_dVx, k2_dVy = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

            res = PS.EquationsOfMovement(Xs + k2_dX * dt / 2, Ys + k2_dY * dt / 2, VXs + k2_dVx * dt / 2,
                                         VYs + k2_dVy * dt / 2)
            k3_dX, k3_dY, k3_dVx, k3_dVy = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

            res = PS.EquationsOfMovement(Xs + k3_dX * dt, Ys + k3_dY * dt, VXs + k3_dVx * dt, VYs + k3_dVy * dt)
            k4_dX, k4_dY, k4_dVx, k4_dVy = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

            Xs += dt / 6 * (k1_dX + 2 * k2_dX + 2 * k3_dX + k4_dX)
            Ys += dt / 6 * (k1_dY + 2 * k2_dY + 2 * k3_dY + k4_dY)
            VXs += dt / 6 * (k1_dVx + 2 * k2_dVx + 2 * k3_dVx + k4_dVx)
            VYs += dt / 6 * (k1_dVy + 2 * k2_dVy + 2 * k3_dVy + k4_dVy)

            for planet, x, y, vx, vy in zip(PS.Planets, Xs, Ys, VXs, VYs):
                planet.X = x
                planet.Y = y
                planet.Vx = vx
                planet.Vy = vy

            if PS.rocket != 'Null':
                # Phi_r = 3 * 3.14 / 2 - self.AngleBar.value() / 100
                # F_r = (100 - self.EngineBar.value()) / 10
                res = PS.EquationsOfRocket(Xs, Ys, VXs, VYs, X_r, Y_r, VX_r, VY_r, Phi_r, F_r)
                k1_dX_r, k1_dY_r, k1_dVx_r, k1_dVy_r = np.array(res[0]), np.array(res[1]), np.array(
                    res[2]), np.array(res[3])

                res = PS.EquationsOfRocket(Xs + k1_dX * dt / 2, Ys + k1_dY * dt / 2, VXs + k1_dVx * dt / 2,
                                           VYs + k1_dVy * dt / 2, X_r + k1_dX_r * dt / 2, Y_r + k1_dY_r * dt / 2,
                                           VX_r + k1_dVx_r * dt / 2, VY_r + k1_dVy_r * dt / 2, Phi_r, F_r)
                k2_dX_r, k2_dY_r, k2_dVx_r, k2_dVy_r = np.array(res[0]), np.array(res[1]), np.array(
                    res[2]), np.array(res[3])

                res = PS.EquationsOfRocket(Xs + k2_dX * dt / 2, Ys + k2_dY * dt / 2, VXs + k2_dVx * dt / 2,
                                           VYs + k2_dVy * dt / 2, X_r + k2_dX_r * dt / 2, Y_r + k2_dY_r * dt / 2,
                                           VX_r + k2_dVx_r * dt / 2, VY_r + k2_dVy_r * dt / 2, Phi_r, F_r)
                k3_dX_r, k3_dY_r, k3_dVx_r, k3_dVy_r = np.array(res[0]), np.array(res[1]), np.array(
                    res[2]), np.array(res[3])

                res = PS.EquationsOfRocket(Xs + k3_dX * dt, Ys + k3_dY * dt, VXs + k3_dVx * dt, VYs + k3_dVy * dt,
                                           X_r + k3_dX_r * dt, Y_r + k3_dY_r * dt, VX_r + k3_dVx_r * dt,
                                           VY_r + k3_dVy_r * dt, Phi_r, F_r)
                k4_dX_r, k4_dY_r, k4_dVx_r, k4_dVy_r = np.array(res[0]), np.array(res[1]), np.array(
                    res[2]), np.array(res[3])

                X_r += dt / 6 * (k1_dX_r + 2 * k2_dX_r + 2 * k3_dX_r + k4_dX_r)
                Y_r += dt / 6 * (k1_dY_r + 2 * k2_dY_r + 2 * k3_dY_r + k4_dY_r)
                VX_r += dt / 6 * (k1_dVx_r + 2 * k2_dVx_r + 2 * k3_dVx_r + k4_dVx_r)
                VY_r += dt / 6 * (k1_dVy_r + 2 * k2_dVy_r + 2 * k3_dVy_r + k4_dVy_r)

                PS.rocket.X = X_r
                PS.rocket.Y = Y_r
                PS.rocket.Vx = VX_r
                PS.rocket.Vy = VY_r
                PS.rocket.F = F_r
                PS.rocket.Phi = Phi_r

            PS.ReplaceSystem(self.SpaceWidget.canvas.axes)

            if PS.rocket != 'Null':
                return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets] + [PS.rocket.Gr,
                                                                                                      PS.rocket.Gt,
                                                                                                      PS.rocket.Gf]
            else:
                return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets]


        fig = self.SpaceWidget.canvas.figure
        Animation = FuncAnimation(fig, KadrPlanet, interval=self.dt * 1000, blit=True)
        print(0)
        self.SpaceWidget.canvas.draw()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()