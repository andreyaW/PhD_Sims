from markovChain import markovChain
import numpy as np


class comp:
    
    ''' a simple model of a component object 
    
        EXAMPLE: 
            >>> comp1 = comp()
            >>> comp1.state
            'working'
            >>> comp1.forecast_state(2) 
            >>> comp1.state
            'working'

    '''


    def __init__(self)->None:
        """
        Initialize the component, (assuming Markov Chain Model for now)
        
        :param MTTF: float the mean time til failure of the component 
        """

        self.defineMarkovModel()



# ---------------------------------------------------------------------        
    def defineMarkovModel(self) ->None:
        """
        Creates a model for self using a markov chain object
        """

        number_of_states = 3 # working, partially working, failed
        transition_mat = np.array([[0.98, 0.01, 0.01],
                                    [0.0, 0.98, 0.02],
                                    [0.0, 0.0,  1.0]])
        
        # save important attributes to self 
        self.markov_model = markovChain(number_of_states, transition_mat)
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
