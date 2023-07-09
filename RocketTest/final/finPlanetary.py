import numpy as np
import sympy as sp


def Rot2D(X,Y,phi):
    RotX = X*np.cos(phi) - Y*np.sin(phi)
    RotY = X*np.sin(phi) + Y*np.cos(phi)
    return RotX, RotY


class Planet:
    def __init__(self,m,X_0,Y_0,Vx_0,Vy_0,Rc, Ra,C_p,C_a, name):
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

    def DrawPlanet(self, axes, Center):
        self.Gp = axes.plot(self.X - Center[0] + self.Circ_x, self.Y - Center[1] + self.Circ_y, color=self.C_p)[0]
        self.TraceX -= Center[0]
        self.TraceY -= Center[1]
        self.Gt = axes.plot(self.TraceX, self.TraceY, ':', color=self.C_p)[0]

        #self.Ga = axes.plot(self.X + self.Atm_x, self.Y + self.Atm_y, color = self.C_a)[0]

    def ReplacePlanet(self, axes, Center):
        self.Gp.set_data(self.X - Center[0] + self.Circ_x, self.Y - Center[1] + self.Circ_y)

        self.TraceX = np.append(self.TraceX, self.X - Center[0])
        self.TraceY = np.append(self.TraceY, self.Y - Center[1])

        self.Gt.set_data(self.TraceX, self.TraceY)
        #self.Ga.set_data(self.X + self.Atm_x, self.Y + self.Atm_y)


class Rocket:
    def __init__(self,m, X_0, Y_0, Vx_0, Vy_0, L, C_r, C_f, name):
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

    def DrawRocket(self, axes, Center):
        RShapeX, RShapeY = Rot2D(self.Shape_x, self.Shape_y, self.Phi)
        RFlameX, RFlameY = Rot2D((self.Flame_x * self.F - 0.45) * self.L, self.Flame_y * self.L, self.Phi)
        self.Gr = axes.plot(self.X - Center[0] + RShapeX, self.Y - Center[1] + RShapeY, color=self.C_r)[0]
        self.TraceX -= Center[0]
        self.TraceY -= Center[1]
        self.Gt = axes.plot(self.TraceX, self.TraceY, ':', color=self.C_r)[0]
        self.Gf = axes.plot(self.X - Center[0] + RFlameX, self.Y - Center[1] + RFlameY, color=self.C_f)[0]



        #self.Ga = axes.plot(self.X + self.Atm_x, self.Y + self.Atm_y, color = self.C_a)[0]

    def ReplaceRocket(self, axes, Center):
        RShapeX, RShapeY = Rot2D(self.Shape_x, self.Shape_y, self.Phi)
        RFlameX, RFlameY = Rot2D((self.Flame_x * self.F - 0.45) * self.L, self.Flame_y * self.L, self.Phi)
        self.Gr.set_data(self.X - Center[0] + RShapeX, self.Y - Center[1] + RShapeY)
        self.Gf.set_data(self.X - Center[0] + RFlameX, self.Y - Center[1] + RFlameY)

        self.TraceX = np.append(self.TraceX, self.X - Center[0])
        self.TraceY = np.append(self.TraceY, self.Y - Center[1])

        self.Gt.set_data(self.TraceX, self.TraceY)
        #self.Ga.set_data(self.X + self.Atm_x, self.Y + self.Atm_y)


class PlanetSystem:
    def __init__(self, Planets, omega = 1/5400, r0 = 6771000, Gamma = 6.6743015*(10**-11)):
        self.Planets = Planets
        self.EquationsOfMovement = 'Null'
        self.Gamma = Gamma
        self.EquationsOfRocket = 'Null'
        self.rocket = 'Null'
        self.Omega = omega
        self.R0 = r0

    def AddRocket(self, rocket):
        self.rocket = rocket

    def DrawSystem(self, axes, center):
        cX = center.X
        cY = center.Y
        print(3)
        for planet in self.Planets:
            planet.DrawPlanet(axes, [cX, cY])
        if self.rocket != 'Null':
            self.rocket.DrawRocket(axes, [cX, cY])

    def ReplaceSystem(self, axes, center):
        cX = center.X
        cY = center.Y
        for planet in self.Planets:
            planet.ReplacePlanet(axes, [cX, cY])
        if self.rocket != 'Null':
            self.rocket.ReplaceRocket(axes, [cX, cY])

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
                    DDx[i] += (self.Gamma * self.Planets[j].m / self.Omega**2 / self.R0**3) * (X[j] - X[i]) / (((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2) ** (3 / 2))
                    DDy[i] += (self.Gamma * self.Planets[j].m / self.Omega**2 / self.R0**3) * (Y[j] - Y[i]) / (((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2) ** (3 / 2))

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
                DDx_r += (self.Gamma * self.Planets[j].m / self.Omega**2 / self.R0**3) * (X[j] - X_r) / (
                    ((X_r - X[j]) ** 2 + (Y_r - Y[j]) ** 2) ** (3 / 2))
                DDy_r += (self.Gamma * self.Planets[j].m / self.Omega**2 / self.R0**3) * (Y[j] - Y_r) / (
                    ((X_r - X[j]) ** 2 + (Y_r - Y[j]) ** 2) ** (3 / 2))

            DDx_r += F_r * sp.cos(Phi_r)/self.rocket.m / self.Omega**2 / self.R0
            DDy_r += F_r * sp.sin(Phi_r)/self.rocket.m / self.Omega**2 / self.R0

            self.EquationsOfRocket = sp.lambdify([X, Y, VX, VY, X_r, Y_r, VX_r, VY_r, Phi_r, F_r],
                                                 [Dx_r, Dy_r, DDx_r, DDy_r], 'numpy')