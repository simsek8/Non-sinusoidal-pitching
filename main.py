import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QLineEdit, QCheckBox, QSlider, QLabel
import sys
from PyQt6 import uic
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

from jacobi import jacobi_sn
from mplwidget import mplwidget

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('Window.ui', self)
        #self.lineedit = self.findChild(QLineEdit, 'lineEdit')
        self.mpl = self.findChild(mplwidget, 'mplwidget')
        self.addToolBar(NavigationToolbar2QT(self.mplwidget.canvas, self))
        self.label_jacobi1 = self.findChild(QLabel, 'label')
        self.sincheck = self.findChild(QCheckBox, 'checkBox')
        self.checkbox2 = self.findChild(QCheckBox, 'checkBox_2')
        self.checkbox3 = self.findChild(QCheckBox, 'checkBox_3')
        self.slider1 = self.findChild(QSlider, 'horizontalSlider')
        self.slider2 = self.findChild(QSlider, 'horizontalSlider_2')

        self.sincheck.stateChanged.connect(self.update_graph_wrapper)
        self.checkbox2.stateChanged.connect(self.update_graph_wrapper)
        self.checkbox3.stateChanged.connect(self.update_graph_wrapper)

        if self.sincheck.isChecked():
            self.update_graph(self.slider1.value(), self.slider2.value())
        if self.checkbox2.isChecked():
            self.update_graph(self.slider1.value(), self.slider2.value())
        if self.checkbox3.isChecked():
            self.update_graph(self.slider1.value(), self.slider2.value())


        self.slider1.valueChanged.connect(lambda value: self.update_label1(value, self.label))
        self.slider2.valueChanged.connect(lambda value: self.update_label2(value, self.label_2))

    def update_graph_wrapper(self):
        # Wrapper function to avoid recursive calls during initialization
        if not self._initializing:
            self.update_graph()

    def update_label1(self, value, label):
        # Update the label text based on the slider value
        k1_value = value / 100.0  # Adjust this scaling factor based on your needs
        label.setText(f'{k1_value:.2f}')
        self.update_graph(k1_value,self.slider2.value())

    def update_label2(self, value, label):
        # Update the label text based on the slider value
        k2_value = value / 100.0  # Adjust this scaling factor based on your needs
        label.setText(f'{k2_value:.2f}')
        self.update_graph(self.slider1.value(), k2_value)

    def update_graph(self, k1_value, k2_value):
        chord = 1
        max_pitch_angle = 8
        reynolds = 10000
        u_inf = 0.06
        strouhal = 0.35
        nu = u_inf * chord / reynolds
        frequency = strouhal * u_inf / (2 * chord * np.sin(max_pitch_angle * np.pi / 180.0))
        period = 1 / frequency
        t = np.linspace(0, 1 * period, 300)
        sinus = np.sin(2 * np.pi * t / period)
        jacobi1 = t / period, jacobi_sn(k1_value, t, period)
        jacobi2 = t / period, jacobi_sn(k2_value, t, period)

        self.mplwidget.canvas.axes.clear()
        if self.sincheck.isChecked():
            self.mplwidget.canvas.axes.plot(t / period, sinus, linewidth=1.5, label=r"$\sin(t)$", color='k')
        if self.checkbox2.isChecked():
            self.mplwidget.canvas.axes.plot(jacobi1[0], jacobi1[1], linewidth=1.5,label=f"$sn, K={0.75}$")
        if self.checkbox3.isChecked():
            self.mplwidget.canvas.axes.plot(jacobi2[0], jacobi2[1], linewidth=1.5, label=f"$sn, K={0.3}$")
        self.mplwidget.canvas.axes.set_title(r'$sin$ vs $sn$', fontsize=16)
        self.mplwidget.canvas.axes.set_xlabel(r'$t / T$', fontsize=16)
        self.mplwidget.canvas.axes.set_ylabel(r'$\theta / \theta_{max}$', fontsize=16)
        self.mplwidget.canvas.axes.axhline(y=0, color="black", linestyle="-", linewidth=1)
        self.mplwidget.canvas.axes.legend(fontsize=14)
        self.mplwidget.canvas.draw()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())