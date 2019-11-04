
from PyQt5.QtWidgets import QRadioButton

class CustomButton(QRadioButton):



    def __init__(self, parent= None, message = "", value = 0):
        super().__init__(message)
        self.setParent(parent)
        self.move(180, 450 - value * 40)
        self.act_func_index = value
