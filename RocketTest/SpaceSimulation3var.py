from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import LoadSystem3var
import spacewidget
import math
import numpy as np
import random as rd
from matplotlib.animation import FuncAnimation
import sympy as sp
import pprint
import time
import scipy.io as io
import random
import pickle
from Planetary3var import *
#from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure


class ExampleApp(QMainWindow, LoadSystem3var.Ui_MainWindow):
    def __init__(self):
        #global PS
        #FileName = ""
        #PS = "Null"
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        QMainWindow.__init__(self)
        self.setWindowTitle("Пространство галактики")
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.LoadButton.clicked.connect(self.LoadButtonClicked)
        self.StartButton.clicked.connect(self.StartButtonClicked)


    def LoadButtonClicked(self):
        global PS
        Filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")[0]
        if( Filename[-5]+Filename[-4]+Filename[-3]+Filename[-2]+Filename[-1]!=".psys"):
            print("Wrong file type, it must be *.psys")
            return

        with open(Filename, 'rb') as file:
            PS = pickle.load(file)['PS']

    def StartButtonClicked(self):
        self.SpaceWidget.canvas.axes.clear()
        global PS, Xs, Ys, VXs, VYs, PS, Xm, Ym, VXm, VYm

        if PS == 'Null':
            print("Вселенная не создана")
        else:
            self.SpaceWidget.canvas.axes.axis('equal')
            dt = float(self.TextDt.toPlainText())
            Lim = float(float(self.TextTimeLimit.toPlainText()))
            MoonNum = int(self.TextMoonNumber.toPlainText())
            MoonsR = float(self.TextMoonsR.toPlainText())
            MoonsV = float(self.TextMoonsV.toPlainText())
            Acc = float(self.TextEps.toPlainText())
            self.SpaceWidget.canvas.axes.set(xlim=[-Lim, Lim], ylim=[-Lim, Lim])
            if PS.rocket != 'Null':
                print("В данной вариации программы ракеты не доступны")
                return
            else:
                X_r = 0
                Y_r = 0
                VX_r = 0
                VY_r = 0


            print(self.CheckR.isChecked())

            moons = []
            for i in range(MoonNum):
                if(self.CheckR.isChecked()):
                    Reps = 1. + (2 * random.random()-1)*Acc/100
                else:
                    Reps = 1.

                if(self.CheckV.isChecked()):
                    Veps = 1. + (2 * random.random()-1) * Acc / 100
                else:
                    Veps = 1.

                if(self.CheckPhi.isChecked()):
                    PHIeps = 1. + (2 * random.random()-1) * Acc / 100
                else:
                    PHIeps = 1.

                print(Reps,Veps,PHIeps)

                moons.append(Moon(1, Reps*MoonsR*np.cos(2*np.pi*i/MoonNum), Reps*MoonsR*np.sin(2*np.pi*i/MoonNum),
                                 -Veps*MoonsV*np.sin((PHIeps*2*np.pi*i)/MoonNum), Veps*MoonsV*np.cos((PHIeps*2*np.pi*i)/MoonNum),
                                 0.5, 1, [1, 0, 0], [1, 0, 0]))

                if(self.CheckShow.isChecked()):
                    moons.append(Moon(1, MoonsR*np.cos(2*np.pi*i/MoonNum), MoonsR*np.sin(2*np.pi*i/MoonNum),
                                     -MoonsV*np.sin((2*np.pi*i)/MoonNum), MoonsV*np.cos((2*np.pi*i)/MoonNum),
                                     0.5, 1, [0, 1, 0], [0, 1, 0]))
            moons = np.array(moons)

            pl = PS.Planets[0]
            PS = PlanetSystem([pl])

            PS.AddMoons(moons)
            PS.GetEquationsOfMovement()


            Xs = np.array([planet.X for planet in PS.Planets])
            Ys = np.array([planet.Y for planet in PS.Planets])
            VXs = np.array([planet.Vx for planet in PS.Planets])
            VYs = np.array([planet.Vy for planet in PS.Planets])

            Xm = np.array([moon.X for moon in PS.Moons])
            Ym = np.array([moon.Y for moon in PS.Moons])
            VXm = np.array([moon.Vx for moon in PS.Moons])
            VYm = np.array([moon.Vy for moon in PS.Moons])

            PS.DrawSystem(self.SpaceWidget.canvas.axes)
            self.SpaceWidget.canvas.show()

            def KadrPlanet(i):
                global Xs, Ys, VXs, VYs, PS, Xm, Ym, VXm, VYm

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

                res = PS.EquationsOfMoons(Xs, Ys, VXs, VYs, Xm, Ym, VXm, VYm)
                k1_dX_m, k1_dY_m, k1_dVx_m, k1_dVy_m = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

                res = PS.EquationsOfMoons(Xs + k1_dX * dt / 2, Ys + k1_dY * dt / 2, VXs + k1_dVx * dt / 2,VYs + k1_dVy * dt / 2,
                            Xm + k1_dX_m * dt / 2, Ym + k1_dY_m * dt / 2,VXm + k1_dVx_m * dt / 2, VYm + k1_dVy_m * dt / 2)
                k2_dX_m, k2_dY_m, k2_dVx_m, k2_dVy_m = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

                res = PS.EquationsOfMoons(Xs + k2_dX * dt / 2, Ys + k2_dY * dt / 2, VXs + k2_dVx * dt / 2,VYs + k2_dVy * dt / 2,
                            Xm + k2_dX_m * dt / 2, Ym + k2_dY_m * dt / 2,VXm + k2_dVx_m * dt / 2, VYm + k2_dVy_m * dt / 2)
                k3_dX_m, k3_dY_m, k3_dVx_m, k3_dVy_m = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

                res = PS.EquationsOfMoons(Xs + k3_dX * dt, Ys + k3_dY * dt, VXs + k3_dVx * dt, VYs + k3_dVy * dt, Xm + k3_dX_m * dt,
                            Ym + k3_dY_m * dt, VXm + k3_dVx_m * dt, VYm + k3_dVy_m * dt)
                k4_dX_m, k4_dY_m, k4_dVx_m, k4_dVy_m = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

                Xm += dt / 6 * (k1_dX_m + 2 * k2_dX_m + 2 * k3_dX_m + k4_dX_m)
                Ym += dt / 6 * (k1_dY_m + 2 * k2_dY_m + 2 * k3_dY_m + k4_dY_m)
                VXm += dt / 6 * (k1_dVx_m + 2 * k2_dVx_m + 2 * k3_dVx_m + k4_dVx_m)
                VYm += dt / 6 * (k1_dVy_m + 2 * k2_dVy_m + 2 * k3_dVy_m + k4_dVy_m)

                for moon, x_m, y_m, vx_m, vy_m in zip(PS.Moons, Xm, Ym, VXm, VYm):
                    moon.X = x_m
                    moon.Y = y_m
                    moon.Vx = vx_m
                    moon.Vy = vy_m

                PS.ReplaceSystem(self.SpaceWidget.canvas.axes)

                return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets]\
                       + [moon.Gp for moon in PS.Moons] + [moon.Gt for moon in PS.Moons]

            print(7)
            fig = self.SpaceWidget.canvas.figure
            Animation1 = FuncAnimation(fig, KadrPlanet, interval=dt * 1000, blit=True)

            self.SpaceWidget.canvas.draw()



app = QApplication([])  # Новый экземпляр QApplication
window = ExampleApp()  # Создаём объект класса ExampleApp
window.show()  # Показываем окно
app.exec_()  # и запускаем приложение

