from shipModel.markovChain import markovChain
import numpy as np


class comp:
    
    ''' a simple model of a component object 
        To run this file enter in terminal: python -i comp.py    

    
        EXAMPLE: 
            >>> c1 = comp()
            >>> c1.state
            'working'
            >>> c1.updateState(2) 
            >>> c1.state
            'working'
            >>> c1.state_num
            0

    '''


    def __init__(self)->None:
        """
        Initialize the component, (assuming Markov Chain Model for now)
        
        :param MTTF: float the mean time til failure of the component 
        """
        self.name="component"
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
        
        # update the name of the markov model to sensor
        mC.name = self.name                     

        # store necessary parameters of the markov model to self
        self.markov_model = mC
        self.state = mC.state
        self.state_prob = mC.state_prob
        self.state_name = mC.stateIdx2Name(mC.state)   
        
# ---------------------------------------------------------------------
    def updateState(self, num_days)-> None:
        """
        Predicts the true state of self after a given number of days
        
        :param num_days: int number of days to predict ahead from current state
        """

        # update the markov model
        mC = self.markov_model
        mC.updateState(num_days)

        # update the parameters of self to match the markov model
        self.state = mC.state
        self.state_prob = mC.state_prob
        self.state_name = mC.stateIdx2Name(mC.state)

# ---------------------------------------------------------------------

    def reset(self)->None:
        '''reset the component to its initial state'''
        self.markov_model.reset()


# ---------------------------------------------------------------------
def main():

    # Create an instance of the component
    c1 = comp()
    
    # Print initial state
    print(f"Initial state: {c1.state_name}")
    
    # Update state after 2 days
    c1.updateState(2)
    
    # Print updated state
    print(f"State after 2 days: {c1.state_name}")

if __name__ == "__main__":
    main()