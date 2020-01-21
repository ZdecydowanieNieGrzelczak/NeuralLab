


from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
import sklearn.utils
import matplotlib.pyplot as plt
import numpy as np
    
from NeuralNet import NeuralNet



class MyGraph(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=100, x_data=[], y_data=[]):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.x_data = []
        self.ax = self.figure.add_subplot(111)
        self.y_data = []
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.brain = NeuralNet()

    def plot(self, eval_value):
        # plt.hide()
        X, Y = sklearn.utils.shuffle(self.x_data, self.y_data, random_state=0)
        # print("eval in plot : ", eval_value)



        cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
        cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
        # cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA'])
        # cmap_bold = ListedColormap(['#FF0000', '#00FF00'])


        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

        h = 0.05
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))



        self.calculate_decision_boundry(X, Y, eval_value)


        Z = self.brain.evaluate(np.c_[xx.ravel(), yy.ravel()])
        # print(xx)
        # print(yy)

        # z = Z.reshape(xx.shape)


        # plt.figure()
        # plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
        #
        # plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=cmap_bold)
        # plt.xlim(xx.min(), xx.max())
        # plt.ylim(yy.min(), yy.max())



        plt.show()

    def set_x_data(self, values):
        self.x_data = values

    def set_y_data(self, values):
        self.y_data = values

    def calculate_decision_boundry(self, X, Y, eval_value):
        # self.neuron.set_y_data(Y)
        # self.neuron.set_x_data(X)
        # self.neuron.set_eval_function(eval_value)
        # self.neuron.create_weights_matrix()
        # self.neuron.train()

        for i in range(len(self.x_data)):
            self.brain.pass_value_to_input_layer(self.x_data[i])
            self.brain.forward_propagation()
            self.brain.backpropagate(self.x_data[i])
