import numpy as np
import random

class Neuron:

    def __init__(self, learning_step = 0, nr_of_iter = 0, X = [], Y = []):
        self.weights_matrix = []
        self.learning_step = learning_step
        self.number_of_iterations = nr_of_iter
        self.x_values = X
        self.y_values = Y
        self.weight = [0, 0, 0]



    def set_x_data(self, x_data):
        self.x_values = x_data

    def set_y_data(self, y_data):
        self.y_values = y_data

    def create_weights_matrix(self):
        mu_range = 1
        nr_of_features = len(self.x_values)
        nr_of_dim = len(self.x_values[0])
        self.weights_matrix = np.ones(shape=(nr_of_features, nr_of_dim))
        for i in range (nr_of_features):
                self.weights_matrix = [random.uniform(-mu_range, mu_range), random.uniform(-mu_range, mu_range)]
        self.weight[0] = random.uniform(-mu_range, mu_range)
        self.weight[1] = np.average(self.weights_matrix[:][0])
        self.weight[2] = np.average(self.weights_matrix[:][1])


    def train(self):
        nr_of_features = len(self.x_values)
        nr_of_dim = len(self.x_values[0] + 1)
        weight_diff = np.zeros(shape=(nr_of_features, nr_of_dim))
        for i in range(self.number_of_iterations):
            for x, y in zip(self.x_values, self.y_values):
                x = np.r_[-1, x]
                weight_diff = self.learning_step * ((y - self.Heavside(np.dot(self.weight, x)) \
                    ) * x)
                self.weight += weight_diff


    def evaluate(self, X):
        Y_predict = np.zeros(len(X))

        for x in range(len(X)):
            Y_predict[x] = self.Heavside(np.dot(self.weight, np.r_[-1, X[x]]))

        return Y_predict


    def Heavside(self, value):
        if value >= 0:
            return 1
        else:
            return 0

    def Sigmoid(self, value):
        return (1.0 / (1.0 + np.exp(-value)))
