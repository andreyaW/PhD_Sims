from comp import *
from sensor import * 
from copy import deepcopy


import numpy as np

class sensed_comp:
    ''' a simple model of a component and sensor pair '''

    def __init__(self, comp, num_sensors):

        # store the comp object and possible states to self
        self.comp = comp
        self.state_space = deepcopy(comp.markov_model.state_space)

        # add sensors to the sensed comp, and add failed sensor state to sensed comp
        self.num_sensors = num_sensors
        self.sensors = [sensor(0.98) for i in range(num_sensors)]
        # self.num_sensors = 1
        # self.sensors = [sensor(0.98)]
        
        val = "sensors failing" 
        key = len(self.state_space)
        self.state_space. update( {key: val})


    def forecast_state(self, num_days):
        '''determines the component health over instances in time'''

        # update component state
        self.comp.forecast_state(num_days)
        for i in range(self.num_sensors):
            self.sensors[i].forecast_state(num_days)
        
        comp = self.comp.markov_model
        num_sensors = self.num_sensors
        sensor = self.sensors[0].markov_model        

        sensed_comp_states = list(self.state_space.values()) # keys only
        for j in range (num_days):

            for i in range(num_sensors):            
                
                # check that the sensor is working
                if sensor.current_state == sensed_comp_states[0]:  
                    
                    # store the sensed components individual state
                    sensed_comp.current_state = comp.current_state       
                    sensed_comp.current_state_prob = comp.current_state_prob * sensor.current_state_prob # multiple conditonal probabilities
                    for key, val in comp.state_space.items(): 
                        if val == sensed_comp.current_state:
                            sensed_comp.current_state_num = key

                # give error if sensor is not working
                else:
                    sensed_comp.current_state = sensed_comp_states[-1]
                    sensed_comp.current_state_num = len(self.state_space)
                    sensed_comp.current_state_prob = sensor.current_state_prob                          # comp not seen on seeing sensor prob of failure
        
        return sensed_comp.current_state, sensed_comp.current_state_num, sensed_comp.current_state_prob










        # num_comp_states = comp.markov_model.num_states
        # num_sensor_states = sensor.markov_model.num_states
        # conditional_lookup = np.zeros((num_sensor_states, num_comp_states)) 
        # remaining_prob = 1-sensor.accuracy
        # state_prob = remaining_prob / (num_comp_states-1)
        
        # conditional_lookup[0][0] = sensor.accuracy      # sensor working state equal to sensor accuracy
        # conditional_lookup[0][1:] = state_prob          # equal prob of other sensor states 
        # # conditional_lookup[-1][-1]= 