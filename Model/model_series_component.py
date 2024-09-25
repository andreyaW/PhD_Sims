import scipy as sp
from Model.utils import calculator as calc

class Series_Component: 
    ''' A simple series component object with a random failure distribution of size n '''

    def __init__(self, n: int, mean_life:float= 0, variance:float = 200, assignment: int= None):
        '''
        Params:
            n (int) :
                number of Samples to generate for the component distrubution 
            mean_life (float) :
                the average failure time of the component
            variance (float) :
                the spread of the failure distribution fo rthis component
            assignment (int) :
                the components number within the system or group for labeling and tracking purposes
        Returns:
            series_component:  stored python object with a distrubution of default type (sp.norm.rvs) and size n
        '''

        # Failure Distribution Parameters
        self.sample_size = n                                    # number of distribution points to generate
        self.dist_type = sp.stats.norm                                # default distrubution of random failures
        self.mean_life = mean_life                              # mean life of the component
        self.scale   = variance                                 # default variance (scale) for failure distribution

        # System Architecture Parameters
        self.parallel = False                                   # components are intiially assumed to be in series  
        self.added_in_parallel = False                          # a flag for system class (will make system skip parts after they have been added)
        self.parallel_comps = []                                # assuming the component is in series and therfore has no parallel counterparts
        self.generate_comp()                                    # initialization function which will create initial component failure distribution

        # Size and Weight Parameters
        self.weight = 0                                         # weight of the component

        # Labelling Parameters
        if assignment != None:
            self.obj_name = "Component "  + str(assignment)     # make component name based on its assignment
            self.assignment = assignment                        # store assignment for indexing

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Failure Distribution Functions
    def generate_comp(self):
        ''' Generates random distrubution for component life of given size n (list)
        Params: 
            None
        Returns
            None
        '''
        # generate random variate distribution of comp fail times life
        self.random_fail_dist = self.dist_type.rvs(loc=self.mean_life, scale=self.scale, size=self.sample_size)

        # from the random failure times distribution solve for the component reliability over time
        self.R_t, self.t = calc.random_to_R_t(self.random_fail_dist)


    def get_lookup_R_t(self, lookup_times):
        ''' Returns the reliability of the component at specific times
        Params:
            lookup_times (list) : 
                list of times to lookup the reliability of the component
        Returns:
            reliability (list) : 
                list of the reliability of the component at the given times
        '''
        # lookup the reliability of the component at specific times
        self.lookup_R_t, self.lookup_t= calc.find_lookup_R_t(self.R_t, self.t, lookup_times)
        return self.lookup_R_t, self.lookup_t
    

    def compute_MTTF(self):
        ''' Returns the mean time to failure of the component
        Params:
            None
        Returns:
            MTTF (float) : 
                mean time to failure of the component
        '''
        return calc.compute_MTTF(self)

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Component Health Assesment Functions
    def report_state(self):
        ''' Returns the output signal of the component at a given time
        Params:
            time (float) : 
                the time at which the component signal is being requested
        Returns:
            signal (int) : 
                the signal of the component at the given time
        '''
        signal = 1000 

        return signal

    def update_health(self):
        ''' Updates the state of the component based on and action or event
        Params:
            None
        Returns:
            None
        '''
        # update the state of the component based on the maintenance actions or events that have occured


        # **** To Do ****

        return

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # System Architecture Functions
    def mark_comp_parallel(self, parallelsList_n):
        ''' Marks the component as a parallel component with given parallel counterparts
        Params:
            parallelsList_n (list) :
                list of the assignment numbers of the components parallel counterparts
                EXAMPLE: [(2,3) , (4,5,6)] 
                        components 2 and 3 are parallel with each other and
                        components 4,5, and 6 are parallel with each other
        Returns:
            None
        '''
        # store the assignment numbers of this components parallel counterparts
        self.parallels= parallelsList_n
        
        # flag component as parallel
        self.parallel= True
        
        # print("component {} now has parallel counterparts {}".format(self.assignment , self.parallelComps))

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # System Architecture Functions