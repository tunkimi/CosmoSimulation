from Planetary import *
import pickle

#Moon
mMass = 7.3477 * (10**22)
mX0 = 384467000
mY0 = 0
mVx0 = 0
mVy0 = 1023-12.585 + 1.4958726415
mR = 1737100
mName = "moon"
#2137100

#Earth
eMass = 5.9726 * (10**24)
eX0 = 0
eY0 = 0
eVx0 = 0
eVy0 = -12.585
eR = 6371000
eName = "Earth"


#Rocket1
rMass = 300000
rX0 = -eR-400000
rY0 = 0
rVx0 = 0 + eVx0
rVy0 = -7700 + eVy0
rR = 100
rName = "Rocket"


r0 = eR + 400000
omega = 1/5400
gamma = 6.6743015 * (10 ** -11)

#System
Earth = Planet(eMass, eX0/r0, eY0/r0, eVx0/r0/omega, eVy0/r0/omega, eR/r0, eR/r0, [0.5, 1, 1], [0.5, 1, 1], eName)
Moon = Planet(mMass, mX0/r0, mY0/r0, mVx0/r0/omega, mVy0/r0/omega, mR/r0, mR/r0, [0.7, 0.7, 0.7], [0.7, 0.7, 0.7], mName)

Rocket1 = Rocket(rMass, rX0/r0, rY0/r0, rVx0/r0/omega, rVy0/r0/omega, rR/r0, [1, 0.5, 0.3], [1, 0.5, 0.3], rName)

PS = PlanetSystem([Earth, Moon], omega, r0, gamma, eName)
PS.AddRocket(Rocket1)

fimeName = "Universe1.psys"
dict = {'PS': PS}
with open(fimeName,'wb') as file:
    pickle.dump(dict, file)



# #Rocket2
# rMass = 300000
# rX0 = mX0 + mR + 400000
# rY0 = 0
# rVx0 = 0 + mVx0
# rVy0 = +1510 + mVy0
# rR = 100
# rName = "Rocket"


RocketR = 400*(2**4)#6400000#399000
rMass = 300000
rX0 = mX0  # + mR + RocketR
rY0 = mR + RocketR  # 0
rVx0 = mVx0 - (gamma * mMass / (mR + RocketR)) ** 0.5
rVy0 = mVy0  # +1510#(gamma*mMass/(mR+RocketR))**0.5#1510
rR = 100
rName = "Rocket"

Rocket2 = Rocket(rMass, rX0/r0, rY0/r0, rVx0/r0/omega, rVy0/r0/omega, rR/r0, [1, 0.5, 0.3], [1, 0.5, 0.3], rName)

PS = PlanetSystem([Earth, Moon], omega, r0, gamma, mName)
PS.AddRocket(Rocket2)

fimeName = "Universe2.psys"
dict = {'PS': PS}
with open(fimeName,'wb') as file:
    pickle.dump(dict, file)