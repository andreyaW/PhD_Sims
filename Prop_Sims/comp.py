from markovChain import *

class comp:
    ''' a simple model of a component object '''

    def __init__(self):       
        '''
        --------------------------------------------------------------------------
        Parameters: 
            1. MTTF : float
                the mean time of failure of the component
            2. 
        --------------------------------------------------------------------------
        Returns:
        --------------------------------------------------------------------------
        ''' 

        number_of_states = 3
        transition_mat = np.array([[0.6, 0.3, 0.1],
                                    [0.0, 0.5, 0.5],
                                    [0.0, 0.2, 0.8]])
        self.markov_model = markovChain(number_of_states, transition_mat)
    
    def update_state(self, num_days):
        return self.markov_model.forecast(num_days)