"""
model_vessel.py

Contains class definition the model SimpleUSV2

(C) 2023 Regents of the University of Michigan

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Created on Tues May 30 17:00:00 2020

@author: mdcoll, adware
 
Last Edited: Tues July 18 11:00 2023 by Andreya Ware (adware)
"""

from Model.model_component_groups import component_groups as comp_group
from Model.utils import plotting_help as plotter
from Model.utils import calculator as calc

import numpy as np

class vessel:
    '''
    Class used to create first order USV model
    '''
    
    assignment= 1
    
    def __init__(self, num_systems, num_comps):
        '''
        Initializes a simple USV object, takes three inputs and has no returned output.

        Parameters
        --------------------------------------------------------------------
        1.num_systems: integer
            Number of Major systems to be considered   

        2.num_comps: integer , integer array, list
            Number of components per system, integer arrays can specifies different number of compoonents per system
        
        3.n: integer
            Number of sample points/ ship instances to generate for component distribution

        Returns
        -------------------------------------------------------------------
        None.
        '''
        #Inherited Parameter
        vessel_assignment = vessel.assignment
        vessel.assignment += 1
        
        #Initialized Parameters
        self.num_systems = num_systems          # Number of Vessel Systems
        self.num_comps = num_comps              # Number of Components in Each Vessel System
        
        #Placeholder Parameters (assigned later through class functions)
        self.ship_systems = []                            #place holder for systems objects to be defined in
        self.total_comp_count = 0

        # self.define_systems()




    def define_systems(self, num_samples, lifetimes= None, variances= None, comp_names = None):
        '''
        Sets up the systems in the vessel based on the values given

        Parameters
        -------
        1.  num_samples: integer
            number of random failures to generate for each system
        
        2.  lifetimes: matrix of floats
            average life of each component to be generated
        
        3.  variances: matrix of floats
            number of units to stretch/vary average lifetime over 
                        
        1.  comp_names: matrix of strings
            names for each component on the ship
        
            

        Returns
        -------
        Ship Systems 
        '''
        num_systems = self.num_systems
        num_comps = self.num_comps

        self.num_samples = num_samples      # save to self the number of ship failures modelled for this vessel configuration
      
        # ensure the number of components is made into a list
        if type(num_comps) == int:
            num_comps = [num_comps for i in range(num_comps+1)]

        default_lifetime = 500      # hours
        default_variance = 100      # hours
        default_comp_name = "Basic Ship Component"

        # Initialize systems with desired number of components and lifetimes
        for i in range(num_systems):
            
            # create a default lifetime if none is provided
            if lifetimes is None:
                sys_lifes= [default_lifetime for j in range(num_comps[i]+1)]
            else:
                #         if num_Sys == 1:  
                sys_lifes= lifetimes[i]
        
            # create variances if none is provided
            if variances is None:
                sys_vars= [default_variance for j in range(num_comps[i]+1)]
            else:
                if type(variances) == int:
                    sys_vars = [variances for j in range(num_comps[i]+1)] 
                else:
                    sys_vars= variances[i]
                
            # create names if none is provided
            if comp_names is None:
                sys_names= [default_comp_name for j in range(num_comps[i]+1)]
            else: 
                sys_names= comp_names[i]
        
            # initialize the system with the selected parameters
            self.ship_systems.append(model_system( num_comps[i], num_samples,  sys_lifes, sys_vars, sys_names) )
           
            # give the system an assignment 
            sysNum= i+1
            self.ship_systems[i].assignment= sysNum
         
            # update the ship class to account for the new system and part
            self.total_comp_count = self.total_comp_count + num_comps[i] 
                       
        print(f"A vessel with {self.num_systems} systems and {self.total_comp_count} total components has been initialized.")
        print(self.ship_systems, "\n")


    
        
    def mark_parallel_comps(self, system_num , parallelsList):
        '''
        Takes components of a series system and parks them as parallel components

        
        Parameters
        --------------------------------------------------------------------
        1.system_num: integer
            the assigned number of the system to add parallel components to   

        2. parallelsList: list of integer tuples
            the list of parallel components and their counterparts.
                EXAMPLE: [(2,3) , (4,5,6)] = components 2 and 3 are parallel with each other and 
                                             components 4,5, and 6 are parallel with each other
        
                                             
        Returns
        -------------------------------------------------------------------
        None.
        '''

        sysNum=system_num #index of system to add parallel components to
        
        #preface which system the parallel component is being added to 
        #print(f"For system number {sysNum} ...")

        system = self.ship_systems[sysNum-1]     #systems indexed starting at 0 (system 1 = assignment 0)
        system.mark_comps_parallel(parallelsList)
    
    
    
    def compute_ship_R_t(self, figure_dict= None, save_folder=None):
        
        # go through each system and solve the reliability curves
        systems = self.ship_systems
        sys_R_ts, sys_ts = [] , []
        for sys in systems:
            
            sys.solve_sys_R_t(figure_dict, save_folder)

            # lookup each R_t along a minimum sampling time (make them even in length)
            max_time = np.max(sys.t)
            lookup_t = np.linspace(0,max_time,self.num_samples)
            sys_R, sys_t= calc.find_lookup_R_t(sys.R_t, sys.t, lookup_t)
            
            # append the look up and R_ts to a list
            sys_R_ts.append(sys_R)
            sys_ts.append(sys_t)
        
        # from each system R(t) solve for the ship R(t)
        sys_R_ts = np.vstack(sys_R_ts)
        sys_ts = np.vstack(sys_ts)
        self.R_t, self.t, self.failing_sys = calc.determine_R_t_from_multiple_r_ts(sys_R_ts, sys_ts) 
       
        # create a ship R_t plot from the individual system R(ts)
        if figure_dict != None:
            plotter.plot_ship_R_t(self, figure_dict, save_folder)
            
        
            
            

              
        # vessel reliability determined by the system with the lowest R_t at all possible times
        
        
    #def determine_specific_failure():
    
    # grab one of the randomly simulated failure times
    
        
    
    
    ## COST FUNCTION CONSIDERATIONS
    # USNS Apichociola
    # 4 engines and 4 reduction gears
    