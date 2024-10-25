from comp import *
from sensor import * 

import numpy as np

class sensed_comp:
    def __init__(self, comp, sensor):

        # store the sensor and comp objects to self
        self.comp = comp
        self.sensor = sensor

        


    def check_state(self):

        # determines the component health for an instance in time
    
        comp = self.comp
        sensor = self.sensor

        # update component state
        comp.update_state(1)
        sensor.update_state(1)

        # fill in the table
        num_comp_states = comp.markov_model.num_states
        num_sensor_states = sensor.markov_model.num_states
        conditional_lookup = np.zeros((num_sensor_states, num_comp_states)) 
        
        remaining_prob = 1-sensor.accuracy
        state_prob = remaining_prob / (num_sensor_states-1)
        
        conditional_lookup[0][0] = sensor.accuracy
        conditional_lookup[0][1:] = state_prob

        print(conditional_lookup)


# sensor = markovChain(3, transition_matrix)
# sensor.forecast(5)
# days= 5
# test_comp = comp()
# test_comp.generate_states(days)