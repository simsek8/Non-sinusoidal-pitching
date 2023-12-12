# mplwidget.py
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

class mplwidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvasQTAgg(Figure())
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)