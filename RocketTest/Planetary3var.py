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


class Moon:
    def __init__(self,m,X_0,Y_0,Vx_0,Vy_0,Rc, Ra,C_p,C_a):
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

        self.TraceX = np.array([X_0])
        self.TraceY = np.array([Y_0])

        phi = np.linspace(0,6.29,30)
        self.Circ_x = Rc*np.cos(phi)
        self.Circ_y = Rc*np.sin(phi)
        self.Atm_x = Ra*np.cos(phi)
        self.Atm_y = Ra*np.sin(phi)

    def DrawMoon(self,axes):
        self.Gp = axes.plot(self.X + self.Circ_x, self.Y + self.Circ_y, color=self.C_p)[0]
        self.Gt = axes.plot(self.TraceX, self.TraceY, ':', color=self.C_p)[0]

    def ReplaceMoon(self,axes):
        self.Gp.set_data(self.X + self.Circ_x, self.Y + self.Circ_y)

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
        self.EquationsOfMoons = 'Null'
        self.rocket = 'Null'
        self.Moons = 'Null'

    def AddRocket(self, rocket):
        self.rocket = rocket

    def AddMoons(self, moons):
        self.Moons = moons


    def DrawSystem(self, axes):
        for planet in self.Planets:
            planet.DrawPlanet(axes)
        for moon in self.Moons:
            moon.DrawMoon(axes)
        if self.rocket != 'Null':
            self.rocket.DrawRocket(axes)

    def ReplaceSystem(self, axes):
        for planet in self.Planets:
            planet.ReplacePlanet(axes)
        for moon in self.Moons:
            moon.ReplaceMoon(axes)
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


        Xm = sp.symbols('x_m:' + str(len(self.Moons)))
        Ym = sp.symbols('y_m:' + str(len(self.Moons)))
        VXm = sp.symbols('vx_m:' + str(len(self.Moons)))
        VYm = sp.symbols('vy_m:' + str(len(self.Moons)))

        Dxm  = [vx_m for vx_m in VXm]
        Dym  = [vy_m for vy_m in VYm]
        DDxm = [0 for x_m in Xm]
        DDym = [0 for y_m in Ym]
        print('eq1')
        print(len(Xm))
        for i in range(len(Xm)):
            for j in range(len(X)):
                DDxm[i] += ((self.Gamma * self.Planets[j].m * (X[j] - Xm[i])) / (
                        ((Xm[i] - X[j]) ** 2 + (Ym[i] - Y[j]) ** 2) ** (3 / 2)))
                DDym[i] += ((self.Gamma * self.Planets[j].m * (Y[j] - Ym[i])) / (
                        ((Xm[i] - X[j]) ** 2 + (Ym[i] - Y[j]) ** 2) ** (3 / 2)))
        print('eq2')
        self.EquationsOfMoons = sp.lambdify([X, Y, VX, VY, Xm, Ym, VXm, VYm],
                                                 [Dxm, Dym, DDxm, DDym], 'numpy')
        print('eq3')