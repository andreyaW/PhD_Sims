from markovChain import *

class comp:
    def __init__(self):
        ' a simple model of a component object '
        
        comp_failure_mat = np.array([[0.6, 0.3, 0.1],
                                    [0.0, 0.5, 0.5],
                                    [0.0, 0.2, 0.8]])
        number_of_states = 3
        self.markov_model = markovChain(number_of_states, comp_failure_mat)
        
    def generate_states(self, num_days):
        return self.markov_model.forecast(num_days)