import Planetary
import pickle
import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt



fig = plt.figure()
ax1 = fig.add_subplot(1,3,1)
ax1.set(title='Скорость от расстояния до земли')
ax2 = fig.add_subplot(1,3,2)
ax2.set(title='Угол скорости от расстояния до земли')
ax3 = fig.add_subplot(1,3,3)
ax3.set(title='Угол между ракетой и луной')

SpeedGraphX = np.array([])
SpeedGraphY = np.array([])
AlphaGraphY = np.array([])
BetaGraphY = np.array([])


for i in np.linspace(0,2*np.pi, 50):
    print(i)
    PS = None
    Filename = 'Universe1.psys'
    # print(Filename)
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
    dt = 0.01
    t0 = 0
    t = 0
    firePhi = 0
    Phi_r = 0
    F_r = 0
    started = 0
    for planet in PS.Planets:
        if planet.name == "Earth":
            earth = planet
        if planet.name == "moon":
            moon = planet
    prevPhi = math.atan2(Y_r - earth.Y, X_r - earth.X)
    while(((earth.X-X_r)**2+(earth.Y-Y_r)**2)**0.5<0.5*((earth.X-moon.X)**2+(earth.Y-moon.Y)**2)**0.5):

        # print(((earth.X-X_r)**2+(earth.Y-Y_r)**2)**0.5/(0.5*((earth.X-moon.X)**2+(earth.Y-moon.Y)**2)**0.5))

        rollAng = 50.5
        Phase = i
        EM = math.atan2(moon.Y - earth.Y, moon.X - earth.X)
        nX = (X_r - earth.X) * np.cos(-EM) - (Y_r - earth.Y) * np.sin(-EM)
        nY = (Y_r - earth.Y) * np.cos(-EM) + (X_r - earth.X) * np.sin(-EM)
        ERM = math.atan2(nY, nX)

        curPhase = (ERM - Phase)
        while curPhase <= 0:
            curPhase+=2*np.pi
        while curPhase > 2 * np.pi:
            curPhase-=2*np.pi

        if curPhase < 0.005 and started == 0:
            started = 1
            # print('staaaart')
        if abs(firePhi) <= rollAng and started == 1:
            F_r = 13000
            nX = (X_r - earth.X) * np.cos(-prevPhi) - (Y_r - earth.Y) * np.sin(-prevPhi)
            nY = (Y_r - earth.Y) * np.cos(-prevPhi) + (X_r - earth.X) * np.sin(-prevPhi)
            dPhi = math.atan2(nY, nX)
            firePhi += dPhi
        else:
            F_r = 0

        prevPhi = math.atan2(Y_r - earth.Y, X_r - earth.X)
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
                if planet.name=="Earth" :
                    eX = planet.X
                    eY = planet.Y
                if planet.name=="moon":
                    mX = planet.X
                    mY = planet.Y
                    mR = planet.Rc

            Phi_r = - math.pi/2 + math.atan2(eY-PS.rocket.Y, eX-PS.rocket.X)
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

    SpeedGraphX = np.append(SpeedGraphX, i)
    SpeedGraphY = np.append(SpeedGraphY, ((PS.rocket.Vx - earth.Vx)**2+(PS.rocket.Vy - earth.Vy)**2)**0.5)

    ER = math.atan2(Y_r-earth.Y, X_r - earth.X)

    nX = (PS.rocket.Vx - earth.Vx) * np.cos(-ER) - (PS.rocket.Vy - earth.Vy) * np.sin(-ER)
    nY = (PS.rocket.Vy - earth.Vy) * np.cos(-ER) + (PS.rocket.Vx - earth.Vx) * np.sin(-ER)
    VRM = math.atan2(nY, nX)
    AlphaGraphY = np.append(AlphaGraphY, VRM)

    EM = math.atan2(moon.Y - earth.Y, moon.X - earth.X)
    nX = (PS.rocket.X - earth.X) * np.cos(-EM) - (PS.rocket.Y - earth.Y) * np.sin(-EM)
    nY = (PS.rocket.Y - earth.Y) * np.cos(-EM) + (PS.rocket.X - earth.X) * np.sin(-EM)
    ERM = math.atan2(nY, nX)
    BetaGraphY = np.append(BetaGraphY, ERM)

    # print(SpeedGraphY)

fileway = 'C:/Users/iTunkimi/Desktop/GitReps/CosmoSimulation/RocketTest/TVrPhir_0.01_0-2pi-629-47.79new.csv'
t = np.linspace(0,2*np.pi, 50)
df = pd.DataFrame([t, SpeedGraphY, AlphaGraphY, BetaGraphY]).T
df1 = pd.DataFrame([], columns=['t', 'Vr', 'Alphar', 'Betar'])
df1['t']=df[0]
df1['Vr']=df[1]
df1['Alphar']=df[2]
df1['Betar']=df[3]
df1.to_csv(fileway)

ax1.plot(SpeedGraphX,SpeedGraphY)
ax2.plot(SpeedGraphX, AlphaGraphY)
ax3.plot(SpeedGraphX, BetaGraphY)



plt.show()

