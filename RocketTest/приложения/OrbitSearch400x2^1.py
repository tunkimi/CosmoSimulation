import math
import pickle
import numpy as np
import time
import pickle


def orbErr(par, neededOrb):
    dt = par[0]

    Filename = 'Universe1.psys'
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
    Phi_r = 0
    F_r = 0
    ErrSum = 0
    ErrN = 0
    started = 0
    moonstarted = 0
    moonended = 0
    for planet in PS.Planets:
        if planet.name == "Earth":
            earth = planet
        if planet.name == "moon":
            moon = planet
    prevPhi = math.atan2(Y_r - earth.Y, X_r - earth.X)
    checkPhi = 0
    fullRolls = 0

    while t<100:#checkPhi<10*np.pi:
        AngE = par[1]  # 50.31632812500004  # 50.69
        PhaseE = par[2]  # -0.56375  # -0.59 #-0.5 #-0.45
        AngM = par[3]  # 7.960175781249993
        # PhaseM = 1.946875
        Rtomoon = par[4]  # 2.114366108798941


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
            # print('r', ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2) ** 0.5)
            if moonstarted == 0 and ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2) ** 0.5 <= Rtomoon:
                # print('STAAAAARTED')
                moonstarted = 1
                prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                fireMPhi = 0
                # print('prefly')
            elif moonstarted == 1 and abs(fireMPhi) <= AngM: #((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2)**0.5>0.27:
                F_r = -13000
                nX = (X_r - moon.X) * np.cos(-prevPhi) - (Y_r - moon.Y) * np.sin(-prevPhi)
                nY = (Y_r - moon.Y) * np.cos(-prevPhi) + (X_r - moon.X) * np.sin(-prevPhi)
                dPhi = math.atan2(nY, nX)
                fireMPhi += dPhi
                prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                # print('stopping')
            elif abs(fireMPhi) > AngM:
                nX = (X_r - moon.X) * np.cos(-prevPhi) - (Y_r - moon.Y) * np.sin(-prevPhi)
                nY = (Y_r - moon.Y) * np.cos(-prevPhi) + (X_r - moon.X) * np.sin(-prevPhi)
                dPhi = math.atan2(nY, nX)
                checkPhi += dPhi
                ErrSum += (neededOrb - ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2) ** 0.5)**2
                ErrN += 1
                prevPhi = math.atan2(Y_r - moon.Y, X_r - moon.X)
                moonended = 1
                fullRolls += dPhi
                # print('rolling')
            if moonended == 1 and ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2)**0.5 > 10:
                print('пролёт около луны')
                return 100000
                if ErrN == 0:
                    return 100000
                return ErrSum/fullRolls
            if moonstarted == 0 and ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2)**0.5 > ((earth.Y - moon.Y) ** 2 + (earth.X - moon.X) ** 2)**0.5:
                print('пролёт мимо луны')
                return 100000
                if ErrN == 0:
                    return 100000
                return ErrSum/fullRolls

            if ((Y_r - moon.Y) ** 2 + (X_r - moon.X) ** 2)**0.5 < 0.93*neededOrb:#moon.Rc:
                print('столкновение')
                return 100000
                if ErrN == 0:
                    return 100000
                return ErrSum/fullRolls

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

    if ErrN == 0:
        return 100000
    fullRolls /= 2*np.pi
    print('err', ErrSum/fullRolls)
    return ErrSum/fullRolls
    return ErrSum/ErrN
#0.3156254615 - 400км
r0 = 6771000

rasstkm = 400*(2**1)

calcOrb = (rasstkm*1000 + 1737100)/r0 #400*2**1км
print(calcOrb)

tempPars = [0.001, 50.31940429687504, -0.569375, 8.61267578125002, 2.14678798379894]
tempPars = [0.001, 50.31664550781318, -0.5670703125000086, 6.189003906250055, 2.170303608798931] #- идем к 400*2**1км
steps = [0.1, 0.01, 0.03, 0.01]
res = orbErr(tempPars, calcOrb)
tempestPars = tempPars
print(tempPars, res)
f = open("new"+str(rasstkm)+'kmsearch.txt','w')
for i in range(1000):
    print(i,':')
    f.write(str(i)+':\n')
    tempestPars[1+i%4] += steps[i%4]
    tempRes = orbErr(tempestPars, calcOrb)
    print(tempPars, ':', tempRes)
    f.write(str(tempPars)+' : '+ str(tempRes)+'\n')
    if abs(tempRes)<abs(res):
        res = tempRes
        tempPars = tempestPars
        print(tempPars, res)
        f.write('good: '+str(tempPars)+' : '+ str(tempRes)+'\n')
    else:
        tempestPars[1+i%4] -= steps[i%4]
        steps[i%4] /=-2
