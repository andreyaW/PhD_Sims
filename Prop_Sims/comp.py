from markovChain import *

class comp:
    def __init_():

        ' a simple model of a component object '
        
        comp_failure_mat = np.array([[0.6, 0.3, 0.1],
                                    [0.0, 0.5, 0.5],
                                    [0.0, 0.2, 0.8]])
        comp = markovChain(3,comp_failure_mat)

