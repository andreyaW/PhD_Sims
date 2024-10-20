import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from comp import comp

# initialize simulation parameters
num_comps = 100 
operational_hours = 2160

# initialize the time vector and test results vector
t = np.linspace(0, operational_hours, 11)       # time vector of 1000 points
all_comp_results = pd.DataFrame({'time' : t})  
# fig, ax = plt.subplot()

for i in range(num_comps):

    # create a component object 
    test_comp = comp(2)
    
    # first save a single component to a excel page
    comp_results = pd.DataFrame(columns= ['time', 'previous state', 'current state'])   # pd.DataFrame({'time' : t})  

    # generate the component states over time
    current_states = []
    prev_states = []
    for times in t:        
        prev_states.append(test_comp.state)
        current_states.append(test_comp.get_next_state())

    # save single test component data 
    comp_results['time'] = t
    comp_results['previous state'] = prev_states
    comp_results['current state'] = current_states

    # save and plot single test data to larger dataset
    all_comp_results.loc[:,(i+1)] = current_states
    plt.plot(t, current_states)

# Save data to excel file using a Pandas Excel writer object and XlsxWriter as the engine
with pd.ExcelWriter('Prop_Sims/results.xlsx', engine='xlsxwriter') as writer:
    test_name = "Results " + str(num_comps) + " 2-State Components"
    all_comp_results.to_excel(writer, sheet_name=test_name, index=False) # Now 'multiple_sheets.xlsx' will have 3 sheets: 'People', 'Products', and 'Countries'
       
    # ************ PRINTING EACH RESULT TO A PAGE IS NOT WORKING YET 
    # comp_name = 'Comp #' + str(i+1)
    # with pd.ExcelWriter('Prop_Sims/each_comp_result.xlsx', engine='xlsxwriter') as writer:
    #     # Write each DataFrame to a different worksheet
    #     comp_results.to_excel(writer, sheet_name=comp_name, index=False) # Now 'multiple_sheets.xlsx' will have 3 sheets: 'People', 'Products', and 'Countries'

# Show the plot
plt.invert_yaxis()           # Flip the y-axis (move "working" to the top)
plt.show() 
