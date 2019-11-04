import numpy as np
import random

class Neuron:

    def __init__(self, learning_step = 0, nr_of_iter = 0, X = [], Y = [], eval_fucn = 0):
        self.eval_function_matrix = [ self.Heavside, self.Sigmoid, self.ReLu, self.leaky_ReLu ]
        self.eval_function_der = [ self.Heavside_der, self.Sigmoid_der, self.ReLu_der, self.ReLu_der ]
        self.weights_matrix = []
        self.learning_step = learning_step
        self.number_of_iterations = nr_of_iter
        self.x_values = X
        self.y_values = Y
        self.weight = [0, 0, 0]
        self.eval_function = self.eval_function_matrix[eval_fucn]
        self.derivative_of_eval = self.eval_function_der[eval_fucn]


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
                weight_diff = self.learning_step * ((y - self.predict_single_label(np.dot(self.weight, x)) \
                    ) * self.derivative_of_eval(np.dot(self.weight, x)) * x)
                if i < 3 :
                    print(weight_diff)
                self.weight += weight_diff


    def predict_single_label(self, value):
        if self.eval_function(value) > 0:
            return 1
        else:
            return 0

    def evaluate(self, X):
        Y_predict = np.zeros(len(X))

        for x in range(len(X)):
            Y_predict[x] = self.Heavside(np.dot(self.weight, np.r_[-1, X[x]]))

        return Y_predict


    def Heavside(self, value):
        return value >= 0


    def Heavside_der(self, value):
        return 1



    def ReLu(self, value):
        if value <= 0:
            return 0
        else:
            return value


    def ReLu_der(self, value):
        return 1


    def leaky_ReLu(self, value):
        if value <= 0:
            return value * 0.01
        else:
            return value


    def Sigmoid(self, value):
        return (1.0 / (1.0 + np.exp(-value)))


    def Sigmoid_der(self, value):
        return (np.exp(-value) / ( (1.0 + np.exp(-value)) ** 2  ) )



    def set_eval_function(self, eval_value):
        self.eval_function = self.eval_function_matrix[eval_value]
        self.derivative_of_eval = self.eval_function_der[eval_value]
        print("Setting eval function to: ", eval_value)
