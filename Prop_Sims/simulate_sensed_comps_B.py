from comp import *
from sensor import *
from sensed_comp import *
from helper_funcs import plotting as plotter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

max_sensors = 10
test_transitions = [i+1 for i in range(max_sensors)]
test_names = [str(i+1) + 'Sensors Attached' for i in range(max_sensors)]

for k in range(len(test_transitions)):

    num_test_comps = 100
    count_working= np.array([])           # sanity check: first value should == num tested comps
    count_failed = np.array([])
    count_undetected = np.array([])

    # set up variables to check sensed states over time
    num_points= 10
    time_vec = np.linspace(0, 5, 10, endpoint=True)                          # input time array
    sensed_comp_states = [[] for i in range(len(time_vec))]     # states are strings, cannot be np. arrays      
    test_count_working = np.zeros_like(time_vec)                                
    test_count_failed = np.zeros_like(time_vec)  
    test_count_undetected = np.zeros_like(time_vec)  

    # for plotting and writing to Excel
    with pd.ExcelWriter('Prop_Sims/results.xlsx', engine='xlsxwriter') as writer:

        # Start Test Loop
        for i in range(num_test_comps):

            # create a test 'sensed component' object
            comp1 = comp(test_transitions[k])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            test_comp = sensed_comp(comp1, 1) # assumes one sensor to start
            
            for j,t in enumerate(time_vec):

                # forecast component state for 1 time step
                sensed_comp_states[j]=test_comp.forecast_state(1)

                # calculate parameters of interest to plot
                state_space = list(test_comp.state_space.values())
                working_state = state_space[0]
                partially_working_state = state_space[1]
                failed_comp_state = state_space[-2]
                failed_sensor_state = state_space[-1]

                if test_comp.current_state == working_state or test_comp.current_state == partially_working_state:
                    test_count_working[j] += 1 
                
                elif test_comp.current_state == failed_comp_state:
                    test_count_failed[j] += 1 
                
                elif test_comp.current_state == failed_sensor_state:
                    test_count_undetected[j] += 1
                else:
                    print("!!SOMETHING UNEXPECTED HAS OCCURRED!!")

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
                            'number of failed comps' : test_count_failed,
                            'number of failed sensors' : test_count_undetected
                            })

    # plot an write the overall data to different sheets
    plotter.plot_sensed_comps(results, test_names[k], 'bar')
    # plotter.plot_sensed_comps(results,'line')

sheet_name = "Test #"+ str(k+1)
idv_result.to_excel(writer, sheet_name=sheet_name, index=False) 

plt.show()