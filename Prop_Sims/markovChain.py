import numpy as np

class markovChain:
    def __init__(self, N, transition_matrix, initial_state:int = 0):
        '''
        Parameters:
            1. N : integer
                number of states in the chain

            2. transition_matrix: np.array
                trainsition probabilities from state to state 

        Returns:
            1. current_state; 
                the starting state of the model
        '''
        self.num_states = N

        # # check for a properly defined transition matrix (sum across each row should be 1)
        # for i in range(transition_matrix.shape[1]):
        #     row = transition_matrix[i, :]
        #     if sum(row) != 1.0:
        #         raise (ValueError("The transition matrix must sum to 1 for each state (across each row)"))
        self.transition_matrix = transition_matrix
        

        # initialize the state space
        self.state_space = self.define_state_space(N)
        
        # the initial space is working unless specified otherwise    
        if initial_state == 0: 
            initial_state = self.state_space[initial_state]    
    
        self.current_state = initial_state
        self.current_state_prob = 1         # 100% chance of starting at the designated inital state


    def define_state_space(self, N):
        vals = ["working", "failed"]
        if N> 2: 
            for i in range(N-2):
                vals.insert(-1,"partially working (" + str(i+1) + ")")
        keys = [i for i in range(N)]
        state_space = dict(zip(keys, vals))

        return state_space
    

    def forecast(self, num_steps):
        current_state = self.current_state
        state_space = self.state_space
        
        states_list = [current_state]
        print("Start state: " + str(current_state))

        prob = self.current_state_prob
        i = 0
        while i != num_steps:

            for key, value in state_space.items():
                
                if current_state == value:
                    transition_probs = self.transition_matrix[key]
                    possible_states = [k for k in state_space.keys()]
                    next_state_idx = np.random.choice(possible_states, replace= True, p=transition_probs)
                    prob *= transition_probs[next_state_idx]

            current_state = state_space[next_state_idx]
            states_list.append(current_state)              
            i +=1 
        self.current_state = current_state
        self.current_state_prob = prob
        
        # print("Possible states: " + str(states_list))
        # print("End state after " + str(num_steps) + " days: " + str(current_state))
        # print("Probability of the possible sequence of states: " + str(prob))


# ---------------------------------------------------------------------