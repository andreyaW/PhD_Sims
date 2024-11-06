from comp import comp
from sensor import sensor
from copy import deepcopy

import numpy as np

class sensed_comp:
    ''' a simple model of sensors connected to a component 
        
        EXAMPLE:
        >>> comp1= comp()             
        >>> sensors = [sensor(0.98) for i in range(3)]
        >>> sensed_comp1 = sensed_comp(comp1, sensors)
        >>> sensed_comp1.state
        'working'
    
    '''

    def __init__(self, comp, sensors_list =  [sensor(0.98) for i in range(2)])->None:
        """
        Initialize a sensed component consisting of a component object and a list of attached sensor objects.

        :param comp: comp the component object being sensed
        :param sensors: list sensor a list of all sensors associated with the component
        """

        # store the comp and sensor objects to self
        self.comp = comp
        self.sensors = sensors_list     # default is two "good" sensors
        self.defineMarkovModel()

        
    def defineMarkovModel(self)->None:
        """
        Creates a model for self using a markov chain object
            the state space for a sensed component is the same state space as the component, plus an additional "undetected" state.
        """

        # save state space
        self.state_space = deepcopy(self.comp.markov_model.state_space)
        val = "sensors failing" 
        key = len(self.state_space)
        self.state_space.update( {key: val})

        # choose initial state
        self.state= self.comp.state

# ---------------------------------------------------------------------
    def update_state(self, num_days):
        """
        Predicts the true state of self after a given number of days
        
        :param num_days: int number of days to predict ahead from current state
        """

        sensed_states_over_time = []
        possible_states = list(self.state_space.values())    # state numbers (keys) only

        for j in range (num_days):

            # update states of all attached sensors and the component         
            num_sensors = len(self.sensors)
            for i in range(num_sensors):
                self.sensors[i].update_state(1)
            self.comp.update_state(1)

            # grab the Markov Models for computation of state transition probability
            comp = self.comp.markov_model
            sensors = [self.sensors[i].markov_model  for i in range(num_sensors)]      
            
            # determine how many sensors are working and what state they sense
            count_sensors_working = np.array([sensors[i].current_state == "working" for i in range(num_sensors)])
            detected_states = np.array([comp.current_state for i in range(num_sensors)])
            detected_states = detected_states[count_sensors_working]


            if sum(count_sensors_working) > num_sensors/2: 
                majority_detected = 
                self.state = majority_detected
            else:
                self.state = self.state_space[-1]



            
            # detected_states = []
            # for i in range(num_sensors):            

            #     # check that the sensor is working
            #     if sensors[i].current_state == "working":  
            #         detected_states.append(comp.current_state)


            #         # store the sensed components individual state
            #         sensed_comp.current_state = comp.current_state       

            #     # give error if sensor is not working
            #     else:






                    # sensed_comp.current_state_prob = comp.current_state_prob * sensor.current_state_prob # multiply conditonal probabilities
                    # for key, val in comp.state_space.items(): 
                    #     if val == sensed_comp.current_state:
                    #         sensed_comp.current_state_num = key
# ---------------------------------------------------------------------


        # num_comp_states = comp.markov_model.num_states
        # num_sensor_states = sensor.markov_model.num_states
        # conditional_lookup = np.zeros((num_sensor_states, num_comp_states)) 
        # remaining_prob = 1-sensor.accuracy
        # state_prob = remaining_prob / (num_comp_states-1)
        
        # conditional_lookup[0][0] = sensor.accuracy      # sensor working state equal to sensor accuracy
        # conditional_lookup[0][1:] = state_prob          # equal prob of other sensor states 
        # # conditional_lookup[-1][-1]= 