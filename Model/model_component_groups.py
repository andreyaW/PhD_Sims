"""
model_component_group.py

Programming instruction create a group of objects from a desired number of component objects.
Components can be considered as parallel or series as seen in the class definitions imported

(C) 2023 Regents of the University of Michigan

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Created on Tues May 30 13:55:00 2020

@author: mdcoll, adware
 
Last Edited: Tues July 1 13:00 2023 by Andreya Ware (adware)
"""



from Model.model_series_component import series_comp
from Model.model_parallel_component import parallel_comp
from Model.utils import calculator as calc
from Model.utils import plotting_help as plotter

import numpy as np
import copy
import matplotlib.pyplot as plt

class component_group:
    
    ### GROUP INITIALIZATION           
    def __init__(self, assignment: int ,num_parts: int, num_sample_points: int, lifetimes: list[float], variances: list[float], parallel_list: list[int] = None, comp_names: list[str]= None):
        ''' a group of series or parallel components, can stand alone or be added to a system
        Args:
            num_parts: Number of parts that will be added to the group (total number of series comps)
            num_sample_points: Number of failures to generate for each component
            lifetimes: lifetimes to be used to define each component in the group
            variances: values to use for the variance of failure for each component's random distribution 
            parallel_list: the assignments of parts to be considered in parallel, each parallel part a seperate tuple
                           EXAMPLE: [(2,3) , (4,5,6)] = components 2 and 3 are parallel with each other 
                                                        then components 4,5, and 6 are parallel with each other
            comp_names: the names for each component in the group, optional ( parts can be labeled by their assignments)        
        Returns:
            component_group ; a group of components with the solved and saved R(t) and t. can be drawn using animation functions
        '''
        # Placeholder Parameters
        self.assignment =  assignment           # assigned reference index og the group
        self.objName = "Group #" + str(self.assignment)              # name of group can go here (cooling, engines, etc.)
        self.weight = 0
        
        #Initialized Parameters
        self.num_parts= num_parts                               # number of Components to create
        self.sample_size= num_sample_points                     # number of samples each componenet will be represented by
        self.avg_lifetimes= lifetimes                
        self.comp_variances= variances
        self.comp_names = comp_names
        
        # store parts parallel within the group
        self.parallel_list = parallel_list
        
        self.add_comps()                                 # creates a list storing the groups components 

        # tracking indicies for if the group is parallel with another object
        self.parallel = False                            # components are intiially assumed to be in series 
        self.added_in_parallel = False                   # a flag for system class (will make system skip parts after they have been added)   


