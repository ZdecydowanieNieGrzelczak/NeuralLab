from Neuron import Neuron
from Connection import Connection

import numpy as np
import random



class NeuralNet():
    def __init__(self, dimensions_of_hidden_layer=[4, 3]):
        self.input_layer = []
        self.hidden_layer = []
        self.output_layer = []
        self.dims_of_hidden_layer = dimensions_of_hidden_layer
        self.create_neural_net(2, dimensions_of_hidden_layer, 2)
        self.activation_func = None
        self.result = []
        self.predict_error = 0

    def create_neural_net(self, number_of_inputs=2, dims_of_hidden_layer=[4,3], number_of_outputs=2):
        temp_layer = []
        for i in range(number_of_inputs):
            self.input_layer.append(Neuron())

        for x in range(len(dims_of_hidden_layer)):
            for y in range(dims_of_hidden_layer[x]):
                temp_layer.append(Neuron())
            self.hidden_layer.append(temp_layer)
        
        for i in range(number_of_outputs):
            self.output_layer.append(Neuron())

        self.create_connections()


    def backpropagate(self, expected_values):
        # self.predict_error = self.calculate_guess_error(expected_values)
        

        # for neuron in self.output_layer:
            # neuron.calculate_error(self.predict_error)
        for i in range(len(self.output_layer)):
            self.output_layer[i].set_total_error( (self.result - expected_values)[i])

        nr_of_hidden_layers = np.shape(self.hidden_layer)[0]

        if nr_of_hidden_layers is 1:
            for neuron in self.hidden_layer:
                neuron.calculate_error()

        for i in range(nr_of_hidden_layers):
            layer = self.hidden_layer[nr_of_hidden_layers - i]
            for neuron in layer:
                neuron.calculate_error()
        

        for neuron in self.output_layer:
            neuron.calculate_error()
            

        


    def calculate_guess_error(self, expected_values):
        return 0.5 * (self.result - expected_values) ** 2


    def forward_propagation(self):
        self.result = []
        result_values_total = 0
        for input_neuron in self.input_layer:
            for conn in input_neuron.connections:
                conn.pass_value_further(input_neuron.value)
            # input_neuron.value = 0
        
        for layer in self.hidden_layer:
            for hidden_neuron in layer:
                hidden_neuron.calculate_activation_level()
                for conn in hidden_neuron.connections:
                    conn.pass_value_further(hidden_neuron.calculate_activation_level)
        
        for output_neuron in self.output_layer:
            result_values_total += output_neuron.value
        
        for output_neuron in self.output_layer:
            output_neuron.activation_level = output_neuron.value / result_values_total
            self.result.append(output_neuron.activation_level)
        
        # return result


    def pass_value_to_input_layer(self, values=[1, 1]):
        if(len(values) != len(self.input_layer)):
            raise ValueError('Missmatch in value dimentions')
        
        for i in range(len(values)):
            self.input_layer[i].value = values[i]


    def create_connections(self):
        for neuron_from in self.input_layer:
            for neuron_to in self.hidden_layer[0]:
                neuron_from.add_new_connection(Connection(neuron_from, neuron_to))
        
        for i in range(np.shape(self.hidden_layer)[0]) - 1):
            layer = self.hidden_layer[i]
            for neuron_from in layer:
                for neuron_to in self.hidden_layer[i + 1]:
                    neuron_from.add_new_connection(Connection(neuron_from, neuron_to))
        
        for neuron_from in self.hidden_layer[-1]:
            for neuron_to in self.output_layer:
                neuron_from.add_new_connection(Connection(neuron_from, neuron_to))
        
