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
        # next_state_probs = np.ones((len(self.state_space),1))   # 1-D array to track the probabilities of the next state

        for i in range(num_steps):
            if self.state == state_space[0]:
                if np.random.uniform(0, 1) <= self.transition_prob: 
                    next_state = 'failed'
                else:
                    next_state = 'working'
            else:
                next_state = 'failed'

        return next_state

            # for j,state in enumerate(state_space):

            #     if self.state == state:
                    
            #         # use the probabilities in the table to determine the current state of the comp
            #         next_state_probs = self.transition_matrix[j].T * prob

            #         # select state with the highest probability as current state
            #         index= np.argmax(next_state_probs)
            #         return state_space[index]


        #     if np.random.uniform(0, 1) <= self.transition_prob: 
        #         return 'failed'
        #     else:
        #         return 'working'
        # else:
        #     return 'failed'


# # A function that implements the Markov model to forecast the state/mood. 
# def activity_forecast(days):
#     # Choose the starting state
#     activityToday = "Sleep"
#     print("Start state: " + activityToday)
#     # Shall store the sequence of states taken. So, this only has the starting state for now.
#     activityList = [activityToday]
#     i = 0
#     # To calculate the probability of the activityList
#     prob = 1
#     while i != days:
#         if activityToday == "Sleep":
#             change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
#             if change == "SS":
#                 prob = prob * 0.2
#                 activityList.append("Sleep")
#                 pass
#             elif change == "SR":
#                 prob = prob * 0.6
#                 activityToday = "Run"
#                 activityList.append("Run")
#             else:
#                 prob = prob * 0.2
#                 activityToday = "Icecream"
#                 activityList.append("Icecream")
#         elif activityToday == "Run":
#             change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
#             if change == "RR":
#                 prob = prob * 0.5
#                 activityList.append("Run")
#                 pass
#             elif change == "RS":
#                 prob = prob * 0.2
#                 activityToday = "Sleep"
#                 activityList.append("Sleep")
#             else:
#                 prob = prob * 0.3
#                 activityToday = "Icecream"
#                 activityList.append("Icecream")
#         elif activityToday == "Icecream":
#             change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
#             if change == "II":
#                 prob = prob * 0.1
#                 activityList.append("Icecream")
#                 pass
#             elif change == "IS":
#                 prob = prob * 0.2
#                 activityToday = "Sleep"
#                 activityList.append("Sleep")
#             else: 
#                 prob = prob * 0.7
#                 activityToday = "Run"
#                 activityList.append("Run")
#         i += 1  
#     print("Possible states: " + str(activityList))
#     print("End state after "+ str(days) + " days: " + activityToday)
#     print("Probability of the possible sequence of states: " + str(prob))

# # Function that forecasts the possible state for the next 2 days
# activity_forecast(2)