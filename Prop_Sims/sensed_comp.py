from comp import *
from sensor import * 

import numpy as np

class sensed_comp:
    ''' a simple model of a component and sensor pair '''

    def __init__(self, comp, num_sensors):

        # store the sensor and comp objects to self
        self.comp = comp
        self.sensors = [sensor(0.98) for i in range(num_sensors)]
        

    def forecast_state(self, num_days):

        '''determines the component health over instances in time'''

        comp = self.comp
        sensor = self.sensors[0]        
        
        # update component state
        comp.forecast_state(num_days)
        sensor.forecast_state(num_days)
        
        # multiply conditional probabilities 
        if sensor.markov_model.current_state == "working":  
            sensed_comp.current_state = comp.markov_model.current_state       
            sensed_comp.current_state_prob = comp.markov_model.current_state_prob * sensor.markov_model.current_state_prob
        else:
            sensed_comp.current_state = "NOT DETECTED"
            sensed_comp.current_state_prob = sensor.markov_model.current_state_prob
        return f"The sensed component is in state {sensed_comp.current_state} , with probability {sensed_comp.current_state_prob}"










        # num_comp_states = comp.markov_model.num_states
        # num_sensor_states = sensor.markov_model.num_states
        # conditional_lookup = np.zeros((num_sensor_states, num_comp_states)) 
        # remaining_prob = 1-sensor.accuracy
        # state_prob = remaining_prob / (num_comp_states-1)
        
        # conditional_lookup[0][0] = sensor.accuracy      # sensor working state equal to sensor accuracy
        # conditional_lookup[0][1:] = state_prob          # equal prob of other sensor states 
        # # conditional_lookup[-1][-1]= 