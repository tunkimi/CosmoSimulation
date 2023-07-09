import numpy as np
import pickle
import math
import time
import pandas as pd


def GetFromEarth(phazeE, angE, dt):
    # dt = 0.01
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

        # print(((earth.X-X_r)**2+(earth.Y-Y_r)**2)**0.5,(0.5*((earth.X-moon.X)**2+(earth.Y-moon.Y)**2)**0.5))

        rollAng = angE
        Phase = phazeE
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

    ER = math.atan2(Y_r-earth.Y, X_r - earth.X)

    nX = (PS.rocket.Vx - earth.Vx) * np.cos(-ER) - (PS.rocket.Vy - earth.Vy) * np.sin(-ER)
    nY = (PS.rocket.Vy - earth.Vy) * np.cos(-ER) + (PS.rocket.Vx - earth.Vx) * np.sin(-ER)
    VRM = math.atan2(nY, nX)

    EM = math.atan2(moon.Y - earth.Y, moon.X - earth.X)
    nX = (PS.rocket.X - earth.X) * np.cos(-EM) - (PS.rocket.Y - earth.Y) * np.sin(-EM)
    nY = (PS.rocket.Y - earth.Y) * np.cos(-EM) + (PS.rocket.X - earth.X) * np.sin(-EM)
    ERM = math.atan2(nY, nX)
    return  ((PS.rocket.Vx - earth.Vx)**2+(PS.rocket.Vy - earth.Vy)**2)**0.5, VRM, ERM

def GetFromMoon(phazeM, angM, dt):
    # dt = -0.01
    Filename = 'Universe2.psys'
    PS = None
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
    for planet in PS.Planets:
        if planet.name == "Earth":
            earth = planet
        if planet.name == "moon":
            moon = planet
    # print(((Y_r-moon.Y)**2+(X_r-moon.X)**2)**0.5)
    accepted = 0
    firePhi = 0
    started = 0
    prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
    inside = 0
    while(((moon.X-X_r)**2+(moon.Y-Y_r)**2)**0.5<((earth.X-moon.X)**2+(earth.Y-moon.Y)**2)**0.5 and inside == 0):
        if ((earth.X-X_r)**2+(earth.Y-Y_r)**2)**0.5<0.5*((earth.X-moon.X)**2+(earth.Y-moon.Y)**2)**0.5:
            inside = 1

        rollAng = angM
        Phase = phazeM
        EM = math.atan2(earth.Y - moon.Y, earth.X - moon.X)
        nX = (X_r - moon.X) * np.cos(-EM) - (Y_r - moon.Y) * np.sin(-EM)
        nY = (Y_r - moon.Y) * np.cos(-EM) + (X_r - moon.X) * np.sin(-EM)
        ERM = math.atan2(nY, nX)

        curPhase = (ERM - Phase)
        while curPhase <= 0:
            curPhase+=2*np.pi
        while curPhase > 2 * np.pi:
            curPhase-=2*np.pi

        # print(((X_r - moon.X)**2+(Y_r - moon.Y)**2)**0.5)
        if curPhase < 0.005 and started == 0:
            started = 1
            # print('staaart')
        if abs(firePhi) <= rollAng and started == 1:
            F_r = -13000
            nX = (X_r - moon.X) * np.cos(-prevPhi) - (Y_r - moon.Y) * np.sin(-prevPhi)
            nY = (Y_r - moon.Y) * np.cos(-prevPhi) + (X_r - moon.X) * np.sin(-prevPhi)
            dPhi = math.atan2(nY, nX)
            firePhi += dPhi
            #
            #
            #
            print("RRRRRRRRR", ((X_r - moon.X)**2+(Y_r - moon.Y)**2)**0.5)
            #
            #
            #
        else:
            F_r = 0
        if accepted == 0 and ((moon.X - X_r) ** 2 + (moon.Y - Y_r) ** 2) ** 0.5 >= 0.5 * (
                (earth.X - moon.X) ** 2 + (earth.Y - moon.Y) ** 2) ** 0.5:
            accepted = 1
            # print('accepted', ((PS.rocket.Vx - earth.Vx) ** 2 + (PS.rocket.Vy - earth.Vy) ** 2) ** 0.5)
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
                if planet.name == "Earth":
                    eX = planet.X
                    eY = planet.Y
                if planet.name == "moon":
                    mX = planet.X
                    mY = planet.Y
                    mR = planet.Rc

            Phi_r = -math.pi / 2 + math.atan2(mY - PS.rocket.Y, mX - PS.rocket.X)
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

    # print(firePhi)
    if inside==0:
        return 0,0,0
    else:
        ER = math.atan2(Y_r - earth.Y, X_r - earth.X)
        nX = (PS.rocket.Vx - earth.Vx) * np.cos(-ER) - (PS.rocket.Vy - earth.Vy) * np.sin(-ER)
        nY = (PS.rocket.Vy - earth.Vy) * np.cos(-ER) + (PS.rocket.Vx - earth.Vx) * np.sin(-ER)
        VRM = math.atan2(nY, nX)

        EM = math.atan2(moon.Y - earth.Y, moon.X - earth.X)
        nX = (PS.rocket.X - earth.X) * np.cos(-EM) - (PS.rocket.Y - earth.Y) * np.sin(-EM)
        nY = (PS.rocket.Y - earth.Y) * np.cos(-EM) + (PS.rocket.X - earth.X) * np.sin(-EM)
        ERM = math.atan2(nY, nX)
        return ((PS.rocket.Vx - earth.Vx)**2+(PS.rocket.Vy - earth.Vy)**2)**0.5, VRM, ERM

def F(params, dt):
    pe, ae, pm, am = params
    vE, alphaE, betaE = GetFromEarth(pe, ae, dt)
    vM, alphaM, betaM = GetFromMoon(pm, am, -dt)
    return 0.1*(vE - vM)**2 + (alphaE - alphaM)**2 + (betaE - betaM)**2

startTime= time.localtime()
steps = [1, 5, 1, 4]    #0-phazeE
                                        #1-angE
                                        #2-phazeM
                                        #3-angM
# steps = [-2.980232238769531e-14, -1.4901161193847657e-13, -2.980232238769531e-14, -1.4901161193847657e-13]
# steps = [8.881784197001252e-22, 4.4408920985006265e-21, 8.881784197001252e-22, 4.4408920985006265e-21]
dt = 0.001
#tempParams = [-0.55875, 50.361875, 1.946875, 7.99658203125]
tempParams = [-0.55875, 50.31750000000004, 1.946875, 7.964082031249993]
tempParams = [-0.5556249999999999, 50.47843750000004, 1.946875, 7.960175781249993]
tempParams = [-1.376953125, 55.43743896484375, 4.066276041666669, 28.333333333333336] #37.59397757685488	# => 0.0031322279352359373


tempF = F(tempParams, dt)
print('start: ', tempParams, '=>', tempF)
for i in range(10000):
    # tempParams[2+i%2] += steps[2+i%2]
    tempParams[i%2] += steps[i%2]
    tempestF = F(tempParams, dt)
    print(i, tempParams, '\t =>', tempestF, '\t', steps)
    if tempestF >= tempF:
        # tempParams[2+i%2] -= steps[2+i%2]
        # steps[2+i%2] /=-2
        tempParams[i%2] -= steps[i%2]
        steps[i%2] /=-2
    else:
        tempF = tempestF
        print(tempParams, '\t =>', tempestF)

now = time.localtime()
print((now.tm_hour-startTime.tm_hour)*60+now.tm_min-startTime.tm_min)