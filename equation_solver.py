

import sys, math
from PyQt5.QtWidgets import (QPushButton, QWidget, QLineEdit, QApplication, QSlider, QLabel, QToolTip, QSizePolicy,\
                             QRadioButton, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import (QFont)
from PyQt5.QtCore import (Qt, pyqtSignal)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

e = math.exp(1)
PI = math.pi


class MainWindow(QWidget):

    slider_update = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.x_values = [-10, 10, 100]
        self.layout = QVBoxLayout()
        self.graph = FunctionFigure(self)
        self.default_radio_button = QRadioButton('Default', self)
        self.custom_radio_button = QRadioButton('Custom', self)
        self.current_equation = ''
        self.previous_equations = []
        self.edit_line = QLineEdit(self)
        self.equation_label = QLabel('Current equation is:' + self.current_equation, self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider_label = QLabel('Value of a: ' + str(self.slider.value()), self)
        self.start_value = QLineEdit(self)
        self.end_value = QLineEdit(self)
        self.number_of_digits = QLineEdit(self)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.reset_previous_equations_button = QPushButton('?', self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GUI")
        self.setFixedSize(800, 600)
        self.init_quit_button()
        self.init_edit_line()
        self.init_edit_button('e^x', 6, 0)
        self.init_edit_button('sqrt', 4, 0)
        self.init_edit_button('x', 1, 0)
        self.init_edit_button('a', 2, 0)
        self.init_edit_button('π', 5, 0)
        self.init_edit_button('^', 3, 0)
        self.init_edit_button('sin', 2, 1)
        self.init_edit_button('cos', 3, 1)
        self.init_edit_button('tan', 4, 1)
        self.init_edit_button('ctg', 5, 1)
        self.init_submit_button()
        self.init_reset_button()
        self.init_reset_previous_equations_button()
        self.init_equation_message()
        self.init_slider()
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.init_radio_buttons()
        self.init_graph()
        self.init_input_fields()

    def init_quit_button(self):
        quit_button = QPushButton("Quit", self)
        quit_button.resize(100, 40)
        quit_button.move(690, 20)
        quit_button.clicked.connect(QApplication.instance().quit)

    def init_edit_line(self):
        self.edit_line.resize(400, 30)
        self.edit_line.move(50, 100)
        self.edit_line.setFont(QFont("Times", 15))
        self.edit_line.setPlaceholderText("Please enter equation here")

    def add_to_edit_line(self, button_name):
        keys = {'e^x': 'e**()', 'sqrt': '**(1/2)', 'x': 'x', 'a': 'a', 'π': 'PI', '^': '**',
                'sin': 'np.sin(x)', 'cos': 'np.cos(x)', 'tan': 'np.tan(x)', 'ctg': 'np.tan(x)**(-1)'}
        self.edit_line.insert(keys[button_name])

    def init_edit_button(self, name, x_position, y_position):
        euler_button = QPushButton(name, self)
        euler_button.resize(35, 25)
        euler_button.move(20 + x_position * 40, 140 + y_position * 30)
        euler_button.clicked.connect(lambda: self.add_to_edit_line(name))

    def init_submit_button(self):
        submit_button = QPushButton("Submit!", self)
        submit_button.resize(100, 50)
        submit_button.move(350, 150)
        QToolTip.setFont(QFont('Times', 13))
        submit_button.setToolTip('Please make sure that \n equation is correct!')
        submit_button.clicked.connect(lambda: self.try_to_crack_math())

    def init_reset_button(self):
        reset_button = QPushButton("Reset graph!", self)
        reset_button.resize(100, 50)
        reset_button.move(500, 470)
        QToolTip.setFont(QFont('Times', 13))
        reset_button.setToolTip('Click to clear the graph area!')
        reset_button.clicked.connect(lambda: self.reset_graph(True))

    def init_reset_previous_equations_button(self):
        self.reset_previous_equations_button.setVisible(False)
        self.reset_previous_equations_button.resize(50, 50)
        self.reset_previous_equations_button.move(500, 400)
        self.reset_previous_equations_button.clicked.connect(lambda: self.clear_previous_equations())

    def set_previous_equations(self):
        self.previous_equations.append(self.current_equation)
        self.reset_previous_equations_button.setVisible(True)
        QToolTip.setFont(QFont('Times', 13))
        text_message = "Previous equations are:\n"
        for iterator in range(len(self.previous_equations)):
            text_message += self.previous_equations[iterator] + '\n'
        text_message += 'Click this button to clear them'
        self.reset_previous_equations_button.setToolTip(text_message)

    def clear_previous_equations(self):
        self.previous_equations = []
        self.reset_graph(False)
        self.draw_graph()
        self.reset_previous_equations_button.setVisible(False)

    def get_values_of_x(self):
        try:
            self.x_values[0] = eval(self.start_value.text())
            self.x_values[1] = eval(self.end_value.text())
            self.x_values[2] = eval(self.number_of_digits.text())
        except (SyntaxError, NameError):
            QMessageBox.question(self, 'Message', "All values must be integers!", QMessageBox.Ok)
            return False
        if self.x_values[0] > self.x_values[1]:
            QMessageBox.question(self, 'Message', "Start value cannot be smaller that end value!", QMessageBox.Ok)
            return False
        elif self.x_values[0] == self.x_values[1]:
            QMessageBox.question(self, 'Message', "Start and end values cannot be equal!", QMessageBox.Ok)
            return False
        elif self.x_values[2] < 0:
            QMessageBox.question(self, 'Message', "The number of calculations cannot be negative!", QMessageBox.Ok)
            return False
        elif self.x_values[2] < 2:
            QMessageBox.question(self, 'Message', "Need at least 2 numbers to compute", QMessageBox.Ok)
            return False
        return True

    def init_equation_message(self):
        self.equation_label.setFont(QFont('Times', 15))
        self.equation_label.setHidden(True)
        self.equation_label.move(50, 50)

    def init_slider(self):
        self.slider.move(500, 100)
        self.slider.resize(150, 20)
        self.slider.setMinimum(-10)
        self.slider.setMaximum(10)

        self.slider_label.move(self.slider.x(), self.slider.y() - 20)
        self.slider_label.setFont(QFont('Times', 15))
        self.slider_label.setVisible(True)

    def init_radio_buttons(self):
        radio_button_label = QLabel('X values settings:', self)
        radio_button_label.setFont(QFont('Times', 15))
        radio_button_label.move(500, 180)
        self.default_radio_button.move(500, 200)
        QToolTip.setFont(QFont('Times', 13))
        self.default_radio_button.setToolTip('From -10 to 10, with 100 digits')
        self.default_radio_button.clicked.connect(lambda: self.hide_options())
        self.default_radio_button.setChecked(True)
        self.custom_radio_button.move(500, 220)
        self.custom_radio_button.setToolTip('Set your own x data\ndata must be integer values!')
        self.custom_radio_button.clicked.connect(lambda: self.show_options())

    def init_input_fields(self):
        self.start_value.move(500, 250)
        self.end_value.move(500, 280)
        self.number_of_digits.move(500, 310)
        self.start_value.resize(100, 30)
        self.end_value.resize(100, 30)
        self.number_of_digits.resize(100, 30)
        self.start_value.setVisible(False)
        self.end_value.setVisible(False)
        self.number_of_digits.setVisible(False)
        self.start_value.setPlaceholderText('first x value')
        self.end_value.setPlaceholderText('last x value')
        self.number_of_digits.setPlaceholderText('# of calculations')

    def hide_options(self):
        self.x_values = [-10, 10, 100]
        self.start_value.setVisible(False)
        self.end_value.setVisible(False)
        self.number_of_digits.setVisible(False)
        self.start_value.clear()
        self.end_value.clear()
        self.number_of_digits.clear()

    def show_options(self):
        self.start_value.setVisible(True)
        self.end_value.setVisible(True)
        self.number_of_digits.setVisible(True)

    def slider_value_changed(self, value):
        if self.current_equation:
            self.slider_update.emit(value)
            self.slider_label.setText("Value of a: " + str(value))
            self.slider_label.adjustSize()
            self.reset_graph(False)
            self.draw_graph()

    def get_function(self):
        return self.current_equation

    def init_graph(self):
        self.graph.setVisible(False)
        self.graph.move(50, 230)

    def draw_graph(self):
        self.graph.set_x_data(self.x_values)

        self.graph.set_y_data(self.get_function(), self.slider.value())
        self.graph.plot()
        for iterator in range (len(self.previous_equations)):
            self.graph.set_y_data((self.previous_equations[iterator]), self.slider.value())
            self.graph.plot()

    def reset_graph(self, reset_equations):
        if reset_equations:
            self.previous_equations = []
            self.current_equation = None
            self.reset_previous_equations_button.setVisible(False)
        self.graph.setVisible(False)
        del self.graph
        self.graph = FunctionFigure(self)
        self.graph.move(50, 230)
        if self.current_equation:
            self.graph.setVisible(True)

    def try_to_crack_math(self):
        if self.custom_radio_button.isChecked():
            if not self.get_values_of_x():
                return
        text = self.edit_line.text()
        x = 0
        a = 0
        try:
            eval(text)
        except (SyntaxError, NameError) as e:
            # print('Raised error! ->', e)
            if text:
                QMessageBox.question(self, 'Message', "Cannot solve provided equation!", QMessageBox.Ok)

            else:
                 QMessageBox.question(self, 'Message', "Input field is empty!", QMessageBox.Ok)
        else:
            self.equation_label.setVisible(False)
            if self.current_equation:
                self.set_previous_equations()
            self.current_equation = text
            self.equation_label.setText("Current equation is: " + self.current_equation)
            self.equation_label.setVisible(True)
            self.draw_graph()
            self.graph.setVisible(True)


class FunctionFigure(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.x_data = None
        self.iterations = 0
        self.ax = self.figure.add_subplot(111)
        self.y_data = []
        self.x = 0
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self):
        self.ax.plot(self.x_data, self.y_data)
        self.draw()

    def set_x_data(self, values):
        starting_value, end_value, number_of_values = values

        self.x_data = np.linspace(starting_value, end_value, number_of_values)
        self.iterations = number_of_values

    def set_y_data(self, function, a):
        self.y_data = []

        for iterator in range(self.iterations):
            x = self.x_data[iterator]
            self.y_data.append(eval(function))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
