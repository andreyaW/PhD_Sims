from comp import *
from sensor import *
from sensed_comp import *

import pandas as pd
import numpy as np


num_test_comps = 10
with pd.ExcelWriter('Prop_Sims/results.xlsx', engine='xlsxwriter') as writer:
    
    for i in range(num_test_comps):

        # setup a test sensed component
        comp1 = comp()
        num_sensors = 1
        test_comp = sensed_comp(comp1, num_sensors)

        # check sensed states over a time array
        time_vec = np.linspace(0, 100, 101)
        sensed_comp_result = []
        for t in time_vec:
            sensed_comp_result.append(test_comp.forecast_state(1))
        results = pd.DataFrame({'time' : time_vec, 'results': sensed_comp_result })  

        # Write each DataFrame to a different worksheet
        sheet_name = "Comp #"+str(i+1)
        results.to_excel(writer, sheet_name=sheet_name, index=False) # Now 'multiple_sheets.xlsx' will have 3 sheets: 'People', 'Products', and 'Countries'

