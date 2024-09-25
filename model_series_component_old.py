from matplotlib import pyplot as plt
from Model.utils import calculator as calc

import scipy.stats as sp
import random
import numpy as np
# ------------------------------------------------------------------------------------------------------------------------------------------------ #    

class series_comp:
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

        # Labelling Parameters
        self.objName = "Component "  + str(assignment)          # give each component a name based on system assignment
        if assignment != None:
            self.assignment = assignment                        # indexing part number
        else: 
            self.assignment = series_comp.assignment
            series_comp.assignment +=1

        # Distribution Parameters
        self.sample_size = n                                    # number of distribution points to generate
        self.distType = sp.norm                                 # default distrubution of random failures
        self.meanLife = mean_life                               # mean life of the component
        self.scale   = variance                                 # default variance (scale) for failure distribution

        # Size and Weight Parameters
        self.weight = 0                                         # Weight of Component         

        # System Architecture Parameters
        self.parallel = False                                   # components are intiially assumed to be in series
        self.added_in_parallel = False                          # a flag for system class (will make system skip parts after they have been added)   
        self.parallelComps =[]                                  # assuming the component is in series and therfore has no parallel counterparts

        # call initialization function which will create an initial random failure distribution for the component
        self.generate_comp()                                                                            



    def generate_comp(self):
        ''' Generates random variate distrubution for component life of given size n (list)
        Args: 
            None
        Returns
            None
        '''

        n=self.sample_size 
        d=self.distType
        meanLifetime= self.meanLife
        variance = self.scale

        #create and save distrubution with given mean life and variance
        componentDist= d.rvs(loc=meanLifetime, size=n, scale=variance, random_state= random.randint(1,999)) 

        # store generated random distribution to component
        self.random_fail_times = componentDist                      # Randomly generated distribution of times til failure for a component       

        # solve for r_t using random fails
        self.R_t, self.t= calc.random_to_R_t(componentDist)



    def mark_parallel(self, parallelsList_n):
            '''Flags a particular component as paraller and then assigns that components paralle counterpart(s)
            Args
                parallelsList_n: the list of parallel components and their counterparts.
                                 EXAMPLE: [(2,3) , (4,5,6)] = components 2 and 3 are parallel with each other 
                                                                then components 4,5, and 6 are parallel with each other
            Returns:
                None
            '''
            
            #store the assignment numbers of this components parallel counterparts
            self.parallels= parallelsList_n
            
            #flag component as parallel
            self.parallel= True
            
            #print("component {} now has parallel counterparts {}".format(self.assignment , self.parallelComps))


            
    def get_lookup_R_t(self,lookup_times):
        ''' 
        Args: 
            lookup_times: 
        Returns
            None
        '''
        try:
            lookup_R_t, lookup_t = calc.find_lookup_R_t(self.R_t_solved, self.t_solved, lookup_times)
            self.lookup_R_t, self.lookup_t=  lookup_R_t, lookup_t

        except: 
            lookup_R_t, lookup_t = calc.find_lookup_R_t(self.R_t, self.t, lookup_times)
            self.lookup_R_t, self.lookup_t=  lookup_R_t, lookup_t



    def update_mean_life(self,  mean_life: float= 0, variance: float= 200, dist_type = sp.norm): 
        ''' Takes a component and updates the mean lifetime, variance and ditribution type to desired parameters
        Args:
            mean_life: the mean life / average failure time of the times to failure distribution
            input_scale: the scale factor or variance of the times to failure distribution
                        *scale has a default value initialized in class definition, to reset to default 
                        scale value use 10.0
        Returns: 
            None
        '''
        self.meanLife = mean_life
        self.scale = variance
        self.distType = dist_type

        self.generate_comp()



    def determine_average_failure_t(self, mission_length:float = None) : 
        ''' From the random failure times generated, determine the average time of failure of each part
        Args:
            mission_length : the length of time to normalize the average time of failure over
        Returns:
            avg_failure_t: the average time of failure of the system, normalized by mission length if length is provided
        '''
        
        all_fails = self.random_fail_times
        
        total_time = 0
        for fail in all_fails:
            total_time += fail
        avg_failure_t= total_time / len(all_fails)

        # normalize time if mission length is provided
        if mission_length != None: 
            avg_failure_t = avg_failure_t / mission_length

        # store the failure time to self        
        self.avg_fail_time = avg_failure_t

        return avg_failure_t