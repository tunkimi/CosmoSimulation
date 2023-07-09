from PyQt5.QtWidgets import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib import pyplot as plt

from matplotlib.figure import Figure


class SpaceWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        fig = plt.figure()
        axE = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=2)
        axM = plt.subplot2grid((2, 3), (0, 2))
        axR = plt.subplot2grid((2, 3), (1, 2))

        self.canvas = FigureCanvas(fig)


        # axEarth.plot(np.linspace(1,5,100), np.linspace(-3,3,100))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)



        self.canvas.axEarth = axE
        self.canvas.axMoon = axM
        self.canvas.axRocket = axR


        self.setLayout(vertical_layout)