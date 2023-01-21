import pickle
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def Rot2D(X,Y,phi):
    RotX = X*np.cos(phi) - Y*np.sin(phi)
    RotY = X*np.sin(phi) + Y*np.cos(phi)
    return RotX, RotY



class Planet:
    def __init__(self,m,X_0,Y_0,Vx_0,Vy_0,Rc, Ra,C_p,C_a,name):
        self.m = m
        self.X = X_0
        self.Y = Y_0
        self.Vx = Vx_0
        self.Vy = Vy_0
        self.X_0 = X_0
        self.Y_0 = Y_0
        self.Vx_0 = Vx_0
        self.Vy_0 = Vy_0
        self.Rc = Rc
        self.Ra = Ra
        self.C_p = C_p
        self.C_a = C_a
        self.Gp = 'Null'
        self.Ga = 'Null'
        self.name = name

        self.TraceX = np.array([X_0])
        self.TraceY = np.array([Y_0])

        phi = np.linspace(0,6.29,30)
        self.Circ_x = Rc*np.cos(phi)
        self.Circ_y = Rc*np.sin(phi)
        self.Atm_x = Ra*np.cos(phi)
        self.Atm_y = Ra*np.sin(phi)


    def DrawPlanet(self,axes):
        self.Gp = axes.plot(self.X + self.Circ_x, self.Y + self.Circ_y, color=self.C_p)[0]
        self.Gt = axes.plot(self.TraceX, self.TraceY, ':', color=self.C_p)[0]

        #self.Ga = axes.plot(self.X + self.Atm_x, self.Y + self.Atm_y, color = self.C_a)[0]


    def ReplacePlanet(self,axes):
        self.Gp.set_data(self.X + self.Circ_x, self.Y + self.Circ_y)

        self.TraceX = np.append(self.TraceX, self.X)
        self.TraceY = np.append(self.TraceY, self.Y)

        self.Gt.set_data(self.TraceX, self.TraceY)
        #self.Ga.set_data(self.X + self.Atm_x, self.Y + self.Atm_y)


class Rocket:
    def __init__(self,m, X_0, Y_0, Vx_0, Vy_0, L, C_r, C_f,name):
        self.m = m
        self.Phi = 0
        self.X = X_0
        self.Y = Y_0
        self.Vx = Vx_0
        self.Vy = Vy_0
        self.X_0 = X_0
        self.Y_0 = Y_0
        self.Vx_0 = Vx_0
        self.Vy_0 = Vy_0
        self.F = 0
        self.L = L
        self.C_r = C_r
        self.C_f = C_f
        self.Gp = 'Null'
        self.Ga = 'Null'
        self.name = name

        self.TraceX = np.array([X_0])
        self.TraceY = np.array([Y_0])

        phi = np.linspace(0,6.29,30)
        self.Shape_x = np.array([0.5,  0.4, -0.25, -0.35, -0.5, -0.45, -0.45,  -0.5, -0.35, -0.25,  0.4, 0.5]) * self.L
        self.Shape_y = np.array([  0, 0.09,  0.09,  0.18, 0.18,  0.09, -0.09, -0.18, -0.18, -0.09,-0.09,   0]) * self.L
        # self.Atm_x = Ra*np.cos(phi)
        # self.Atm_y = Ra*np.sin(phi)

        self.Flame_x = np.array([ 0, -0.1, -0.2, -0.15, -0.25, -0.15, -0.2, -0.1, 0])
        self.Flame_y = np.array([ 0.09, 0.1, 0.09, 0.05, 0, -0.05, -0.09, -0.1,  -0.09])



    def DrawRocket(self,axes):
        RShapeX, RShapeY = Rot2D(self.Shape_x, self.Shape_y, self.Phi)
        RFlameX, RFlameY = Rot2D((self.Flame_x * self.F - 0.45) * self.L, self.Flame_y * self.L, self.Phi)
        self.Gr = axes.plot(self.X + RShapeX, self.Y + RShapeY, color=self.C_r)[0]
        self.Gt = axes.plot(self.TraceX, self.TraceY, ':', color=self.C_r)[0]
        self.Gf = axes.plot(self.X + RFlameX, self.Y + RFlameY, color=self.C_f)[0]



        #self.Ga = axes.plot(self.X + self.Atm_x, self.Y + self.Atm_y, color = self.C_a)[0]


    def ReplaceRocket(self,axes):
        RShapeX, RShapeY = Rot2D(self.Shape_x, self.Shape_y, self.Phi)
        RFlameX, RFlameY = Rot2D((self.Flame_x * self.F - 0.45) * self.L, self.Flame_y * self.L, self.Phi)
        self.Gr.set_data(self.X + RShapeX, self.Y + RShapeY)
        self.Gf.set_data(self.X + RFlameX, self.Y + RFlameY)

        self.TraceX = np.append(self.TraceX, self.X)
        self.TraceY = np.append(self.TraceY, self.Y)

        self.Gt.set_data(self.TraceX, self.TraceY)
        #self.Ga.set_data(self.X + self.Atm_x, self.Y + self.Atm_y)




