from Prop_Sims.shipModel.comp import *
from Prop_Sims.shipModel.sensor import *
from Prop_Sims.shipModel.sensedComp import *
from helper_funcs import plotting as plotter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

name1= 'test result: good component [P_ij]'
transition_mat1 = np.array([[0.98, 0.01, 0.01],
                            [0.0, 0.98, 0.02],
                            [0.0, 0.0,  1.0]])

name2= 'test result: ok component [P_ij]'
transition_mat2 = np.array([[0.45, 0.45, 0.10],
                            [0.0, 0.90, 0.10],
                            [0.0, 0.0,  1.0]])

name3= 'test result: bad component [P_ij]'
transition_mat3 = np.array([[0.34, 0.33, 0.33],
                            [0.0, 0.5, 0.5],
                            [0.0, 0.0,  1.0]])

test_transitions = [transition_mat1 , transition_mat2, transition_mat3]
test_names = [name1, name2, name3]
figures = []

#for k in range(len(test_transitions)):
for k in range(1):

    num_test_comps = 1000
    count_working= np.array([])                                                 # *sanity check: first value should == num tested comps
    count_failed = np.array([])
    count_undetected = np.array([])

    # set up variables to check sensed states over time
    num_points= 10
    time_vec = np.linspace(0, 5, 100, endpoint=True)                            # input time array
    sensed_comp_states = [[] for i in range(len(time_vec))]                      
    test_count_working = np.zeros_like(time_vec)
    test_count_partial = np.zeros_like(time_vec)                                 
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
                    # test_count_failed[j] += 1 
                    pass                
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
                            'time' : time_vec,
                            'number of working comps' : test_count_working,
                            'number of partially working comps' : test_count_partial,
                            'number of failed comps' : test_count_failed,
                            'number of failed sensors' : test_count_undetected
                            })

    # plot an write the overall data to different sheets
    figures.append(plotter.plot_sensed_comps(results, test_names[k], 'bar'))
    figures.append(plotter.plot_sensed_comps(results,test_names[k],'line'))

sheet_name = "Test #"+ str(k+1)
idv_result.to_excel(writer, sheet_name=sheet_name, index=False) 

# show generated plot
plotter.plot_multiple_plots(figures)
plt.show()