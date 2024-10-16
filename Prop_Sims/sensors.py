# a Markov Decision Process for the sensor model
# sensor can be in one of two states (working (A) or failed(B))
# probability of the sensor failing is 0.5 (i.e probability of the sensor working is 0.5)   
# the failed state is an absorbing state


import numpy as np


# a Markov Decision Process for the component health model using numpy
# component can be in one of two states (working (A) or failed(B))
# the failed state is an absorbing state

class comp: 
    
    def __init__(self):

        self.transition_prob = 0.1                  # probability of the part failing is 0.1 (i.e probability of the part working is 0.9)
        self.state = self.MDP_model()

    def MDP_model(self): 
        # assumes two states only right now
        self.state_space = ["working", "failed"]
        prob_fail = self.transition_prob

        self.transitions = np.array([["WW", "WF"], 
                                     ["FF", "FW"]])
        
        self.transition_matrix= np.array([[ 1-prob_fail , prob_fail ], 
                                          [ prob_fail, 1-prob_fail ]])

        return "working"                                # the component starts in a working state


    def get_next_state(self): 
        self.state = self.forecast(1)
        return self.state


    def forecast(self, num_steps):

        # after installation, the component can either stay in the same state or transition to another state
        next_state=""
        state_space = self.state_space 

        for i in range(num_steps):
            if self.state == state_space[0]:
                if np.random.uniform(0, 1) <= self.transition_prob: 
                    next_state = 'failed'
                else:
                    next_state = 'working'
            else:
                next_state = 'failed'

        return next_state