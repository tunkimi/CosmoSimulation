from matplotlib import pyplot as plt
import pandas as pd
fig = plt.figure()
ax1 = fig.add_subplot(1,3,1)
ax1.set(title='Скорость на середине расстояния')
ax2 = fig.add_subplot(1,3,2)
ax2.set(title='Угол скорости к нормали до Земли')
ax3 = fig.add_subplot(1,3,3)
ax3.set(title='Угол ракета-Земля-Луна')

fileway1 = 'C:/Users/iTunkimi/Desktop/GitReps/CosmoSimulation/RocketTest/fromMoon_0.01_0-2pi-50new.csv'
fileway2 = 'C:/Users/iTunkimi/Desktop/GitReps/CosmoSimulation/RocketTest/TVrPhir_0.01_0-2pi-629-47.79new.csv'

df1 = pd.read_csv(fileway1)
df2 = pd.read_csv(fileway2)

ax1.plot(df1['t'], df1['Vr'])
ax2.plot(df1['t'], df1['Alphar'])
ax3.plot(df1['t'], df1['Betar'])

removal = 1
head = df2['t'][-1]



ax1.plot(df2['t'], df2['Vr'])
ax2.plot(df2['t'], df2['Alphar'])
ax3.plot(df2['t'], df2['Betar'])

ax1.grid()
ax2.grid()
ax3.grid()

plt.show()