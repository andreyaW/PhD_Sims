from markovChain import *

class sensor:
    def __init_():

        ' a simple model of a sensor object '

        comp_failure_mat = np.array([[0.5, 0.5],
                                    [0.0, 1.0]])
        comp = markovChain(2,comp_failure_mat)
        
        
        N= 3
        transition_matrix = np.array([[0.1, 0.3, 0.6], 
                                    [0.2, 0.3, 0.5], 
                                    [0.4, 0.5, 0.1]])
        sensor = markovChain(3, transition_matrix)
        sensor.forecast(5)