### ADDING COMPONENTS TO THE GROUP 
#       (series components by default unless paralle list is passed in initialization)    
    def mark_parallel(self, parallel_list):
        ''' Function will mark the group as a parallel objects and store the assignments of
            its parallel counterparts so they are replaced during R(t) computation 
        Args:
            parallel_list = list of assignment to consider in parallel with this group                               
        Returns:
            None
        '''
        # store the assignment numbers of this components parallel counterparts
        self.parallels= parallel_list
            
        # flag component as parallel
        self.parallel= True
                
    
    
    def mark_comps_parallel(self):
        ''' Function will mark the components in the group as parallel objects and store 
            the assignments of their parallel counterparts so they are replaced during R(t) computation 
        Args:
            None                               
        Returns:
            None
        '''
        
        parallel_list = self.parallel_list
        # go through each tuple set in the list of tuples and store the parallel assignments to each part
        if type(parallel_list) == tuple:
            for i in range(len(parallel_list)):
                assignment= parallel_list[i]                                            # store the component being considered this iteration             
                copy_list= parallel_list[:i] + parallel_list[i+1:]                       # remove the item from the copy                    
                self.series_parts[assignment-1].mark_parallel(copy_list)                 # add the remining parts to the parallel set varible for this component
            
        else:
            for parallel_set in parallel_list:
                for i in range(len(parallel_set)):
                    assignment= parallel_set[i]                                            # store the component being considered this iteration             
                    copy_list= parallel_set[:i] + parallel_set[i+1:]                       # remove the item from the copy
                    self.series_parts[assignment-1].mark_parallel(copy_list)                 # add the remining parts to the parallel set varible for this component



    def add_comps(self):
        ''' Will create the desired number of component objects in the group
            all object will by default be serial components the solve R_t will replace them with parallels  
        Args:
            None                               
        Returns:
            None
        '''
        
        # grab comp information from self
        lifetimes= self.avg_lifetimes
        variances= self.comp_variances
        
        # generate n number of components for the group
        n= self.num_parts
        group=[series_comp(self.sample_size, lifetimes[i], variances[i],  i+1) for i in range(n)]                      
        
        # if the names are not defaulted to None, add each name to each component
        if self.comp_names != None:
            for i in range(n):
                group[i].objName = self.comp_names[i]
                    
        # store initialized comps to self
        group = np.array(group).T    # transposing list
        self.parts= group 
    
        # ensure a copy of the group with only series parts will always be available (for individual characteristics of each component)
        self.series_parts = copy.deepcopy(group)                      # COPY OF THE SERIES GROUP (LIST of component objects)          
        
        # mark parts parallel if requested 
        if self.parallel_list != None:
            self.mark_comps_parallel()
        
        # solve the R_t of the group and store the components which are causing the group to fail
        self.solve_group_R_t()  # (also marks parallels accordingly)                                        



    def solve_group_R_t(self, figure_dict: dict= None, save_folder: str= None): 
        ''' This function will be used to Generating the R_t curves from the 
            random distributions generated for each component in the grouptem
        Args:
            figure_dict: the dictionary to save figure to (saves title as figure Key and the axes as Values)
            save_folder: the folder directory to save the figure too after being generated
        Returns:
            None
        '''
        #save all parts in series to be referenced later
        original_series_group = copy.deepcopy(self.series_parts)
        
        # create a np.array for storring all the updated components (may or may not have parallels)       
        updated_comps=[]
        
        # initialize space to store all R(t) curves and fail times in matrix
        ouput_size= (len(original_series_group), self.sample_size)
        group_R_t = np.zeros((ouput_size))
        group_t= np.zeros_like(group_R_t)
        
        # tracking number of parts in parallel in the group 
        count_Of_Parallels =0
        
        # loop through and solve for R(t) of each part
        for i, comp in enumerate(original_series_group):
  
            # for series components....
            if comp.parallel== False:
                # solve R_t over desired lookup times and store to group_R_t matrix
                group_R_t[i], group_t[i]= comp.R_t, comp.t                                                        
                comp.assignment = i+1

                # add component to updated comps list
                updated_comps.append(comp)                                                         

            # for parallel components...
            elif comp.parallel== True:  
                
                # check to see if part has already been added                         
                if comp.added_in_parallel == True:                                                 # skip the part it if it's reliabilitity has already been added
                    # update the total count of parallel parts
                    count_Of_Parallels = sum([part.added_in_parallel for part in original_series_group])                     
                    continue
                
                # if part has not be added, add it to the group_R_t matrix   
                else:
                    parallel_parts=list( comp.parallels )
                    parallel_parts.append(comp.assignment)                                        # adding all series assignements to single list

                    # replace the series comp a parallel comp
                    comp= parallel_comp(parallel_parts, self.parts, original_series_group, count_Of_Parallels)     
                    
                    # solve parallel_R_t and store to part
                    group_R_t[i], group_t[i]= comp.R_t, comp.t                                                        
                    comp.assignment = i+1
                    
                    # add component to updated list
                    updated_comps.append(comp)                                                         
                                                             

        # remove any zero rows that were added and never replaced (result of series components being considered in parallel)        
        group_t = group_t[~np.all(group_t <= 0, axis=1)]
        group_R_t = group_R_t[~np.all(group_R_t <= 0, axis=1)]

        # fill in end points for all curves
        latest_failure = np.max( np.max(group_t))
        earliest_failure = np.min( np.min(group_t)) 
        group_t = np.c_[earliest_failure * np.ones(group_t.shape[0]), group_t, latest_failure * np.ones(group_t.shape[0])]
        group_R_t = np.c_[group_R_t[:,0], group_R_t , group_R_t[:,-1]]

        # REPLACE parts with the updated components to include the desired parallels    
        self.parts= np.array(updated_comps).T  
        self.num_parts = len(self.parts)    
        
        # store updated curves to each comp
        for i,comp in enumerate(self.parts):
            comp.R_t_solved = group_R_t[i]
            comp.t_solved = group_t[i]

        # calling function from calculator that will determine and store group R(t)
        self.R_t, self.t, self.failing_part = calc.determine_R_t_from_multiple_r_ts(group_R_t, group_t)

        # plot the group_R_t curve after solving
        if figure_dict != None: 
            plotter.plot_R_t(self, figure_dict, save_folder) 
            
        # # ensure R_t for reference has the same number of sample points in the future
        # max_time = np.max(self.t)
        # lookup_t = np.linspace(0, max_time, self.sample_size+2)
        # self.R_t, self.t, self.failing_part = calc.find_lookup_R_t(self.R_t, self.t, lookup_t,  self.failing_part)

        # update the component group weight
        self.determine_group_weight()

        # print("done with comp_group R_t")
 
 
    def get_lookup_R_t(self, times_to_lookup, figure_dict= None, save_folder=None):
        ''' From the solved R_t of the system, grab a specific lookup R_t
        Args:
            times_to_lookup: an array of lookup times to grab from the R_t curve
            figure_dict: the dictionary to save figure to (saves title as figure Key and the axes as Values)
            save_folder: the folder directory to save the figure too after being generated
        Returns:
            None
        '''
        look_up_R_t , lookup_t= calc.find_lookup_R_t(self.R_t, self.t, times_to_lookup)
        self.lookup_R_t, self.lookup_t = look_up_R_t, lookup_t
       
        # generate lookup R_t for each component
        for comp in self.parts:
            comp.get_lookup_R_t(times_to_lookup)
        
        if figure_dict != None:
            plotter.plot_lookup(self, figure_dict, save_folder)
        
        
        
    def determine_average_failure_t(self, mission_length: float = None):
        ''' determine the number of times each component in the system fails over a specified period
        Args:
            mission_length: a time to normalize the average failure time over (if provided) 
        Returns:
            None
        '''
        # determine and store the average failure time to self        
        calc.determine_average_failure_t(self, mission_length)

        return self.avg_fail_time
    


    def determine_fail_rate(self, operational_time):
        ''' determine the number of times each component in the system fails over a specified period
        Args:
            operational_time: the length of time to determine how many times the part will fail 
        Returns:
            None
        '''
        # determine and store the failure rate to self        
        calc.determine_fail_rate(self, operational_time)
        

    def determine_group_weight(self):
        self.weight=0
        for part in self.series_parts:
            self.weight = self.weight + part.weight