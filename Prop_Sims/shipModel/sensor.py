from markovChain import markovChain
import numpy as np

class sensor:

    ''' a simple model of a sensor object 
    
        EXAMPLE:
        >>> sensor1 = sensor(0.98) 
        >>> sensor1.state
        'working'
        >>> sensor1.update_state(2)
        >>> sensor1.state
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
        self.markov_model = markovChain(num_states, transition_mat)
        self.state = self.markov_model.current_state        


# ---------------------------------------------------------------------
    def updateState(self, num_days)-> None:
        """
        Predicts the true state of self after a given number of days
        
        :param num_days: int number of days to predict ahead from current state
        """

        # update then update self attributes
        self.markov_model.updateState(num_days)
        self.state = self.markov_model.current_state
    
# ---------------------------------------------------------------------