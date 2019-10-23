from PyQt5.QtWidgets import (QSlider, QLabel, QToolTip, QLineEdit)
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtGui import (QFont, QIntValidator)



class MySlider(QSlider):

    slider_update = pyqtSignal(int)
    text_field_update = pyqtSignal(int)

    def __init__(self, parent=None, x_val=100, y_val=500, min_val=1, max_val=10, \
    label_message="Value of slider: "):

        super().__init__(Qt.Horizontal)
        self.label_message = label_message
        self.setParent(parent)
        self.move(x_val, y_val)
        self.resize(200, 20)
        self.setMinimum(min_val)
        self.setMaximum(max_val)
        self.setVisible(True)
        self.valueChanged.connect(self.slider_value_changed)
        self.label = QLabel(self.label_message + str(self.value()), parent)

        self.text_field = QLineEdit(parent)

        self.init_tool_tip()
        self.init_label()
        self.init_text_field()

    def init_label(self):
        self.label.move(self.x(), self.y() - 20)
        self.label.setFont(QFont('Times', 13))
        self.label.setVisible(True)


    def init_tool_tip(self):
        QToolTip.setFont(QFont('Times', 13))
        self.setToolTip('If the value are not big enought\ninput them into text field')
        self.label.setToolTip('If the value are not big enought\ninput them into text field')


    def slider_value_changed(self, value):
        self.slider_update.emit(value)
        self.label.setText(self.label_message + str(value))
        self.label.adjustSize()
        self.text_field.setText(str(value))
        # font_size = self.text_field.PointSize
        self.text_field.setFixedWidth(self.fm.boundingRect(self.text_field.text()).width() + self.font_size)



    def init_text_field(self, x_val=250, y_val=-10, font_size=13):
        self.font_size = font_size
        self.text_field.setValidator(QIntValidator(1, 99999, self.text_field))
        self.text_field.setFont(QFont('Times', font_size))
        self.text_field.move(self.x() + x_val, self.y() + y_val)
        self.text_field.setText(str(self.value()))
        self.fm = self.text_field.fontMetrics()
        self.text_field.setFixedWidth(self.fm.boundingRect(self.text_field.text()).width() + self.font_size)
        self.text_field.textEdited.connect(self.text_field_value_changed)

    def text_field_value_changed(self, value):
        if(value == ''):
            self.text_field.setText('1')
            value = '1'
        self.text_field_update.emit(value)
        self.text_field.setFixedWidth(self.fm.boundingRect(self.text_field.text()).width() + self.font_size)
        self.label.setText(self.label_message + str(value))
        self.label.adjustSize()
