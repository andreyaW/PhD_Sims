import numpy as np

class markovChain:

    ''' a simple model for a markovChain
        
    
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
        self.state_space, self.state = self.defineStateSpace(num_states)

# ------------------------------------------------------------------------------------

    def verifyTransitionMatrix(self, transition_matrix) -> None:
        """ 
        Check for a properly defined transition matrix i.e: 
            - the sum across each row should be 1
            - matrix must be NxN, where N is the number of states in the chain

        :param transition_matrix: ndarray matrix of transition probabilities between states
        
        """
        # check that the matrix is square
        if transition_matrix.shape[0] != transition_matrix.shape[1]:
            raise(ValueError("The transition matrix should be square."))

        # check that each row sums to 1
        for i in range(transition_matrix.shape[1]):
            row = transition_matrix[i, :]
            if np.sum(row) != 1.0:
                raise (ValueError("The transition matrix must sum to 1 across each row."))

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

        # the initial state is working (unless specified otherwise)   
        initial_state_name = self.idxToName(initial_state_idx)
    

        return initial_state_name

        # save important attributes to self       
        self.state_space = state_space
        self.current_state = state_space[initial_state_name]   
        self.current_state_prob = 1     # 100% chance of starting at designated inital state
        
        
    
    # ------------------------------------------------------------------------------------
    # def idxToName(self, idx):
    #     """
    #         Allows a users to quickly go between the state number and state name (for plotting mostly)

    #         :param idx: int the number of the state in the state space (ex: 0 = working)
    #     """
    #     # grab name using idx 
    #     state_space_names = list(self.state_space.keys)       
    #     initial_state_name = state_space_names[idx]
    
    
    def updateState(self, num_steps) -> None:
        """
        Forecasts the future state of the Markov Model
        
        :param num_days: int number of steps to update the state over
        
        """

        current_state = self.current_state        
        state_space = self.state_space
        
        states_list = [current_state]
        # print("Start state: " + str(current_state))

        prob = self.current_state_prob
        i = 0
        while i != num_steps:

            for key, value in state_space.items():
                # keys is state label #, values is state name

                if current_state == value:
                    transition_probs = self.transition_matrix[key]
                    possible_states = list(state_space.keys())                    
                    next_state_idx = np.random.choice(possible_states, replace= True, p=transition_probs)
                    prob *= transition_probs[next_state_idx]

            current_state = state_space[next_state_idx]
            states_list.append(current_state)              
            i +=1 

        # save important attributes to self
        self.current_state = current_state
        self.current_state_prob = prob
        
        # print("Possible states: " + str(states_list))
        # print("End state after " + str(num_steps) + " days: " + str(current_state))
        # print("Probability of the possible sequence of states: " + str(prob))

# ---------------------------------------------------------------------