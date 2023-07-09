from Planetary import *
from matplotlib.animation import FuncAnimation
import numpy as np
import pickle
import math


def secondtry(maain):
    global Xs,Ys,VXs,VYs,X_r,Y_r,VX_r,VY_r, started, t, firePhi, Phi_r, F_r, accepted, prevPhi
    Filename = 'Universe2.psys'
    print(Filename)
    PS = None
    with open(Filename, 'rb') as file:
        PS = pickle.load(file)['PS']
    maain.SpaceWidget.canvas.axes.clear()
    PS.GetEquationsOfMovement()
    maain.SpaceWidget.canvas.axes.axis('equal')
    Lim = float(maain.Lim_field.toPlainText())
    maain.SpaceWidget.canvas.axes.set(xlim=[-Lim, Lim], ylim=[-Lim, Lim])
    X_r = PS.rocket.X
    Y_r = PS.rocket.Y
    VX_r = PS.rocket.Vx
    VY_r = PS.rocket.Vy
    Xs = np.array([planet.X for planet in PS.Planets])
    Ys = np.array([planet.Y for planet in PS.Planets])
    VXs = np.array([planet.Vx for planet in PS.Planets])
    VYs = np.array([planet.Vy for planet in PS.Planets])
    PS.DrawSystem(maain.SpaceWidget.canvas.axes)
    maain.SpaceWidget.canvas.show()
    dt = float(maain.Dt_field.toPlainText())
    for planet in PS.Planets:
        if planet.name == "Earth":
            earth = planet
        if planet.name == "moon":
            moon = planet
    accepted = 0
    firePhi = 0
    started = 0
    prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
    def KadrPlanetMoon(i):
        global Xs,Ys,VXs,VYs,X_r,Y_r,VX_r,VY_r, started, t, firePhi, Phi_r, F_r, accepted, prevPhi
        rollAng = 7.960175781249993
        Phase = 1.946875#2#6.283185307179586

        Phi_r = -math.pi / 2 + math.atan2(moon.Y - PS.rocket.Y, moon.X - PS.rocket.X)
        EM = math.atan2(earth.Y - moon.Y, earth.X - moon.X)
        nX = (X_r - moon.X) * np.cos(-EM) - (Y_r - moon.Y) * np.sin(-EM)
        nY = (Y_r - moon.Y) * np.cos(-EM) + (X_r - moon.X) * np.sin(-EM)
        ERM = math.atan2(nY, nX)

        curPhase = (ERM - Phase)
        while curPhase <= 0:
            curPhase+=2*np.pi
        while curPhase > 2 * np.pi:
            curPhase-=2*np.pi

        if curPhase < 0.005 and started == 0:
            started = 1
            print('aaaaaaaa', ERM, Phase, ERM - Phase, curPhase)
            print('ER', math.atan2(Y_r - moon.Y, X_r - moon.X))
        if abs(firePhi) <= rollAng and started == 1:
            F_r = -13000
            nX = (X_r - moon.X) * np.cos(-prevPhi) - (Y_r - moon.Y) * np.sin(-prevPhi)
            nY = (Y_r - moon.Y) * np.cos(-prevPhi) + (X_r - moon.X) * np.sin(-prevPhi)
            dPhi = math.atan2(nY, nX)
            firePhi += dPhi
            print('fireee')
        else:
            F_r = 0
        if abs(firePhi) > rollAng:
            print(((X_r - moon.X)**2+(Y_r - moon.Y)**2)**0.5)
        if accepted == 0 and ((moon.X - X_r) ** 2 + (moon.Y - Y_r) ** 2) ** 0.5 >= 0.5 * (
                (earth.X - moon.X) ** 2 + (earth.Y - moon.Y) ** 2) ** 0.5:
            accepted = 1
            print('accepted', ((PS.rocket.Vx - earth.Vx) ** 2 + (PS.rocket.Vy - earth.Vy) ** 2) ** 0.5)
        prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
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
                if planet.name=="Earth" :
                    eX = planet.X
                    eY = planet.Y
                if planet.name=="moon":
                    mX = planet.X
                    mY = planet.Y
                    mR = planet.Rc

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

        PS.ReplaceSystem(maain.SpaceWidget.canvas.axes)

        if PS.rocket != 'Null':
            return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets] + [PS.rocket.Gr,
                                                                                                  PS.rocket.Gt,
                                                                                                  PS.rocket.Gf]
        else:
            return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets]

    fig = maain.SpaceWidget.canvas.figure
    Animation1 = FuncAnimation(fig, KadrPlanetMoon, interval=abs(dt) * 1000, blit=True)
    maain.SpaceWidget.canvas.draw()