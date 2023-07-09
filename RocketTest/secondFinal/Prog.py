import math
import numpy as np
from PyQt5.QtWidgets import *
import secondfinal as LoadSystem
from matplotlib.animation import FuncAnimation
import pickle
from functools import partial


class ExampleApp(QMainWindow, LoadSystem.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        QMainWindow.__init__(self)
        self.setWindowTitle("Пространство галактики")
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # self.LoadSystemButton.clicked.connect(self.LoadSystemButtonClicked)
        self.LoadPresetButton.clicked.connect(self.LoadPresetButtonClicked)

        fig = self.SpaceWidget.canvas.figure
        ax1 = self.SpaceWidget.canvas.axes1
        ax2 = self.SpaceWidget.canvas.axes2
        ax1.set_aspect('equal', 'box')
        ax1.set(xlim=(-20, 60), ylim=(-20, 60))
        # ax1.set(xlim=(-2, 2), ylim=(-2, 2))
        ax2.set_aspect('equal', 'box')
        ax2.set(xlim=(-0.8, 0.8), ylim=(-0.8, 0.8))


    def LoadPresetButtonClicked(self):

        def Kadr(PS, earth, moon, rock, center, coords, ax, frame):
            print(frame)
            rock.Phi = coords[8][int(frame)]
            earth.X, earth.Y, moon.X, moon.Y, rock.X, rock.Y = coords[0][int(frame)], coords[1][int(frame)], coords[2][
                int(frame)], \
                                                               coords[3][int(frame)], coords[4][int(frame)], coords[5][
                                                                   int(frame)]
            PS.ReplaceSystem(ax, center)
            return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets] + [PS.rocket.Gr,
                                                                                                  PS.rocket.Gt,
                                                                                                  PS.rocket.Gf]

        def orbDisplay(par, totalt):
            dt = par[0]
            Filename = 'Universe1.psys'
            print('file')
            with open(Filename, 'rb') as file:
                PS = pickle.load(file)['PS']
            PS.GetEquationsOfMovement()
            X_r = PS.rocket.X
            Y_r = PS.rocket.Y
            VX_r = PS.rocket.Vx
            VY_r = PS.rocket.Vy
            Xs = np.array([planet.X for planet in PS.Planets])
            Ys = np.array([planet.Y for planet in PS.Planets])
            VXs = np.array([planet.Vx for planet in PS.Planets])
            VYs = np.array([planet.Vy for planet in PS.Planets])
            t = 0
            firePhi = 0
            fireMPhi = 0
            Phi_r = PS.rocket.Phi
            F_r = 0
            started = 0
            moonstarted = 0
            for planet in PS.Planets:
                if planet.name == "Earth":
                    earth = planet
                if planet.name == "moon":
                    moon = planet
            prevPhi = math.atan2(Y_r - earth.Y, X_r - earth.X)
            checkPhi = 0
            ErthX = np.array([])
            ErthY = np.array([])
            MoonX = np.array([])
            MoonY = np.array([])
            RockX = np.array([])
            RockY = np.array([])
            RockPhi = np.array([])

            time = np.array([])
            R = np.array([])

            while t < totalt:  # checkPhi<10*np.pi:
                print(t)
                AngE = par[1]  # 50.31632812500004  # 50.69
                PhaseE = par[2]  # -0.56375  # -0.59 #-0.5 #-0.45
                AngM = par[3]  # 7.960175781249993
                PhaseM = 1.946875
                Rtomoon = par[4]  # 2.114366108798941

                ErthX = np.append(ErthX, earth.X)
                ErthY = np.append(ErthY, earth.Y)
                MoonX = np.append(MoonX, moon.X)
                MoonY = np.append(MoonY, moon.Y)
                RockX = np.append(RockX, X_r)
                RockY = np.append(RockY, Y_r)
                RockPhi = np.append(RockPhi, Phi_r)

                firsthalfway = ((earth.X - X_r) ** 2 + (earth.Y - Y_r) ** 2) ** 0.5 < 0.5 * (
                        (earth.X - moon.X) ** 2 + (earth.Y - moon.Y) ** 2) ** 0.5
                if firsthalfway:
                    EM = math.atan2(moon.Y - earth.Y, moon.X - earth.X)
                    nX = (X_r - earth.X) * np.cos(-EM) - (Y_r - earth.Y) * np.sin(-EM)
                    nY = (Y_r - earth.Y) * np.cos(-EM) + (X_r - earth.X) * np.sin(-EM)
                    ERM = math.atan2(nY, nX)
                    Phi_r = - math.pi / 2 + math.atan2(earth.Y - PS.rocket.Y, earth.X - PS.rocket.X)
                    curPhase = (ERM - PhaseE)
                    while curPhase <= 0:
                        curPhase += 2 * np.pi
                    while curPhase > 2 * np.pi:
                        curPhase -= 2 * np.pi

                    if curPhase < 0.005 and started == 0:
                        started = 1
                    F_r = 0
                    if abs(firePhi) <= AngE and started == 1:
                        F_r = 13000
                        nX = (X_r - earth.X) * np.cos(-prevPhi) - (Y_r - earth.Y) * np.sin(-prevPhi)
                        nY = (Y_r - earth.Y) * np.cos(-prevPhi) + (X_r - earth.X) * np.sin(-prevPhi)
                        dPhi = math.atan2(nY, nX)
                        firePhi += dPhi
                    prevPhi = math.atan2(Y_r - earth.Y, X_r - earth.X)
                else:
                    Phi_r = - math.pi / 2 + math.atan2(moon.Y - Y_r, moon.X - X_r)
                    F_r = 0
                    if moonstarted == 0 and ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2) ** 0.5 <= Rtomoon:
                        moonstarted = 1
                        prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                        fireMPhi = 0
                    elif moonstarted == 1 and abs(fireMPhi) <= AngM:
                        F_r = -13000
                        nX = (X_r - moon.X) * np.cos(-prevPhi) - (Y_r - moon.Y) * np.sin(-prevPhi)
                        nY = (Y_r - moon.Y) * np.cos(-prevPhi) + (X_r - moon.X) * np.sin(-prevPhi)
                        dPhi = math.atan2(nY, nX)
                        fireMPhi += dPhi
                        prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                    elif abs(fireMPhi) > AngM:
                        nX = (X_r - moon.X) * np.cos(-prevPhi) - (Y_r - moon.Y) * np.sin(-prevPhi)
                        nY = (Y_r - moon.Y) * np.cos(-prevPhi) + (X_r - moon.X) * np.sin(-prevPhi)
                        dPhi = math.atan2(nY, nX)
                        checkPhi += dPhi
                        # Err = np.append(Err, (0.3156254615 - ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2) ** 0.5)**2)
                        prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                        time = np.append(time, t)
                        R = np.append(R, ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2) ** 0.5)

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

                t += dt

            # return Err
            print('t:', t)
            return ErthX, ErthY, MoonX, MoonY, RockX, RockY, time, R, RockPhi

        totalT = float(self.tLimInput.toPlainText())
        dt = float(self.dtInput.toPlainText())
        cadrSkip = int(self.cadrSkipField.toPlainText())

        tempParams = [dt, 50.31865814208989, -0.5670703125000086, 7.918574218750057, 2.141426655673945]

        res = orbDisplay(tempParams, totalT)

        fig = self.SpaceWidget.canvas.figure
        ax1 = self.SpaceWidget.canvas.axes1
        ax2 = self.SpaceWidget.canvas.axes2

        Filename = 'Universe1.psys'
        with open(Filename, 'rb') as file:
            Sys1 = pickle.load(file)['PS']
        for planet in Sys1.Planets:
            if planet.name == "Earth":
                Ea1 = planet
            if planet.name == "moon":
                Mo1 = planet
        Ro1 = Sys1.rocket
        with open(Filename, 'rb') as file:
            Sys2 = pickle.load(file)['PS']
        for planet in Sys2.Planets:
            if planet.name == "Earth":
                Ea2 = planet
            if planet.name == "moon":
                Mo2 = planet
        Ro2 = Sys2.rocket


        Sys1.DrawSystem(ax1, Ea1)
        anim1 = FuncAnimation(fig, partial(Kadr, Sys1, Ea1, Mo1, Ro1, Ea1, res, ax1),
                              np.linspace(0, totalT / 0.001, int((totalT / 0.001) / cadrSkip), dtype=np.int64), blit=True)

        Sys2.DrawSystem(ax2, Mo2)
        anim2 = FuncAnimation(fig, partial(Kadr, Sys2, Ea2, Mo2, Ro2, Mo2, res, ax2),
                              np.linspace(0, totalT / 0.001, int((totalT / 0.001) / cadrSkip), dtype=np.int64), blit=True)

        self.SpaceWidget.canvas.draw()


app = QApplication([])  # Новый экземпляр QApplication
window = ExampleApp()  # Создаём объект класса ExampleApp
window.show()  # Показываем окно
app.exec_()  # и запускаем приложение