from comp import comp
from sensor import sensor
from markovChain import markovChain

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
        Creates a new markov chain model for the sensedComp using the components 
        markov chain object. the state space for a sensed component is the same 
        state space as the components, plus an additional "undetected" state.

        """        
        # create a new state space and transition matrix for the sensed component
        self.createNewStates()
        self.createTransitionMatrix()

        # # use states and transition matrix to define the markov model
        # self.markov_model = markovChain(len(self.state_space), self.transition_matrix)
        # self.markov_model.state_space = self.state_space  

        # # determine the probability that majority of the sensors are working
        # sensor_state, sensor_state_prob = self.checkSensors()
        # comp_state, comp_state_prob = self.comp.state, self.comp.state_prob

    # ---------------------------------------------------------------------
    def createNewStates(self):
        """
        Creates a new state space for the sensed component by combining the component and sensor state spaces
        """

        # create new states as combinations of the component and sensor states
        state_space = {}
        comp_state_names = list(self.comp.markov_model.state_space.keys())
        sensor_state_names = list(self.sensors[0].markov_model.state_space.keys())
        

        for i in range(len(sensor_state_names)):
            for j in range(len(comp_state_names)):
                new_state_idx = (i, j)
                new_state_name = "comp " + str(comp_state_names[j]) + " sensors " + sensor_state_names[i]
                state_space.update({new_state_name: new_state_idx})
        self.state_space = state_space

    # ---------------------------------------------------------------------
    def createTransitionMatrix(self):
        
        # create new transition matrix
        self.transition_matrix = np.zeros((len(self.state_space), len(self.state_space)))

        # iterate over all possible cases of sensor and component states
        self.checkSensors() # function to aggregate sensor states

        # iterate over all possible cases of sensor and component states
        i,j = self.transition_matrix.shape
        for i in range(i):
            for j in range(j):
                self.transition_matrix[i,j] = 6


    # ---------------------------------------------------------------------
    def checkSensors(self)->None:
        """
        Checks the state of all sensors attached to the component
        """
        # start with equal probabilities of sensors working and failing
        prob_working = 1
        prob_failed = 1

        # iterate over all sensors and update probabilities
        sensor_states = [sensor.state for sensor in self.sensors]
        for i, state in enumerate(sensor_states):
            if state == 0:
                prob_working *= self.sensors[i].state_prob[state] 
            if state ==1: 
                prob_failed *= self.sensors[i].state_prob[state]
        
        # determine the state of the sensors based on the probabilities
        if prob_working > prob_failed:
            self.sensor_state = 0 # "working"
            self.sensor_state_prob = prob_working
        else:
            self.sensor_state = 1 # "failing"
            self.sensor_state_prob = prob_failed


    # ---------------------------------------------------------------------
    def setInitialState(self):
        pass
        # # choose initial state based on component
        # if sensor_state == 0:
        #     self.state = comp_state
        #     self.state_name = comp_state
        #     self.state_prob = comp_state_prob * sensor_state_prob
        # else:
        #     self.state = comp_state + 1
        #     self.state_name =  self.markov_model.stateIdx2Name(self.state)
        #     self.state_prob = comp_state_prob * sensor_state_prob

            
        
















    # # # ---------------------------------------------------------------------
    # def defineMarkovModel(self)->None:
    #     """
    #     Creates a model for self using a the components original markov chain object. the state space for a sensed component is the same state space as the component, plus an additional "undetected" state.
    #     """

    #     # add a state indicating only some sensors working
    #     self.markov_model = deepcopy(self.comp.markov_model)

    #     new_states = ["sensors failing" , "sensors_failed"]
    #     new_states_idx = [len(self.markov_model.state_space) , len(self.markov_model.state_space)+1]
        
    #     for i in range(len(new_states)):
    #         self.markov_model.state_space.update({new_states_idx[i]: new_states[i]})
    
    #     # choose initial state based on component
    #     self.state= self.comp.state
    #     self.state_num = self.comp.state_num
    #     self.state_space = self.markov_model.state_space

# ---------------------------------------------------------------------
    def updateState(self, num_days):
        """
        Predicts the true state of self after a given number of days
        
        :param num_days: int number of days to predict ahead from current state
        
        """
        # iterate over the desired number of days
        for j in range (num_days):
            
            # update states of all attached sensors and the component         
            num_sensors = len(self.sensors)
            for i in range(num_sensors):
                self.sensors[i].updateState(1)
            self.comp.updateState(1)

            self.checkSensors()
            sensors_state, sensors_prob = self.sensor_state, self.sensor_state_prob
            comp_state, comp_prob = self.comp.state, self.comp.state_prob

            print(comp_state, sensors_state)

# ---------------------------------------------------------------------
