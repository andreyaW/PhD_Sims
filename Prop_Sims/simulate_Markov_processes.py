import numpy as np
import matplotlib.pyplot as plt
from comp import comp

# initialize simulation parameters
num_comps = 2 
operational_hours = 2160

# initialize the time vector and test results vector
t = np.linspace(0, operational_hours, 11)       # time vector of 1000 points
all_tests_results = np.empty([3, num_comps])

# plot for the data
fig, ax = plt.subplots()

# create a plot of the MDP working for Z components over X hours (Y axis = working or failing)
for i in range(num_comps):

    # create a component object
    test_comp = comp()                          # initialize the component object

    test_results_headers = [["t"], ["prev. state"] , ["current state"]]
    test_results = [t, [], []]                  # list to store the test results

    # testing Markov Decision Process for the component model
    for i in range(len(t)):
        test_results[1].append(test_comp.state)
        test_results[2].append(test_comp.get_next_state())

    # add test data to the list and the plot
    ax.plot(t, test_results[2])
    test_results = np.array(test_results)

    # 


    # all_tests_results[i] = np.array(test_results[2])



# save the data to a page of an xlxs file
# test_results[0][:] = test_results_headers
# np.savetxt('Prop_Sims/test_results.xlsx', test_results, delimiter=',', fmt='%s')


# Show the plot
ax.invert_yaxis()           # Flip the y-axis (move "working" to the top)
plt.show() 

