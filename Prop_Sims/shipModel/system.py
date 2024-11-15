from sensedComp import sensedComp

class system: 
    '''
        a simple model of a ship system
        To run this file enter in terminal: python -i system.py
    '''

    def __init__(self, 
                 sensed_comps = [sensedComp(), sensedComp(), sensedComp()],
                 parallel_connections = [(2,3)]):
        """
            Initialize the system as a collection of sensed components with a known architecture (series or parallel connections)

            :param sensed_comps: list sensedComps a list containing the sensed components comprising the system
            :param parallel_connections: list of tuples the list of possible parallel components within the system. i.e. [(2,3,4)] results in a system with components #2, #3 and #4 within the system are considered to be operating in parallel with each other.  
        
        """
        self.defineSystem(sensed_comps, parallel_connections)

# ---------------------------------------------------------------------
    def defineSystem(self, list_of_comps, list_of_parallels)-> None:
        """
        Define the system as a collection of sensed components with known parallel and series connections. 

        :params sensed_comps: list sensedComps 
        :params parallel_connections:

        """
        # save to self
        self.comps = list_of_comps
        self.parallels = list_of_parallels

        # determine state of comps to be considered in parallel
        system_states = []
        for parallel in list_of_parallels:
            parallel_states = []
            for idx in parallel:
                comp = list_of_comps[idx-1]
                parallel_states.append(comp.state)
                group_state = parallel_logic(parallel_states, int(len(parallel_states)/2)) # assumes majority must be functional
            system_states.append(group_state)

        # # determine state of groups and series comps all together
        # list_of_parallels = set(list_of_parallels) # flatten the list of parallels
        # list_of_series = [i for i in range(len(list_of_comps)) if i not in list_of_parallels]
        # for series in list_of_series:            
        #     system_states.append(system_states[idx])        
        # self.state = series_logic(system_states)

# ---------------------------------------------------------------------





# ---------------------------------------------------------------------
def parallel_logic(parallel_states, k):
    """
    Implement the logic for parallel connections. k out of in should be used to determine the state of the combination of components.

    """

    

# ---------------------------------------------------------------------
def series_logic(series_states):
    """
    Implement the logic for series connections. 

    """

# ---------------------------------------------------------------------