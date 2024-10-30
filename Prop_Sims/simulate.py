from comp import *
from sensor import *
from sensed_comp import *
from helper_funcs import plotting as plotter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

num_test_values = 2
for k in range(num_test_values):
    num_test_comps = 10
    count_working= np.array([])           # sanity check: first value should == num tested comps
    count_failed = np.array([])
    count_undetected = np.array([])

    # set up variables to check sensed states over time
    num_points= 50
    time_vec = np.linspace(0, 25000, num_points+1)                          # input time array
    sensed_comp_states = [[] for i in range(len(time_vec))]     # states are strings, cannot be np. arrays      
    test_count_working = np.zeros_like(time_vec)
    test_count_partial = np.zeros_like(time_vec)                                
    test_count_failed = np.zeros_like(time_vec)  
    test_count_undetected = np.zeros_like(time_vec)  

    # for plotting and writing to Excel
    with pd.ExcelWriter('Prop_Sims/results.xlsx', engine='xlsxwriter') as writer:

        # Start Test Loop
        for i in range(num_test_comps):

            # create a test 'sensed component' object
            comp1 = comp()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            num_sensors = 1
            test_comp = sensed_comp(comp1, num_sensors)
            
            for j,t in enumerate(time_vec):

                # forecast component state for 1 time step
                sensed_comp_states[j]=test_comp.forecast_state(1)

                # calculate parameters of interest to plot
                state_space = list(test_comp.state_space.values())
                working_state = state_space[0]
                failed_comp_state = state_space[-2]
                failed_sensor_state = state_space[-1]

                if test_comp.current_state == working_state:
                    test_count_working[j] += 1 
                
                elif test_comp.current_state == failed_comp_state:
                    test_count_failed[j] += 1 
                
                elif test_comp.current_state == failed_sensor_state:
                    test_count_undetected[j] += 1
                else:
                    test_count_partial[j] +=1
                    
            # append test data to simulate results arrays
            sensed_comp_states = np.array(sensed_comp_states)
            
            # save results of a single comp test
            idv_result = pd.DataFrame({'time' : time_vec,
                                    'current state': sensed_comp_states[:,0],
                                    'current state number' : sensed_comp_states[:,1],
                                    'probability of current state': sensed_comp_states[:,2] 
                                    })
            
            # Write each individual test DataFrame to a different worksheet for storage to Excel
            sheet_name = "Comp #"+str(i+1)
            idv_result.to_excel(writer, sheet_name=sheet_name, index=False) 

    results = pd.DataFrame({
                            'number of working comps' : test_count_working,
                            'number of partially working comps' : test_count_partial,
                            'number of failed comps' : test_count_failed,
                            'number of failed sensors' : test_count_undetected
                            })

    # plot an write the overall data to different sheets
    plotter.plot_sensed_comps(results,'bar')
    # plotter.plot_sensed_comps(results,'line')

sheet_name = "Test #"+ str(k+1)
idv_result.to_excel(writer, sheet_name=sheet_name, index=False) 

plt.show()