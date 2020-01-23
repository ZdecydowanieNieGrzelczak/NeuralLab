import numpy as np
import random


class Connection():
    def __init__(self, neuron_from=None, neuron_to=None, weight_range=4):
        self.weight = random.uniform(-weight_range, weight_range)
        self.destination_neuron = neuron_to
        self.source_neuron = neuron_from

    def pass_value_further(self, value):
        self.destination_neuron.gather_input(value * self.weight)


    def adjust_weight(self, value):
        self.weight += value