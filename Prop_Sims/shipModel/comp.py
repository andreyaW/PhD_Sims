from markovChain import markovChain
import numpy as np


class comp:
    
    ''' a simple model of a component object 
        run with python -i comp.py    

    
        EXAMPLE: 
            >>> c1 = comp()
            >>> c1.state
            'working'
            >>> c1.updateState(2) 
            >>> c1.state
            'working'
            >>> c1.state_no
            0

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

        num_states = 3 # working, partially working, failed
        transition_mat = np.array([[0.98, 0.01, 0.01],
                                    [0.0, 0.98, 0.02],
                                    [0.0, 0.0,  1.0]])
        
        # save important attributes to self 
        mC = markovChain(num_states, transition_mat)
        self.markov_model = mC
        self.state = mC.current_state
        self.state_no = mC.stateName2Idx(self.state)        

# ---------------------------------------------------------------------
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