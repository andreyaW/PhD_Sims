from comp import comp
from sensor import sensor
from copy import deepcopy

import numpy as np

class sensedComp:
    ''' a simple model of sensors connected to a component 
        To run this file enter in terminal: python -i sensedComp.py    
    
        EXAMPLE: 
        >>> c1= sensed_comp()             
        >>> c1.state           
        'working'
        >>> c1.updateState(10)
        >>> c1.state 
        'sensors failing'
        >>> c1.updateState(10)
        >>> c1.state
        'sensors failing'
        >>> c1.updateState(10)
        >>> c1.state
        'all sensors failed'
    
    '''

    def __init__(self, comp = comp(), sensors_list =  [sensor(0.98) for i in range(3)])->None:
        """
        Initialize a sensed component consisting of a component object and a list of attached sensor objects.

        :param comp: comp the component object being sensed
        :param sensors: list sensor a list of all sensors associated with the component
        """

        # store the comp and sensor objects to self
        self.comp = comp
        self.sensors = sensors_list     # default is two "good" sensors
        self.defineMarkovModel()

    # ---------------------------------------------------------------------
    def defineMarkovModel(self)->None:
        """
        Creates a model for self using a the components original markov chain object. the state space for a sensed component is the same state space as the component, plus an additional "undetected" state.
        """

        # add a state indicating only some sensors working
        self.markov_model = deepcopy(self.comp.markov_model)

        new_states = ["sensors failing" , "sensors_failed"]
        new_states_idx = [len(self.markov_model.state_space) , len(self.markov_model.state_space)+1]
        
        for i in range(len(new_states)):
            self.markov_model.state_space.update({new_states_idx[i]: new_states[i]})
    
        # choose initial state based on component
        self.state= self.comp.state
        self.state_num = self.comp.state_num
        self.state_space = self.markov_model.state_space

# ---------------------------------------------------------------------
    def updateState(self, num_days):
        """
        Predicts the true state of self after a given number of days
        
        :param num_days: int number of days to predict ahead from current state
        
        """
        comp = self.comp
        sensors = self.sensors
        possible_states = list(self.state_space.values())

        # iterate over the desired number of days
        for j in range (num_days):
            
            # update states of all attached sensors and the component         
            num_sensors = len(sensors)
            for i in range(num_sensors):
                sensors[i].updateState(1)
            comp.updateState(1)
            
            # determine how many sensors are working and what state they sense
            sensors_working = np.array([sensors[i].state == "working" for i in range(num_sensors)])
            num_sensors_working = sum(sensors_working)
            detected_states = np.array([comp.state_no for i in range(num_sensors)])
            detected_states = detected_states[sensors_working]
            
            # if the majority of sensors are working the component state can be sensed
            if num_sensors_working > num_sensors/2: 
                majority_detected = max(set(detected_states), key=detected_states.tolist().count)
                self.state_no = majority_detected
                self.state = possible_states[majority_detected]

            # else component state is not detectable            
            elif num_sensors_working == 0 :
                self.state = possible_states[-1]
                self.state_no = len(self.state_space)

            else:
                self.state = possible_states[-2]
                self.state_no = len(self.state_space)-1

# ---------------------------------------------------------------------
