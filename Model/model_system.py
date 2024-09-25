
from Model.model_series_component import series_comp
from Model.model_parallel_component import parallel_comp
from Model.model_component_groups import component_group as comp_group
from Model.utils import calculator as calc
from Model.utils import plotting_help as plotter
from typing import Union


import numpy as np
import copy



class system:    
    '''
    Class used to add components or groups of components together to create a single system
    '''
    
    ### SYSTEM INITIALIZATION           
    def __init__(self, assignment: int, list_of_items: list[Union[series_comp, parallel_comp, comp_group]], num_sample_points: int, parallel_list: list[tuple] = None):
        '''Initializes a ship system from a list with n number of objects

        Args:
            assignement: the assigned number of this system
            list_of_items: a list containing the series or parallel comps or a comp_group           
            num_sample_points: number of failures that was generated for each component
            parallel_list: the assignments of parts to be considered in parallel, each parallel part a seperate tuple
                           EXAMPLE: [(2,3) , (4,5,6)] = components 2 and 3 are parallel with each other 
                                                        then components 4,5, and 6 are parallel with each other

        Returns
        -------------------------------------------------------------------
        a list of n number of component objects
        '''

        # Placeholder Parameters
        self.assignment = assignment                            # assigned reference index og the group
        self.objName = "System #" + str(self.assignment)        # name of group can go here (cooling, engines, etc.)
        
        # Initialized Parameters
        self.sample_size= num_sample_points                     # number of samples each componenet will be represented by
        self.parts = list_of_items
        for i in range(len(self.parts)):
            self.parts[i].assignment = i+1
        self.num_parts= len(list_of_items)                      # number of Components to create
        
        # create a copy of the parts before parallel consideration for refernce later
        self.series_parts = copy.deepcopy(self.parts)
        
        # store parts parallel within the group        
        self.parallels = parallel_list
        
        # mark parts parallel if requested 
        if self.parallels != None:
            self.mark_comps_parallel()        
            
        self.weight= 0



    def mark_comps_parallel(self):
        '''Mark the appropriate objects of the system as parallel so they are replaced during R(t) computation 
        Args:
            None                               
        Returns:
            None
        '''
        
        parallel_list = self.parallels
        # go through each tuple set in the list of tuples and store the parallel assignments to each part
        if type(parallel_list) == tuple:
            for i in range(len(parallel_list)):
                assignment= parallel_list[i]                                            # store the component being considered this iteration             
                copy_list= parallel_list[:i] + parallel_list[i+1:]                       # remove the item from the copy                    
                self.series_parts[assignment-1].mark_parallel(copy_list)                 # add the remining parts to the parallel set varible for this component
            
        else:
            for parallel_set in parallel_list:
                for i in range(len(parallel_set)):
                    assignment= parallel_set[i]-1                                            # store the component being considered this iteration             
                    copy_list= parallel_set[:i] + parallel_set[i+1:]                       # remove the item from the copy
                    self.series_parts[assignment].mark_parallel(copy_list)                 # add the remining parts to the parallel set varible for this component
                    self.series_parts[assignment].assignment = assignment+1


            
    def solve_sys_R_t(self, figure_dict: dict= None, save_folder: str= None, figure_name: str= None): 
        ''' This function will be used to Generating the R_t curves from the 
            random distributions generated for each component in the grouptem
        Args:
            figure_dict: the dictionary to save figure to (saves title as figure Key and the axes as Values)
            save_folder: the folder directory to save the figure too after being generated
            figure_name: optional name to save the figure under
        Returns:
            None
        '''
        #save all parts in series to be referenced later
        original_series_sys = copy.deepcopy(self.series_parts)    
        self.objName = "System #" + str(self.assignment)        # name of group can go here (cooling, engines, etc.)

        # create a np.array for storring all the updated components (may or may not have parallels)       
        updated_comps=[]
        
        # initialize space to store all R(t) curves and fail times in matrix
        ouput_size= (self.num_parts, self.sample_size)
        sys_R_t = np.zeros((ouput_size))
        sys_t= np.zeros_like(sys_R_t)
        
        #tracking index for number of parallels in the system 
        count_Of_Parallels =0
        
        # solve for R(t) of each part
        for i, comp in enumerate(original_series_sys):
            
            # for series components components or groups....
            if comp.parallel== False:
                # solve R_t over desired lookup times and store to sys_R_t matrix
                sys_R_t[i], sys_t[i]= comp.R_t[-(self.sample_size):], comp.t[-(self.sample_size):]                                                        
                comp.assignment = i+1
                comp.objName = f'Component {comp.assignment}'
                
                # add component to updated comps list
                updated_comps.append(comp)                                                         

            # for parallel components or groups...
            elif comp.parallel== True:  
                
                # check to see if part has already been added                         
                if comp.added_in_parallel == True:                                                 # skip the part it if it's reliabilitity has already been added
                   
                    # update the total count of parallel parts
                    count_Of_Parallels = sum([part.added_in_parallel for part in original_series_sys])                     
                    continue
                
                # if part has not be added, add it to the system R_t matrix   
                else:
                    parallel_parts=list( comp.parallels )
                    parallel_parts.append(comp.assignment)                                        # adding all series assignements to single list

                    # replace the series comp a parallel comp or comp_group
                    comp= parallel_comp(parallel_parts, self.parts, original_series_sys, count_Of_Parallels)     
                    comp.assignment = i+1
                    comp.objName = f'Component {comp.assignment}'
                    
                    # solve parallel_R_t and store to part
                    sys_R_t[i], sys_t[i]= comp.R_t[-(self.sample_size):], comp.t[-(self.sample_size):]                                                        
                    
                    # add component to updated list
                    updated_comps.append(comp)                                                                                              

        # remove any zero rows that were added and never replaced (result of series components being considered in parallel)        
        sys_t = sys_t[~np.all(sys_t <= 0, axis=1)]
        sys_R_t = sys_R_t[~np.all(sys_R_t <= 0, axis=1)]

        # fill in end points for all curves
        latest_failure = np.max( np.max(sys_t))
        earliest_failure = np.min( np.min(sys_t)) 
        sys_t = np.c_[earliest_failure * np.ones(sys_t.shape[0]), sys_t, latest_failure * np.ones(sys_t.shape[0])]
        sys_R_t = np.c_[sys_R_t[:,0], sys_R_t , sys_R_t[:,-1]]

        # REPLACE parts with the updated components to include the desired parallels    
        self.parts= np.array(updated_comps).T  
        self.num_parts = len(self.parts)    
        
        # store updated curves to each comp
        for i,comp in enumerate(self.parts):
            comp.R_t_solved = sys_R_t[i]
            comp.t_solved = sys_t[i]

        # calling function from calculator that will determine and store group R(t)
        self.R_t, self.t, self.failing_part = calc.determine_R_t_from_multiple_r_ts(sys_R_t, sys_t)

        # plot the group_R_t curve after solving
        if figure_dict != None: 
            plotter.plot_R_t(self, figure_dict, save_folder, figure_name) 
            
        # update the component 
        self.determine_sys_weight()
        
 
    def get_lookup_R_t(self, times_to_lookup: list[float], figure_dict: dict= None, save_folder:str =None):
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
            save_path = plotter.plot_lookup(self, figure_dict, save_folder)
            return save_path

    def determine_fail_rate(self, operational_time):
        ''' determine the number of times each component in the system fails over a specified period
        Args:
            operational_time: the length of time to determine how many times the part will fail 
        Returns:
            None
        '''
        # determine and store the failure rate to self        
        calc.determine_fail_rate(self, operational_time)


    def determine_MTBF(self):
        ''' determine the number of times each component in the system fails over a specified period
        Args:
            None
        Returns:
            None
        '''
        for part in self.series_parts:
            calc.determine_MTBF(part)
        calc.determine_MTBF(self)
        


    def count_components(self):
        num_parts= 0
        for part in self.series_parts:
            if isinstance(part, comp_group):
                num_parts+= part.num_parts
            else:
                num_parts+= 1
        
        # save to self
        self.comp_count = num_parts
        
        return num_parts
    
    

    def determine_sys_weight(self):
        self.weight= 0
        for part in self.series_parts:
            if isinstance(part, comp_group):
                part.determine_group_weight()
                self.weight = self.weight + part.weight
            else:
                self.weight = self.weight + part.weight