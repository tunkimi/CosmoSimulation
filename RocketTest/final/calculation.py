import numpy as np
import math
import pickle

def Calculate(par, PS, totalT):
    Filename = 'Universe1.psys'
    with open(Filename, 'rb') as file:
        PS = pickle.load(file)['PS']
    dt = par[0]
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

    while t<totalT:
        # print(t)
        AngE = par[1]
        PhaseE = par[2]
        AngM = par[3]
        Rtomoon = par[4]

        ErthX = np.append(ErthX, earth.X)
        ErthY = np.append(ErthY, earth.Y)
        MoonX = np.append(MoonX, moon.X)
        MoonY = np.append(MoonY, moon.Y)
        RockX = np.append(RockX, X_r)
        RockY = np.append(RockY, Y_r)

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
    print('t caculated:', t)
    return ErthX, ErthY, MoonX, MoonY, RockX, RockY
