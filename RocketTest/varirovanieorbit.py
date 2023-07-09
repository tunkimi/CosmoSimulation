from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
from functools import partial
from finPlanetary import *

def orbiit(PS, dt):
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
    Phi_r = PS.rocket.Phi
    F_r = 0
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

    while t<100:
        print('r', ((moon.X-X_r)**2+(moon.Y-Y_r))*0.5, '\nmoon', moon.X, moon.Y)
        ErthX = np.append(ErthX, earth.X)
        ErthY = np.append(ErthY, earth.Y)
        MoonX = np.append(MoonX, moon.X)
        MoonY = np.append(MoonY, moon.Y)
        RockX = np.append(RockX, X_r)
        RockY = np.append(RockY, Y_r)
        RockPhi = np.append(RockPhi, Phi_r)

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

    # print('t:', t)
    return ErthX, ErthY, MoonX, MoonY, RockX, RockY, time, R, RockPhi

#Moon
mMass = 7.3477 * (10**22)
mX0 = 384467000
mY0 = 0
mVx0 = 0
mVy0 = 1023-12.585 + 1.4958726415
mR = 1737100
mName = "moon"

#Earth
eMass = 5.9726 * (10**24)
eX0 = 0
eY0 = 0
eVx0 = 0
eVy0 = -12.585
eR = 6371000
eName = "Earth"

r0 = eR + 400000
omega = 1/5400
gamma = 6.6743015 * (10 ** -11)

#Rocket1
rMass = 300000
rX0 = mX0 + 400000
rY0 = 0
rVx0 = 0 + mVx0
rVy0 = mVy0 + (gamma*mMass/(((mX0-rX0)**2+(mY0-rY0)**2)**0.5)**2)
rR = 100000
rName = "Rocket"


#System
Earth = Planet(eMass, eX0/r0, eY0/r0, eVx0/r0/omega, eVy0/r0/omega, eR/r0, eR/r0, [0.5, 1, 1], [0.5, 1, 1], eName)
Moon = Planet(mMass, mX0/r0, mY0/r0, mVx0/r0/omega, mVy0/r0/omega, mR/r0, mR/r0, [0.7, 0.7, 0.7], [0.7, 0.7, 0.7], mName)

Rocket1 = Rocket(rMass, rX0/r0, rY0/r0, rVx0/r0/omega, rVy0/r0/omega, rR/r0, [1, 0.5, 0.3], [1, 0.5, 0.3], rName)
# Rocket1.Phi = -np.pi/2

PS = PlanetSystem([Earth, Moon], omega, r0, gamma)
PS.AddRocket(Rocket1)

for planet in PS.Planets:
    if planet.name =="Earth":
        Ea = planet
    if planet.name =="moon":
        Mo = planet
Ro = PS.rocket

res = orbiit(PS, dt=0.01)

fig = plt.figure()
ax = plt.subplot()
ax.set_aspect('equal', 'box')
ax.set(xlim=(-1, 1), ylim=(-1, 1))
def Kadr(PS, earth, moon, rock, center, coords, ax, frame):
    print(frame)
    rock.Phi = coords[8][int(frame)]
    earth.X, earth.Y, moon.X, moon.Y, rock.X, rock.Y = coords[0][int(frame)], coords[1][int(frame)], coords[2][int(frame)], \
                                                       coords[3][int(frame)], coords[4][int(frame)], coords[5][int(frame)]
    PS.ReplaceSystem(ax, center)
    return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets] + [PS.rocket.Gr,
                                                                                          PS.rocket.Gt,
                                                                                          PS.rocket.Gf]

PS.DrawSystem(ax, Mo)
FuncAnimation(fig, partial(Kadr, PS, Ea, Mo, Ro, Ro, res, ax),
              np.linspace(0, 100/0.001, int((100/0.001)/20), dtype=np.int64),  blit=True)


plt.show()

