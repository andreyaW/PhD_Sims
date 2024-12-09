from Prop_Sims.shipModel.sensedComp_old import sensedComp

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
            :param parallel_connections: list of tuples the list of parallel connections within the system. EX: [(2,3,4)] results in a system with components #2, #3 and #4 within the system are considered to be operating in parallel with each other.  
        
        """

        self.state = self.defineSystem(sensed_comps, parallel_connections)

# ---------------------------------------------------------------------

    def defineSystem(self, sensed_comps, parallel_connections):

        '''
            Define the system as a collection of sensed components with a known architecture (series or parallel connections)

            :param sensed_comps: list sensedComps a list containing the sensed components comprising the system
            :param parallel_connections: list of tuples the list of parallel connections within the system. EX: [(2,3,4)] results in a system with components #2, #3 and #4 within the system are considered to be operating in parallel with each other.  
        
        '''
        # Define the system as a collection of sensed components with a known architecture (series or parallel connections)
        # EX: [(2,3,4)] results in a system with components #2, #3 and #4 within the system are considered to be operating in parallel with each other.  
        # EX: [(2,3)] results in a system with components #2 and #3 within the system are considered to be operating in series with each other.  
        # EX: [] results in a system with no parallel connections.  
        # EX: [(2,3,4),(5,6)] results in a system with components #2, #3 and #4 within the system are considered to be operating in parallel with each other and components #5 and #6 are considered to be operating in parallel with each other.  

        
