import pickle
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import CreateSystem as design  # Это наш конвертированный файл дизайна
from Planetary3var import *


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        FileName = ""
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.LoadButton.clicked.connect(self.LoadButtonClicked)
        self.ApplyChangesButton.clicked.connect(self.ApplyButtonClicked)
        self.AddPlanetButton.clicked.connect(self.AddPlanetButtonClicked)
        self.RemovePlanetButton.clicked.connect(self.RemovePlanetButtonClicked)
        self.AddRockettButton.clicked.connect(self.AddRocketButtonClicked)
        self.RemoveRocketButton.clicked.connect(self.RemoveRocketButtonClicked)
        self.CreateButton.clicked.connect(self.SaveFileButtonClick)

        self.data = "Null"
        self.currentIndex = -1
        self.currentItem = "Null"
        self.isRocket = "Null"

        self.rocket = "Null"
        self.planets = "Null"
        self.ObjectList.currentRowChanged.connect(self.ItemChanging)

    def LoadButtonClicked(self):
        Filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")[0]
        if( Filename[-5]+Filename[-4]+Filename[-3]+Filename[-2]+Filename[-1]!=".psys"):
            print("Wrong file type, it must be *.psys")
            return
        print("Opened File: ", Filename)
        with open(Filename, 'rb') as file:
            self.data = pickle.load(file)['PS']
        if(self.data.rocket!="Null"):
            self.rocket = self.data.rocket
            self.AddRockettButton.setUpdatesEnabled(False)
            self.RemoveRocketButton.setUpdatesEnabled(True)
        else:
            self.AddRockettButton.setUpdatesEnabled(True)
            self.RemoveRocketButton.setUpdatesEnabled(False)
            self.rocket = "Null"
        self.planets = self.data.Planets
        self.ObjectList.clear()
        self.reloadList()

    def reloadList(self):
        self.ObjectList.clear()
        for i in range(len(self.planets)):
            self.ObjectList.addItem("planet: " + str(self.planets[i].name))
        if(self.rocket!="Null"):
            self.ObjectList.addItem("rocket: " + str(self.rocket.name))

    def ItemChanging(self, current_row):
        self.currentIndex = current_row
        if(current_row == len(self.planets)):
            self.currentItem = self.rocket
            self.isRocket = True
            self.TextMainColor.setText(str(self.currentItem.C_r[0]) + " " + str(self.currentItem.C_r[1]) + " " + str(self.currentItem.C_r[2]))
            self.TextSideColor.setText(str(self.currentItem.C_f[0]) + " " + str(self.currentItem.C_f[1]) + " " + str(self.currentItem.C_f[2]))
            #self.TextFRocket.setText(str(self.currentItem.Fmax)) //нет пока что фмакс
            self.TextSize.setText(str(self.currentItem.L))
        else:
            self.currentItem = self.planets[current_row]
            self.isRocket = False
            self.TextMainColor.setText(str(self.currentItem.C_p[0]) + " " + str(self.currentItem.C_p[1]) + " " + str(self.currentItem.C_p[2]))
            self.TextSideColor.setText(str(self.currentItem.C_a[0]) + " " + str(self.currentItem.C_a[1]) + " " + str(self.currentItem.C_a[2]))
            self.TextSize.setText(str(self.currentItem.Rc))
        self.TextMass.setText(str(self.currentItem.m))
        self.TextXY.setText(str(self.currentItem.X)+" "+str(self.currentItem.Y))
        self.TextVxy.setText(str(self.currentItem.Vx)+" "+str(self.currentItem.Vy))
        self.TextObjectName.setText(self.currentItem.name)

    def ApplyButtonClicked(self):
        coordinates = str.split(self.TextXY.toPlainText(), " ")
        self.currentItem.X = float(coordinates[0])
        self.currentItem.Y = float(coordinates[1])

        velocities = str.split(self.TextVxy.toPlainText(), " ")
        self.currentItem.Vx = float(velocities[0])
        self.currentItem.Vy = float(velocities[1])

        m = self.TextMass.toPlainText()
        self.currentItem.m = float(m)

        name = self.TextObjectName.toPlainText()
        self.currentItem.name = name

        maincolor = str.split(self.TextMainColor.toPlainText(), " ")
        sidecolor = str.split(self.TextSideColor.toPlainText(), " ")
        size = float(self.TextSize.toPlainText())
        if(self.isRocket == True):
            self.currentItem.C_r = [float(maincolor[0]),float(maincolor[1]),float(maincolor[2])]
            self.currentItem.C_r = [float(sidecolor[0]),float(sidecolor[1]),float(sidecolor[2])]
            self.currentItem.L = float(size)
        else:
            self.currentItem.Cp = [float(maincolor[0]),float(maincolor[1]),float(maincolor[2])]
            self.currentItem.Ca = [float(sidecolor[0]),float(sidecolor[1]),float(sidecolor[2])]
            self.currentItem.Rc = float(size)
        self.reloadList()

    def AddPlanetButtonClicked(self):
        coordinates = str.split(self.TextXY.toPlainText(), " ")
        velocities = str.split(self.TextVxy.toPlainText(), " ")
        m = self.TextMass.toPlainText()
        name = self.TextObjectName.toPlainText()
        maincolor = str.split(self.TextMainColor.toPlainText(), " ")
        sidecolor = str.split(self.TextSideColor.toPlainText(), " ")
        size = self.TextSize.toPlainText()

        tempPlanet = Planet(float(m), float(coordinates[0]), float(coordinates[1]),
                            float(velocities[0]), float(velocities[1]),
                            float(size), 1.1*float(size),
                            [float(maincolor[0]),float(maincolor[1]),float(maincolor[2])],
                            [float(sidecolor[0]),float(sidecolor[1]),float(sidecolor[2])],
                            name)

        if(self.planets == "Null"):
            self.planets = [tempPlanet]
        else:
            self.planets.append(tempPlanet)
        self.reloadList()

    def RemovePlanetButtonClicked(self):
        self.planets.pop(self.currentIndex)
        self.reloadList()

    def AddRocketButtonClicked(self):
        if(self.rocket=="Null"):
            coordinates = str.split(self.TextXY.toPlainText(), " ")
            velocities = str.split(self.TextVxy.toPlainText(), " ")
            m = self.TextMass.toPlainText()
            name = self.TextObjectName.toPlainText()
            maincolor = str.split(self.TextMainColor.toPlainText(), " ")
            sidecolor = str.split(self.TextSideColor.toPlainText(), " ")
            size = self.TextSize.toPlainText()

        tempRocket = Rocket(float(m), float(coordinates[0]), float(coordinates[1]),
                            float(velocities[0]), float(velocities[1]),
                            float(size),
                            [float(maincolor[0]),float(maincolor[1]),float(maincolor[2])],
                            [float(sidecolor[0]),float(sidecolor[1]),float(sidecolor[2])],
                            name)

        self.rocket = tempRocket
        self.reloadList()
        self.AddRockettButton.setUpdatesEnabled(False)
        self.RemoveRocketButton.setUpdatesEnabled(True)

    def RemoveRocketButtonClicked(self):
        self.rocket = "Null"
        self.reloadList()
        self.AddRockettButton.setUpdatesEnabled(True)
        self.RemoveRocketButton.setUpdatesEnabled(False)

    def SaveFileButtonClick(self):

        PS = PlanetSystem(self.planets)
        if(self.rocket != "Null"):
            PS.AddRocket(self.rocket)
        Filename = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить систему", "Planet System.psys", "*psys")[0]
        dict = {'PS': PS}
        with open(Filename,'wb') as file:
            pickle.dump(dict, file)
            print("Saved File: ", Filename)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