class PlanetSystem:
    def __init__(self, Planets, Gamma = 1):
        self.Planets = Planets
        self.EquationsOfMovement = 'Null'
        self.Gamma = Gamma
        self.EquationsOfRocket = 'Null'
        self.rocket = 'Null'

    def AddRocket(self, rocket):
        self.rocket = rocket

    def DrawSystem(self, axes):
        for planet in self.Planets:
            planet.DrawPlanet(axes)
        if self.rocket != 'Null':
            self.rocket.DrawRocket(axes)

    def ReplaceSystem(self, axes):
        for planet in self.Planets:
            planet.ReplacePlanet(axes)
        if self.rocket != 'Null':
            self.rocket.ReplaceRocket(axes)

    def GetEquationsOfMovement(self):

        X = sp.symbols('x:' + str(len(self.Planets)))
        Y = sp.symbols('y:' + str(len(self.Planets)))
        VX = sp.symbols('vx:' + str(len(self.Planets)))
        VY = sp.symbols('vy:' + str(len(self.Planets)))

        Dx  = [vx for vx in VX]
        Dy  = [vy for vy in VY]
        DDx = [0 for x in X]
        DDy = [0 for y in Y]

        for i in range(len(X)):
            for j in range(len(X)):
                if i != j:
                    DDx[i] += ((self.Gamma * self.Planets[j].m * (X[j] - X[i])) / (((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2) ** (3 / 2)))
                    DDy[i] += ((self.Gamma * self.Planets[j].m * (Y[j] - Y[i])) / (((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2) ** (3 / 2)))

        self.EquationsOfMovement = sp.lambdify([X, Y, VX, VY], [Dx, Dy, DDx, DDy], 'numpy')
        if self.rocket != 'Null':

            X_r = sp.Symbol('X_r')
            Y_r = sp.Symbol('Y_r')
            VX_r = sp.Symbol('VX_r')
            VY_r = sp.Symbol('VY_r')
            Phi_r = sp.Symbol("Phi_r")
            F_r = sp.Symbol("F_r")

            Dx_r = VX_r
            Dy_r = VY_r
            DDx_r = 0
            DDy_r = 0

            for j in range(len(X)):
                DDx_r += ((self.Gamma * self.Planets[j].m * (X[j] - X_r)) / (
                    ((X_r - X[j]) ** 2 + (Y_r - Y[j]) ** 2) ** (3 / 2)))
                DDy_r += ((self.Gamma * self.Planets[j].m * (Y[j] - Y_r)) / (
                    ((X_r - X[j]) ** 2 + (Y_r - Y[j]) ** 2) ** (3 / 2)))

            DDx_r += F_r * sp.cos(Phi_r)/self.rocket.m
            DDy_r += F_r * sp.sin(Phi_r)/self.rocket.m

            self.EquationsOfRocket = sp.lambdify([X, Y, VX, VY, X_r, Y_r, VX_r, VY_r, Phi_r, F_r],
                                                 [Dx_r, Dy_r, DDx_r, DDy_r], 'numpy')


Planet1 = Planet(1, -1.0, 0.0, 0.0,  0.485, 0.3, 0.4, [0,0,1], [0,  0,1], "p1")
Planet2 = Planet(1,  1.0, 0.0, 0.0, -0.485, 0.3, 0.4, [0,1,0], [0,  1,1], "p2")
Planet3 = Planet(2,  1.0, 1.0, 1.0, -0.485, 0.3, 0.4, [1,0,0], [0,  1,1], "p3")
# Rocket1 = Rocket(1,  0.1, 0.0, 0.0, 0.0, 1, [0,0,0], [0.8,0,0],"rocket")


PS = PlanetSystem([Planet1, Planet2, Planet3])
# PS.AddRocket(Rocket1)
# PS.rocket.F = 1


fimeName = "planet.psys"
dict = {'PS': PS}
with open(fimeName,'wb') as file:
    pickle.dump(dict, file)

# with open(fimeName,'rb') as file:
#     dict = pickle.load(file)
#
# PS = dict['PS']


PS.GetEquationsOfMovement()





fig = plt.figure(figsize=[13,7])
ax = fig.add_subplot(1,1,1)
ax.axis('equal')
ax.set(xlim = [-10,10], ylim = [-10,10])

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



PS.DrawSystem(ax)
dt = 0.01

Phi_r = 0
F_r = 0

def KadrPlanet(i):
    global Xs, Ys, VXs, VYs, PS, X_r,Y_r, VX_r, VY_r, Phi_r, F_r

    res = PS.EquationsOfMovement(Xs, Ys, VXs, VYs)
    k1_dX, k1_dY, k1_dVx, k1_dVy = np.array(res[0]),np.array(res[1]),np.array(res[2]),np.array(res[3])

    res = PS.EquationsOfMovement(Xs+k1_dX*dt/2, Ys+k1_dY*dt/2, VXs+k1_dVx*dt/2, VYs+k1_dVy*dt/2)
    k2_dX, k2_dY, k2_dVx, k2_dVy = np.array(res[0]),np.array(res[1]),np.array(res[2]),np.array(res[3])

    res = PS.EquationsOfMovement(Xs+k2_dX*dt/2, Ys+k2_dY*dt/2, VXs+k2_dVx*dt/2, VYs+k2_dVy*dt/2)
    k3_dX, k3_dY, k3_dVx, k3_dVy = np.array(res[0]),np.array(res[1]),np.array(res[2]),np.array(res[3])

    res = PS.EquationsOfMovement(Xs+k3_dX*dt, Ys+k3_dY*dt, VXs+k3_dVx*dt, VYs+k3_dVy*dt)
    k4_dX, k4_dY, k4_dVx, k4_dVy = np.array(res[0]),np.array(res[1]),np.array(res[2]),np.array(res[3])

    Xs += dt/6*(k1_dX+2*k2_dX+2*k3_dX+k4_dX)
    Ys += dt/6*(k1_dY+2*k2_dY+2*k3_dY+k4_dY)
    VXs += dt/6*(k1_dVx+2*k2_dVx+2*k3_dVx+k4_dVx)
    VYs += dt/6*(k1_dVy+2*k2_dVy+2*k3_dVy+k4_dVy)

    for planet,x, y, vx, vy in zip(PS.Planets, Xs, Ys, VXs, VYs):
        planet.X = x
        planet.Y = y
        planet.Vx = vx
        planet.Vy = vy

    if PS.rocket!='Null':
        Phi_r += dt
        F_r += dt
        res = PS.EquationsOfRocket(Xs, Ys, VXs, VYs, X_r, Y_r, VX_r, VY_r, Phi_r, F_r)
        k1_dX_r, k1_dY_r, k1_dVx_r, k1_dVy_r = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

        res = PS.EquationsOfRocket(Xs + k1_dX * dt / 2, Ys + k1_dY * dt / 2, VXs + k1_dVx * dt / 2,
                                     VYs + k1_dVy * dt / 2, X_r + k1_dX_r * dt / 2, Y_r +k1_dY_r * dt / 2, VX_r + k1_dVx_r * dt / 2, VY_r +k1_dVy_r * dt / 2, Phi_r, F_r)
        k2_dX_r, k2_dY_r, k2_dVx_r, k2_dVy_r = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

        res = PS.EquationsOfRocket(Xs + k2_dX * dt / 2, Ys + k2_dY * dt / 2, VXs + k2_dVx * dt / 2,
                                     VYs + k2_dVy * dt / 2, X_r + k2_dX_r * dt / 2, Y_r +k2_dY_r * dt / 2, VX_r + k2_dVx_r * dt / 2, VY_r +k2_dVy_r * dt / 2, Phi_r, F_r)
        k3_dX_r, k3_dY_r, k3_dVx_r, k3_dVy_r = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

        res = PS.EquationsOfRocket(Xs + k3_dX * dt, Ys + k3_dY * dt, VXs + k3_dVx * dt, VYs + k3_dVy * dt,
                                   X_r + k3_dX_r * dt, Y_r +k3_dY_r * dt, VX_r + k3_dVx_r * dt, VY_r +k3_dVy_r * dt, Phi_r, F_r)
        k4_dX_r, k4_dY_r, k4_dVx_r, k4_dVy_r = np.array(res[0]), np.array(res[1]), np.array(res[2]), np.array(res[3])

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

    PS.ReplaceSystem(ax)

    if PS.rocket!='Null':
        return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets] + [PS.rocket.Gr,PS.rocket.Gt,PS.rocket.Gf]
    else:
        return [planet.Gp for planet in PS.Planets] + [planet.Gt for planet in PS.Planets]


Animation1 = FuncAnimation(fig,KadrPlanet,interval=dt*1000,blit=True)





plt.show()





