from markovChain import *

class sensor:

    ''' a simple model of a sensor object '''

    def __init__(self, accuracy):
        '''
        --------------------------------------------------------------------------
        Parameters: 
            1. accuracy : float
                the precision of the sensor in its working state
        --------------------------------------------------------------------------
        Returns:
        --------------------------------------------------------------------------
        '''

        self.accuracy = accuracy

        # assuming a 2 state markov sensor model
        number_of_states= 2
        transition_mat =np.array([[0.5, 0.5],
                                  [0.0, 1.0]])
        self.markov_model = markovChain(number_of_states,transition_mat)
        

        def update_state(self, num_days):
            return self.markov_model.forecast(num_days)
        
