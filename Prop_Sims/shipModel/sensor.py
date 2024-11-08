from markovChain import markovChain
import numpy as np

class sensor:

    ''' a simple model of a sensor object 
        run with python -i sensor.py    

    
        EXAMPLE:
        >>> s1 = sensor(0.98) 
        >>> s1.state
        'working'
        >>> s1.update_state(2)
        >>> s1.state
        'failed'

    '''

    def __init__(self, accuracy=0.98):
        """
        Initialize a sensor object represented as a Markov Chain

        :params accuracy: float the probability of the sensor detecting state correctly
                                the default is a good sensor (high accuracy)
        """
        self.accuracy = accuracy   
        self.defineMarkovModel()
        

    def defineMarkovModel(self)-> None:
        """
        Creates a model for self using a markov chain object
        """
        
        # assuming a 2 state markov sensor model
        num_states= 2
        transition_mat = np.array([[self.accuracy, 1.0 -self.accuracy],
                                   [0.0  ,    1.0]])        # failed is absorbing state
        
        mC = markovChain(num_states, transition_mat)
        self.markov_model = mC
        self.state = mC.current_state
        self.state_no = mC.stateName2Idx(self.state)        

# ---------------------------------------------------------------------
    def updateState(self, num_days)-> None:
    def updateState(self, num_days)-> None:
        """
        Predicts the true state of self after a given number of days
        
        :param num_days: int number of days to predict ahead from current state
        """

        # update then update self attributes
        mC = self.markov_model
        mC.update_state(num_days)
        self.state = mC.current_state
        self.state_no = mC.stateName2Idx(mC.current_state)

# ---------------------------------------------------------------------