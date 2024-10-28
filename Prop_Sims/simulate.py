from comp import *
from sensor import *
from sensed_comp import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

num_test_comps = 50      
count_working= np.array([])           # sanity check: first value should == num tested comps
count_failed = np.array([])                                   
count_undetected = np.array([])                                           # number of test comps

# set up variables to check sensed states over time
time_vec = np.linspace(0, 100, 10)                          # input time array
sensed_comp_states = [[] for i in range(len(time_vec))]     # states are strings, cannot be np. arrays      
test_count_working = np.zeros_like(time_vec)                                
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
        
        for i,t in enumerate(time_vec):

            # forecast component state for 1 time step
            sensed_comp_states[i]=test_comp.forecast_state(1)

            # calculate parameters of interest to plot
            state_space = list(test_comp.state_space.values())
            working_state = state_space[0]
            failed_comp_state = state_space[-2]
            failed_sensor_state = state_space[-1]

            if test_comp.current_state == working_state:
                test_count_working[i] += 1 
            
            if test_comp.current_state == failed_comp_state:
                test_count_failed[i] += 1 
            
            if test_comp.current_state == failed_sensor_state:
                test_count_undetected[i] += 1

    # append test data to simulate results arrays
    sensed_comp_states = np.array(sensed_comp_states)
    results = pd.DataFrame({'time' : time_vec,
                            'current state': sensed_comp_states[:,0],
                            'current state number' : sensed_comp_states[:,1],
                            'probability of current state': sensed_comp_states[:,2], 
                            'number of working comps' : test_count_working,
                            'number of failed comps' : test_count_failed,
                            'number of failed sensors' : test_count_undetected
                            })
    
    # Write each DataFrame to a different worksheet for storage to Excel
    sheet_name = "Comp #"+str(i+1)
    results.to_excel(writer, sheet_name=sheet_name, index=False) # Now 'multiple_sheets.xlsx' will have 3 sheets: 'People', 'Products', and 'Countries'


    # set plot parameters
    barWidth = 10                         # width of bar 
    fig = plt.subplots(figsize =(12, 8))    # figure setup

    # Horizontal Bar Plot
    plt.bar(results['time'], results['number of working comps'], 
            color ='g', width = barWidth, edgecolor ='grey', label ='working components')
    plt.bar(results['time'], results['number of failed comps'], 
            color ='r', width = barWidth, edgecolor ='grey', label ='failed components')
    plt.bar(results['time'], results['number of failed sensors'], 
            color ='b', width = barWidth, edgecolor ='grey', label ='failed sensors')

    # Show Plot
    plt.legend()
    plt.show()


    # # plot simulation data
    # fig.plot(time_vec, results['number of working comps'], '*g', label = 'number working comps')
    # fig.plot(time_vec, results['number of failed comps'], '^r', label = 'number failed comps')
    # fig.plot(time_vec, results['number of failed sensors'], '.b', label = 'number failed sensors')

    # plt.legend()
    # plt.show()