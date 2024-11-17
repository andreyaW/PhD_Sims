import numpy as np
from artistFunctions import drawGraphs as artist

class markovChain:
    ''' 
        a simple model for a markovChain
        run with python -i markovChain()    


        EXAMPLE: 
            >>> mc_model = markovChain()
            >>> mc_model.current_state
            'working'
            >>> mc_model.update_state(1)
            >>> mc_model.current_state
            'failed'

    '''

    def __init__(self, 
                 num_states : int = 2, 
                 transition_prob = np.array(([0.5, 0.5],[0.5, 0.5]))
                )-> None:
        
        """
        Initialize a markov chain model. Number of states and transition probabilities can be specified.

        :param num_states: int number of states in the Markov chain
        :param transition_prob: ndarray matrix of transition probabilities between states

        """
        # self.num_states = num_states
        self.verifyTransitionMatrix(transition_prob) 
        self.defineStateSpace(num_states)
        
# ------------------------------------------------------------------------------------

    def verifyTransitionMatrix(self, transition_matrix) -> None:
        """ 
        Check for a properly defined transition matrix i.e: 
            - the sum across each row should be 1
            - matrix must be NxN, where N is the number of states in the chain

        :param transition_matrix: ndarray matrix of transition probabilities between states
        
        """
        # CHECK0: matrix must be square
        if transition_matrix.shape[0] != transition_matrix.shape[1]:
            raise ValueError("The transition matrix must be square.")
        
        # CHECK1: the sum of each row should be 1
        if not np.allclose(transition_matrix.sum(axis=1), 1):
            raise ValueError("The sum of each row should be 1.")

        # CHECK2: all values should be between 0 and 1
        if not np.all((transition_matrix >= 0) & (transition_matrix <= 1)):
            raise ValueError("All values in the transition matrix should be between 0 and 1.")
        
        self.transition_matrix = transition_matrix

    # ------------------------------------------------------------------------------------

    def defineStateSpace(self, N, initial_state_idx: int = 0) -> None:
        """
        Initialize the state space as a dictionary and pick a random initial state
        
        :param N: int number of states in the state space
        :param initial_state_idx: the number of the intial state as defined in the state space dictionary 
                                (defualt is comps current state) 
        """

        # default two states (0: working, 1: failed)
        state_name = ["working", "failed"]

        # for Markov Chain with more than 2 states, give intermediate states a default name
        if N> 2: 
            for i in range(N-2):
                state_name.insert(-1,"partially working (" + str(i+1) + ")")

        # zip state names and numbers to define state space as dictionary
        state_num = [i for i in range(N)]
        state_space = dict(zip(state_name, state_num))          # keys, values
        self.state_space = state_space

        # the initial state is working (unless specified otherwise)   
        initial_state_name = self.stateIdx2Name(initial_state_idx)
        self.state = initial_state_name
        self.state_prob = 1                 # 100% chance of starting at designated inital state


# ------------------------------------------------------------------------------------  
    
    def updateState(self, num_steps) -> None:
        """
        Forecasts the future state of the Markov Model
        
        :param num_days: int number of steps to update the state over
        
        """
        current_state = self.state        
        state_space = self.state_space
        states_list = [current_state]
        
        # iterate over the desired number of days 
        probs = [self.current_state_prob , 0, 0]
        i = 0
        while i != num_steps:

            for key, value in state_space.items(): # keys is state label #, values is state name
                
                # determine the current state and the next state 
                if current_state == value:
                    transition_probs = self.transition_matrix[key]
                    possible_states = list(state_space.keys())                    
                    next_state_idx = np.random.choice(possible_states, replace= True, p=transition_probs)
                    probs *= transition_probs                               # n step update (assumes no change in transition probabilities over time)
                    current_state_prob = max(probs) * probs[next_state_idx] # probability of the ground truth sequence of states
            
                    print(probs)
                    print(current_state_prob)
            
                # update the state to reflect the transition
                current_state = state_space[next_state_idx]
                states_list.append(current_state)              
                i +=1 

        # save important attributes to self
        self.state = current_state
        self.state_prob = max(probs) # probability of the ground truth sequence of states
        self.all_state_probs = probs      # probability of being in any state at any time
        
        # print("Possible states: " + str(states_list))
        # print("End state after " + str(num_steps) + " days: " + str(current_state))
        # print("Probability of the possible sequence of states: " + str(prob))

# ---------------------------------------------------------------------

    def stateIdx2Name(self, idx):
        """
            Allows a users to quickly go between the state number and state name (for plotting mostly)

            :param idx: int the number of the state in the state space

            EX:
                >>> mc.stateIdx2Name(0)
                working
        
        """
        state_space = self.state_space
        name = state_space.get(idx, "STATE WITH THAT IDX NOT FOUND.")
        return name

# ---------------------------------------------------------------------
        
    def stateName2Idx(self, name):    
        """
            Allows a users to quickly go between the state number and state name (for plotting mostly)

            :param name: str the name of the state in the state space

            EX:
            >>> mc.stateIdx2Name('failed')
            3
        
        """
        for key, value in self.state_space.items():
            if value == name:
                idx = key
                return idx
        return "STATE WITH THAT NAME NOT FOUND"  # Return error if the name is not found

# ---------------------------------------------------------------------
    def draw(self):
        """
        Draws the Markov Chain Model

        EX: 
        >>> mc.draw()
        """
        
        artist.drawMarkovChain(self)