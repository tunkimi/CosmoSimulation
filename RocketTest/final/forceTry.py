import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import *
import twoFinalProg as LoadSystem
import math
from matplotlib.animation import FuncAnimation
import pickle
from functools import partial
from matplotlib import gridspec
import calculation




fig = plt.figure()
axE = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=2)
axM = plt.subplot2grid((2, 3), (0, 2))
axR = plt.subplot2grid((2, 3), (1, 2))

Filename = 'Universe1.psys'
with open(Filename, 'rb') as file:
    Syst1 = pickle.load(file)['PS']
for planet in Syst1.Planets:
    if planet.name == "Earth":
        earth = planet
    if planet.name == "moon":
        moon = planet
rocket = Syst1.rocket

axE.set_aspect('equal', 'box')
axE.set(xlim=(-60, 60), ylim=(-60, 60))

# axM.set_aspect('equal', 'box')
# axM.set(xlim=(-02.25, 02.25), ylim=(-02.25, 02.25))
#
# axR.set_aspect('equal', 'box')
# axR.set(xlim=(-0.25, 0.25), ylim=(-0.25, 0.25))

Syst1.DrawSystem(axE, earth)

totalt = 100
cadrSkip = 20

Params = [0.001, 50.31865814208989, -0.5670703125000086, 7.918574218750057, 2.141426655673945]
res = calculation.Calculate(Params, Syst1, totalt)

# print(res[5])

def Kadr(PS1, ea, mo, ro, coords, axe, frame):
    # print(frame)
    ea.X, ea.Y, mo.X, mo.Y, ro.X, ro.Y = coords[0][int(frame)], coords[1][int(frame)], coords[2][int(frame)], \
                                                       coords[3][int(frame)], coords[4][int(frame)], coords[5][int(frame)]
    PS1.ReplaceSystem(axe, ea)

    return [planet.Gp for planet in PS1.Planets] + [planet.Gt for planet in PS1.Planets] + [PS1.rocket.Gr,
                                                                                            PS1.rocket.Gt,
                                                                                            PS1.rocket.Gf]

anim = FuncAnimation(fig, partial(Kadr, Syst1, earth, moon, rocket, res, axE), frames=np.linspace(0, totalt/Params[0], int((totalt/Params[0])/cadrSkip), dtype=np.int64),  blit=True)




plt.show()


