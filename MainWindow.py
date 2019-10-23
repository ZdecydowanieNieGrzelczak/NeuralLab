import sys, math
from PyQt5.QtWidgets import (QPushButton, QWidget, QLineEdit, QApplication, QSlider, QLabel, QToolTip, QSizePolicy,\
                             QRadioButton, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import (QFont)
from PyQt5.QtCore import (Qt, pyqtSignal)


from MyGraph import MyGraph
from MyClassConstructor import MyClassConstructor
from Neuron import Neuron

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import random
import time


random.seed(time.time())


class MainWindow(QWidget):


    def __init__(self):
        super().__init__()
        self.class_1_construction = MyClassConstructor(self, 100, 200, 'color: blue', 1)
        self.class_0_construction = MyClassConstructor(self, 100, 100, 'color: red', 0)
        self.graph = MyGraph(self)
        self.graph_button = QPushButton('Create graph', self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GUI")
        self.setFixedSize(800, 600)
        self.init_graph(200, 250)
        self.init_button()


    def init_graph(self, x_val, y_val):
        self.graph.move(x_val, y_val)
        self.graph.setVisible(False)


    def slider_value_changed(self, value):
        self.slider_update.emit(value)
        self.slider_label.setText("Value of a: " + str(value))
        self.slider_label.adjustSize()
        # self.reset_graph(False)
        # self.draw_graph()


    def init_button(self):
        self.graph_button.resize(100, 50)
        self.graph_button.move(600, 350)
        QToolTip.setFont(QFont('Times', 13))
        self.graph_button.setToolTip('Click to show/recreate graph!')
        self.graph_button.clicked.connect(lambda: self.redraw_graph())


    def redraw_graph(self):
        # self.graph.setVisible(False)
        # self.gather_data_and_create
        X, Y = self.construct_data()
        self.graph.set_x_data(X)
        self.graph.set_y_data(Y)

        self.graph.plot()
        # self.graph.setVisible(True)




    def construct_data(self):
        zero_data = (int(self.class_0_construction.samples_slider.text_field.text()),
                    int(self.class_0_construction.modes_slider.text_field.text()))
        one_data = (int(self.class_1_construction.samples_slider.text_field.text()),
                    int(self.class_1_construction.modes_slider.text_field.text()))


        number_samples_per_class = [zero_data[0] * zero_data[1], one_data[0] * one_data[1]]
        total_samples = number_samples_per_class[0] + number_samples_per_class[1]

        Y = np.zeros(shape=(total_samples,))
        X = np.zeros(shape=(total_samples, 2))

        X, Y = self.construct_arrays(0, zero_data, X, Y, 0)
        X, Y = self.construct_arrays(zero_data[0] * zero_data[1], one_data, X, Y, 1)

        return X, Y




    def construct_arrays(self, start_index, data, x, y, class_label):
        mu_range = 5
        for i in range(data[1]):
            mu = [random.uniform(-mu_range, mu_range), random.uniform(-mu_range, mu_range)]
            xi = np.random.randn(data[0], 2) + mu
            yi = np.ones(shape=(data[0], )) * class_label
            x[start_index: start_index + data[0], :] = xi
            y[start_index: start_index + data[0]] = yi
            start_index += data[0]

        return x, y
