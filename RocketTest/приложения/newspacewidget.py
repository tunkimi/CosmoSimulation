from PyQt5.QtWidgets import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib import pyplot as plt

from matplotlib.figure import Figure



class SpaceWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes1 = self.canvas.figure.add_subplot(121)
        self.canvas.axes2 = self.canvas.figure.add_subplot(122)
        self.setLayout(vertical_layout)