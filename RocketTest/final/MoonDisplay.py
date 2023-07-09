import math
import pickle
import numpy as np
import time
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
from functools import partial
from finPlanetary import *

def orbDisplay(par, totalt):
    dt = par[0]
    searchOrb = par[3]

    ##
    fimeName = "WWW" + str(searchOrb) + ".psys"
    with open(fimeName, 'rb') as file:
        PS = pickle.load(file)['PS']
    ###
    searchOrb = (par[3]+15180)/6771000#15БЛИЗКО, 15.5 много
        #15200
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
    for planet in PS.Planets:
        if planet.name == "Earth":
            earth = planet
        if planet.name == "moon":
            moon = planet
    ErthX = np.array([])
    ErthY = np.array([])
    MoonX = np.array([])
    MoonY = np.array([])
    RockX = np.array([])
    RockY = np.array([])
    RockPhi = np.array([])

    time = np.array([])
    R = np.array([])
    on=1

    while abs(t)<totalt:#checkPhi<10*np.pi:
        print(t)
        Phase=par[1]
        RtoMoon = par[2]

        EM = math.atan2(earth.Y - moon.Y, earth.X - moon.X)
        nX = (X_r - moon.X) * np.cos(-EM) - (Y_r - moon.Y) * np.sin(-EM)
        nY = (Y_r - moon.Y) * np.cos(-EM) + (X_r - moon.X) * np.sin(-EM)
        ERM = math.atan2(nY, nX)
        Phi_r = -math.pi / 2 + math.atan2(moon.Y - PS.rocket.Y, moon.X - PS.rocket.X)

        if ((X_r - moon.X)**2+(Y_r - moon.Y)**2)**0.5>searchOrb+moon.Rc and on==1:
            F_r = -13000
        else:
            on=0
            F_r = 0

        ErthX = np.append(ErthX, earth.X)
        ErthY = np.append(ErthY, earth.Y)
        MoonX = np.append(MoonX, moon.X)
        MoonY = np.append(MoonY, moon.Y)
        RockX = np.append(RockX, X_r)
        RockY = np.append(RockY, Y_r)
        RockPhi = np.append(RockPhi, Phi_r)

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

    print('t:', t)

    return ErthX, ErthY, MoonX, MoonY, RockX, RockY, time, R, RockPhi


def Kadr(PS, earth, moon, rock, center, coords, ax, frame):
    print(frame)
    rock.Phi = coords[8][int(frame)]
    earth.X, earth.Y, moon.X, moon.Y, rock.X, rock.Y = coords[0][int(frame)], coords[1][int(frame)], coords[2][int(frame)], \
                                                       coords[3][int(frame)], coords[4][int(frame)], coords[5][int(frame)]
    PS.ReplaceSystem(ax, center)
    return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets] + [PS.rocket.Gr,
                                                                                          PS.rocket.Gt,
                                                                                          PS.rocket.Gf]


tempParams = [0.001, 0.5+np.pi/4, 7.5, 40000]#5hu
# tempParams = [0.001, -2.5+np.pi/2, 8, 400000]#5
# tempParams = [0.001, 2+np.pi/2, 8.5, 800000]#5
# tempParams = [0.001, 0.3+np.pi/2, 9, 1600000]#5
# tempParams = [0.001, -1.+np.pi/2, 9.5, 3200000]#5
# tempParams = [0.001, -1.5+np.pi/4, 10, 6400000]#5
lims = 0.5
searchOrb = tempParams[3]
totalT = 35
kadrSkip = 20
dt = 0.001
res = orbDisplay(tempParams, totalT)


##
fimeName = "WWW" + str(searchOrb) + ".psys"
with open(fimeName, 'rb') as file:
    PS = pickle.load(file)['PS']
###


fig = plt.figure()
fig.canvas.manager.full_screen_toggle() # toggle fullscreen mode
axM = plt.subplot2grid((1, 1), (0, 0))
axM.set_aspect('equal', 'box')
axM.set(xlim=(-lims,lims), ylim=(-lims, lims))

for planet in PS.Planets:
    if planet.name == "Earth":
        Ea2 = planet
    if planet.name == "moon":
        Mo2 = planet
Ro2 = PS.rocket
PS.DrawSystem(axM, Mo2)
anim2 = FuncAnimation(fig, partial(Kadr, PS, Ea2, Mo2, Ro2, Mo2, res, axM), np.linspace(0, totalT/0.001, int((totalT/0.001)/kadrSkip), dtype=np.int64),  blit=True)

plt.show()
