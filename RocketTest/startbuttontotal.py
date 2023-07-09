import pickle
import numpy as np
import math
from matplotlib.animation import FuncAnimation
def total(maaaain):
    global Xs,Ys,VXs,VYs,X_r,Y_r,VX_r,VY_r, started, t, firePhi, Phi_r, F_r, accepted, prevPhi, moonstarted, earth, moon
    Filename = 'Universe1.psys'
    print(Filename)
    with open(Filename, 'rb') as file:
        PS = pickle.load(file)['PS']
    maaaain.SpaceWidget.canvas.axes.clear()
    PS.GetEquationsOfMovement()
    maaaain.SpaceWidget.canvas.axes.axis('equal')
    Lim = float(maaaain.Lim_field.toPlainText())
    maaaain.SpaceWidget.canvas.axes.set(xlim=[-Lim, Lim], ylim=[-Lim, Lim])
    X_r = PS.rocket.X
    Y_r = PS.rocket.Y
    VX_r = PS.rocket.Vx
    VY_r = PS.rocket.Vy
    Xs = np.array([planet.X for planet in PS.Planets])
    Ys = np.array([planet.Y for planet in PS.Planets])
    VXs = np.array([planet.Vx for planet in PS.Planets])
    VYs = np.array([planet.Vy for planet in PS.Planets])
    PS.DrawSystem(maaaain.SpaceWidget.canvas.axes)
    maaaain.SpaceWidget.canvas.show()
    dt = float(maaaain.Dt_field.toPlainText())
    t = 0
    firePhi = 0
    Phi_r = 0
    F_r = 0
    started = 0
    moonstarted = 0
    for planet in PS.Planets:
        if planet.name == "Earth":
            earth = planet
        if planet.name == "moon":
            moon = planet
    prevPhi = math.atan2(Y_r - earth.Y, X_r - earth.X)
    def KadrPlanet(i):
        global Xs,Ys,VXs,VYs,X_r,Y_r,VX_r,VY_r, started, t, firePhi, Phi_r, F_r, accepted, prevPhi, moonstarted, earth, moon
        AngE = 50.31632812500004#50.69
        PhaseE = -0.56375#-0.59 #-0.5 #-0.45
        AngM = 7.928925781249994#7.960175781249993
        PhaseM = 1.946875
        RtoMoon = 2.36436610879894


        firsthalfway = ((earth.X-X_r)**2+(earth.Y-Y_r)**2)**0.5 < 0.5*((earth.X-moon.X)**2+(earth.Y-moon.Y)**2)**0.5
        if firsthalfway:
            EM = math.atan2(moon.Y - earth.Y, moon.X - earth.X)
            nX = (X_r - earth.X) * np.cos(-EM) - (Y_r - earth.Y) * np.sin(-EM)
            nY = (Y_r - earth.Y) * np.cos(-EM) + (X_r - earth.X) * np.sin(-EM)
            ERM = math.atan2(nY, nX)
            Phi_r = - math.pi/2 + math.atan2(earth.Y-PS.rocket.Y, earth.X-PS.rocket.X)
            curPhase = (ERM - PhaseE)
            while curPhase <= 0:
                curPhase+=2*np.pi
            while curPhase > 2 * np.pi:
                curPhase-=2*np.pi

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
            Phi_r = - math.pi/2 + math.atan2(moon.Y-Y_r, moon.X-X_r)
            F_r = 0
            if moonstarted == 0 and ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2)**0.5 <= RtoMoon:
                print('STAAAAARTED')
                moonstarted = 1
                prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                firePhi = 0
            elif moonstarted == 1 and abs(firePhi) <= AngM and ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2)**0.5>0.3156254615:
                F_r = -13000
                nX = (X_r - moon.X) * np.cos(-prevPhi) - (Y_r - moon.Y) * np.sin(-prevPhi)
                nY = (Y_r - moon.Y) * np.cos(-prevPhi) + (X_r - moon.X) * np.sin(-prevPhi)
                dPhi = math.atan2(nY, nX)
                firePhi += dPhi
                prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                print(dPhi, firePhi, '\t', ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2)**0.5)




        t+=dt
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
                if planet.name == "Earth":
                    eX = planet.X
                    eY = planet.Y
                if planet.name == "moon":
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
        PS.ReplaceSystem(maaaain.SpaceWidget.canvas.axes)

        if PS.rocket != 'Null':
            return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets] + [PS.rocket.Gr,
                                                                                                  PS.rocket.Gt,
                                                                                                  PS.rocket.Gf]
        else:
            return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets]

    fig = maaaain.SpaceWidget.canvas.figure
    Animation1 = FuncAnimation(fig, KadrPlanet, interval=abs(dt) * 1000, blit=True)
    maaaain.SpaceWidget.canvas.draw()