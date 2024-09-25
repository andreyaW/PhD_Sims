"""
simulation.py

Programming instruction create a test vessel then run and export results from 
the simulations of relaibility of various ship system configurations.


(C) 2023 Regents of the University of Michigan

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Created on Tues May 30 13:55:00 2023

@author: mdcoll, adware
 
Last Edited: Tues July 18 11:00 2023 by Andreya Ware (adware)
"""

# ------------------------------------------------------------------------------------------------------------------------------------------------ #

from matplotlib import pyplot as plt
from Model.model_vessel import vessel as model_vessel
from Model.utils.animation_functions import * 

import numpy as np
import os
import shutil
import seaborn as sns
sns.set_theme(style='whitegrid')

# ------------------------------------------------------------------------------------------------------------------------------------------------ #

class simulation:
    '''
    Class used to do calculations on the simulated vessels
    '''
    
    def __init__(self, num_Ships, num_Sys, num_Comps):        
        '''
        Initializes a ship and its systems and components. This calls also has built in functions 
        to run specific system or ship reliability tests

        Parameters
        --------------------------------------------------------------------
        1. num_Ships:   integer
                        number of random failure times to generate for the component's overall failure sample set

        2. num_Sys:     integer
                the number of model system objects to create in the model vessel
            
        3. num_Comps:   integer or list of integers
                        a single integer value or list of integer number of model components to be created in each model system. A single value will 
                        default to all systems having the same number of components.To have systems of varied number of components provided a integer 
                        number of componetns for each system. 
       
        Returns
        -------------------------------------------------------------------
        None
        '''
        
        # Simulation Parameters
        self.total_num_ships    = num_Ships    
        self.numberOfSystems    = num_Sys                   # integer assignment of the subsytem of the ship i.e System # "1"
        self.numberOfComps      = num_Comps                 # integer value or list of number of parts in each system i.e "(2, 3, 4)" or "3"
               
        # Function Call to initialize model vessel
        self.initialize_vessels(num_Ships, num_Sys, num_Comps)                                    # creating an initial vessel model to test 

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    
    
    
    def initialize_vessels(self, lifetimes, variances, component_names = ""):
        '''
        Defines a model vessel for the simulation run. 
            EX:  initialize_vessel(3,3)  --OR--  initialize_vessel(3,[1,4,3]) 

        Parameters
        --------------------------------------------------------------------
        1. n  : integer
                number of values to use to initialize in the components random 
                distribution of failure times
                
        2. num_Comps:   integer, list of integers
                        a single integer value or list of integer number of model components to be created in each model system. A single value will 
                        default to all systems having the same number of components.To have systems of varied number of components provided a integer 
                        number of componetns for each system. 
        
        3. num_Sys:     integer
                        the number of model system objects to create in the model vessel
            
                            
        Returns
        -------------------------------------------------------------------
        1. vessel: class for modelling vessels
           a machinery model for a simple USV
        '''
        
        num_Comps = self.numberOfComps
        num_Sys = self.numberOfSystems   
    
        self.vessel_model = model_vessel(num_Sys, num_Comps)         #ship_model 
        
        
        
    def define_comps(self, lifetimes= None, variances= None, comp_names = None ):
        '''
        Assigns all average liftimes (hours) and names to the appropriate component in each ship subsystem. 

        Parameters
        --------------------------------------------------------------------
        1. component_lifetimes: list of integers
            average time to failure of a component, measured in operational hours
            stored as a list of lists, seprated by system
                EX:     lifetimes= [(9944.0,   528.5,  528.5, 10149.0),
                                    (4104.0, 10149.0, 1122.5, 10690.0),
                                    (4305.0,  4305.0, 4305.0,  4305.0)]
                                                                       
        2. variance_scale: integer
            the scale/ amount of variance (randomness) to include in the spread of failure realizations
                           
        3.  component_names:    list of string
                            the name to be assigned to the component, displays in charts and on graphs, 
                            stored as a list of lists, seprated by system
                                EX:         componentNames= [ ( "LP Pump", "LP Filter" ,"LP Filter" , "LP Fuel Line"), 
                                                            ( "Fuel Meter" , "HP Fuel Line" , "HP Fuel Filter", "HP Fuel Pump" ),
                                                            ( "Injector Valve", "Injector Valve" , "Injector Valve", "Injector Valve")]
        
        Returns
        -------------------------------------------------------------------
        None    
        '''   
             
        num_samples= self.total_num_ships                   # default number of sample point to use per component model
        ship_model = self.vessel_model
        
        self.compNames = comp_names                         # save the names of the components being       
        
        # define systems within the model vessel with the provided parameters
        ship_model.define_systems(num_samples, lifetimes, variances, comp_names)
            


    def save_sim_R_t(self, save_folder):
        ship_model = self.vessel_model

        figure_dict= {}
        ship_model.compute_ship_R_t(figure_dict, save_folder)







  
    # def calculate_categorized_R_t(self, time_vector, save_folder):
                
    #     '''
    #         ---

    #     Parameters
    #     --------------------------------------------------------------------
    #     1. time_vector: integer/double array
    #         times for the system failure to be evaluated over
        
    #     2. save_folder: string directory 
    #         file directory location for generated average R_t curves to be saved to
        
    #     Returns
    #     -------------------------------------------------------------------
    #     Folder with .pdf graph files showing the failure of each system in a simulated ship         
    #     '''
    #     num_Sys = self.numberOfSystems 
    #     self.lookup_times= time_vector

    #     #delete the folder if it had been previously generated then save
    #     if os.path.exists(save_folder):
    #         shutil.rmtree(save_folder)
    #         os.makedirs(save_folder)

    

        # for i in range(num_Sys):             # sys_assignment= i    # system assignment/number
        #     # grab system object
        #     sys = self.vessel.shipSystems[i]               
        #     num_sim_ships = self.total_num_ships    

        #     # add a mask to highlight failures caused by parallel part
        #     fail_times, failure_cause_idx= self.check_ship_failure(num_sim_ships, save_folder, save_diagram=False) # turn of storing to folder
            
        #     failure_times , rel_curve = self.random_to_R_t(fail_times)
        #     self.solve_sim_R_t(time_vector)
            
        #     mask= (failure_cause_idx!=0)
        #     #print(mask.T[0])

        #     # arrange the failure times as a R_t curve after indexing the failures
            

        #     #plot system overall reliability as a dotted line (stored to last row of sys_rel)
        #     overall_rel_label= f'System {i+1} ' + '$R_{t}$'
        #     plt.plot(time_vector, rel_curve, label = "system R(t) Curve",
        #             linestyle='dashdot', linewidth=1.75, marker='', markersize=3, 
        #             color='black')
        #     plt.suptitle( overall_rel_label, fontsize= 10)

        #     plt.plot(time_vector, [mask.T[0]], label = "failure caused by parallel set",
        #             linestyle='', linewidth=1.75, marker='*', markersize=3, 
        #             color='red')
        #     plt.legend(fontsize= 6)

        #     #save file
        #     file_label= f'System {i+1} Categorized R_t.png'
        #     file_directory= os.path.join(save_folder, file_label)
        #     plt.savefig(file_directory)  

    def save_categorized_R_t(self, save_folder):
        ship_model = self.vessel_model





    # def check_ship_failure(self, num_realizations, save_folder, save_diagram = True, make_gif= False):
    #     
    #     Determine the Failure Time of the ship and each of its systems and components
    #     for a specific number of simulated vessels. 
        
    #     Parameters
    #     --------------------------------------------------------------------
    #     1. num_realizations: integer/double array
    #         number of ship failure realizations to determine failure times for 
            
    #     Returns
    #     -------------------------------------------------------------------
    #     failure times for each realization desired
        
        
    #     ship= self.vessel
    #     num_Sys = self.numberOfSystems
                    
    #     #determine all individual component, sys, and ship fail times             
    #     ship_fail_times = np.zeros((num_realizations)) 
    #     failure_cause = np.zeros((num_realizations, num_Sys))
    #     sys_fail_times = np.zeros((num_Sys))       

    #     for i in range(num_realizations): 
            
    #         if save_diagram :
    #                 #initialize a diagram to draw the system on
    #                 ship_diagram = animation_functions(i, num_Sys)
                    
    #         for j in range(num_Sys):
                
    #             # grab the system object, solve and store its failure times
    #             system= ship.shipSystems[j]
    #             system.determine_Sys_Failure_T(i)                         # for a sys, realized_fails= [comp1_f_t,comp2_f_t,... sys_f_t]      
    #             sys_fail_times[j]= system.f_t

    #             failure_cause_idx= system.failure_cause
                
    #             if save_diagram :
    #                 # Draw each system diagram    
    #                 ship_diagram.determine_times_N_colors(system)                    # function to determine fail times and component colors for plot
    #                 ship_diagram.draw_sys(system)            
    #                 ship_diagram.add_failure_times(system)                     
                    
    #                 #save file to newly created folder      
    #                 file_label= f'Ship {i+1} Failure Times.png'
    #                 file_directory= os.path.join(save_folder, file_label)
    #                 plt.savefig(file_directory) 
                    
    #             if make_gif :
    #                 # Create an anymation of the sytem functioning over a time vector    
    #                 ship_diagram.determine_times_N_colors(system,self.lookup_times)                    # function to determine fail times and component colors for plot
    #                 ship_diagram.draw_sys(system)            
    #                 ship_diagram.add_failure_times(system)                     

    #                 # save gif to a newly created folder      
    #                 file_label= f'Ship {i+1} Failure Animation.png'
    #                 file_directory= os.path.join(save_folder, file_label)                        
    #                 ship_diagram.create_failure_gif(system, file_directory)                    
                        
    #             plt.close()
    #             failure_cause[i][j] = failure_cause_idx
    #         ship_fail_times[i]= min(sys_fail_times)
           
    #     #return the failure times of all vessels simulated
    #     print(failure_cause)
    #     print(ship_fail_times)
    #     return ship_fail_times, failure_cause
                    
                    
    # '''         
                
                
    # def mission_success_check(self, save_folder=''):
        
        # num_sim_ships= self.total_num_ships
        
        #initialize  a vector for storing all failure times
        # simulated_fail_times = np.zeros((num_sim_ships,1))
        
        # mission_success= 0
        # mission_failure= 0
        
        # # for all simulated ships determine if they fail before completing the mission
        # fail_times, failure_cause_idx= self.check_ship_failure(num_sim_ships, save_folder, save_diagram=False) # turn of storing to folder

        # for time in fail_times:
        #     if time >= mission_length: 
        #         mission_success +=1
        #     else:
        #         mission_failure +=1
                
        # # save all simulated failure times to the simulation class        
        # self.fail_times= simulated_fail_times
        # print(self.fail_times)
        
        # # save the failure cause idx matrix to the simulation class
        # self.failure_cause_matrix = failure_cause_idx

        # # determine how many failures caused by each element
        # unique_causes = []
        # [unique_causes.append(x) for x in failure_cause_idx if x not in unique_causes]
        # categorized_fails = dict()

        # for unique_cause in unique_causes:
        #     count=0
            
        #     for failure_cause in failure_cause_idx:
        #         if failure_cause== unique_cause:
        #             count+=1
        #     unique_percent = count/num_sim_ships
        #     categorized_fails.update({ str(unique_cause) : unique_percent }) 
               
        # #return percentage of sucessful ships
        # overall_success = mission_success / num_sim_ships 
        # return overall_success, categorized_fails

