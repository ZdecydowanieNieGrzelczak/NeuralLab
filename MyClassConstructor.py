from PyQt5.QtGui import (QFont, QIntValidator)
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QPushButton, QWidget, QLineEdit, QApplication, QSlider, QLabel, QToolTip, QSizePolicy)



from MySlider import MySlider



class MyClassConstructor(QWidget):

    def __init__(self, parent=None, x_val=500, y_val=100, color='color: black', class_no=0):

        super().__init__()
        self.setParent(parent)
        self.samples_slider = MySlider(self, x_val, y_val, 1, 100, 'Number of samples per mode: ')
        self.modes_slider = MySlider(self, x_val + 400, y_val, 1, 10, 'Number of modes: ')
        self.init_slider(self.samples_slider, 10, 50)
        self.init_slider(self.modes_slider, 1, 1)
        self.class_no = class_no
        self.class_label = QLabel('Class ' + str(self.class_no), parent)
        self.x_val = x_val
        self.y_val = y_val
        self.color = color
        self.init_class_label(color)

    def init_slider(self, slider, step_value, start_value):
        slider.setSingleStep(step_value)
        slider.setValue(start_value)


    def init_class_label(self, color):
        self.class_label.setFont(QFont('Times', 20))
        self.class_label.move(self.x_val + 290, self.y_val - 50)
        self.class_label.setStyleSheet(color)
