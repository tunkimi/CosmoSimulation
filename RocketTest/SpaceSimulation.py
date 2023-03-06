import math

from PyQt5.QtWidgets import *
import LoadSystem
from matplotlib.animation import FuncAnimation
import pickle
from Planetary import *


class ExampleApp(QMainWindow, LoadSystem.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        QMainWindow.__init__(self)
        self.setWindowTitle("Пространство галактики")
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.LoadButton.clicked.connect(self.LoadButtonClicked)
        self.StartButton.clicked.connect(self.StartButtonClicked)
        self.EngineBar.setValue(100)
        self.AngleBar.setValue(314)


    def LoadButtonClicked(self):
        global PS
        Filename = self.Filename_field.text() + '.psys'

        with open(Filename, 'rb') as file:
            PS = pickle.load(file)['PS']


    def StartButtonClicked(self):

        self.SpaceWidget.canvas.axes.clear()
        global PS, Xs, Ys, VXs, VYs, PS, X_r, Y_r, VX_r, VY_r, Phi_r, F_r
        Filename = self.Filename_field.text() + '.psys'

        with open(Filename, 'rb') as file:
            PS = pickle.load(file)['PS']
        if PS == 'Null':
            print("Вселенная не создана")
        else:
            PS.GetEquationsOfMovement()
            self.SpaceWidget.canvas.axes.axis('equal')
            Lim = float(self.Lim_field.text())
            self.SpaceWidget.canvas.axes.set(xlim=[-Lim, Lim], ylim=[-Lim, Lim])
            # self.SpaceWidget.canvas.axes.set(xlim=[50, 60], ylim=[-2, 20])
            if PS.rocket != 'Null':
                X_r = PS.rocket.X
                Y_r = PS.rocket.Y
                VX_r = PS.rocket.Vx
                VY_r = PS.rocket.Vy
            else:
                X_r = 0
                Y_r = 0
                VX_r = 0
                VY_r = 0

            Xs = np.array([planet.X for planet in PS.Planets])
            Ys = np.array([planet.Y for planet in PS.Planets])

            VXs = np.array([planet.Vx for planet in PS.Planets])
            VYs = np.array([planet.Vy for planet in PS.Planets])

            PS.DrawSystem(self.SpaceWidget.canvas.axes)
            self.SpaceWidget.canvas.show()
            dt = float(self.Dt_field.text())

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
                    for planet in PS.Planets:
                        if planet.name=="Earth":
                            eX = planet.X
                            eY = planet.Y
                        if planet.name=="moon":
                            mX = planet.X
                            mY = planet.Y
                            mR = planet.Rc
                    # print(((PS.rocket.X-mX)**2+(PS.rocket.Y-mY)**2)**(1/2)-mR)
                    # Phi_r = 3*3.14/2 - self.AngleBar.value()/100
                    F_r = (100-self.EngineBar.value())*13000
                    Phi_r = -math.pi/2 + math.atan2(eY-PS.rocket.Y, eX-PS.rocket.X)
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
            Animation1 = FuncAnimation(fig, KadrPlanet, interval=dt * 1000, blit=True)

            self.SpaceWidget.canvas.draw()



app = QApplication([])  # Новый экземпляр QApplication
window = ExampleApp()  # Создаём объект класса ExampleApp
window.show()  # Показываем окно
app.exec_()  # и запускаем приложение

