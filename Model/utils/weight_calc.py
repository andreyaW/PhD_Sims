import numpy as np

# weight parameters for each component 
W_LP_pump = 55.0            # kg (https://www.ato.com/1-hp-horizontal-centrifugal-pump?affiliate=shopping&gad_source=1&gclid=CjwKCAiAt5euBhB9EiwAdkXWOxLSXW1dHLCRQswJSufp8niP8M4CEFeODMCBnU-wAbRzb0pc7NyF0RoCExEQAvD_BwE) 
W_HP_pump = 127.00          # kg (https://alternativefuelmecca.com/product/industrial-oil-transfer-pump-60gpm/?gad_source=1&gclid=CjwKCAiAt5euBhB9EiwAdkXWO8e-ZLsdDAN6t0VqNzGfhFezQqUAbbCEt4vHupAkF7oXjqAUjCz89xoCQPgQAvD_BwE)
W_heat_exchanger = 26.3     # kg (https://shop.cummins.com/SC/product/cummins-heat-exchanger-5289417/01t4N0000048hw0QAA)
W_valve = 0.57              # kg (https://shop.cummins.com/SC/product/cummins-fuel-shutoff-valve-4069998/01t4N0000048fZmQAI)
W_cross_tie_valve = 0.68    # kg (https://shop.cummins.com/SC/product/cummins-valve-cover-3976175/01t4N0000048f2zQAA)

f_cross_tie_to_HP_pump = W_cross_tie_valve/W_HP_pump
f_valve_to_HP_pump=  W_valve / W_HP_pump
f_HE_to_HP_pump=  W_heat_exchanger / W_HP_pump
f_LP_to_HP_pump= W_LP_pump / W_HP_pump

factors= [f_cross_tie_to_HP_pump, f_valve_to_HP_pump, f_HE_to_HP_pump, f_LP_to_HP_pump]

# -------------------------------------------------------------------------------------------------------

# initial_weight = 0.05 * (27.3) # tons
initial_weight = 0.05 * (550) # tons
# initial_weight = 0.05 * (27.3*1000) # kgs
# initial_weight = 0.05 * (550*1000) # kgs

print("initial system weight is :" ,  initial_weight, '\n')


# solving for fuel oil + cooling comp weights
    # contains valves, LP pumps and HP pumps (cross ties added in latter configurations)
    # cooling_parts = [1, 3, 1]   # 1 LP pump, 3 valves, 1 HE

    
part_count = np.array([8, 2, 1, 1])
factors= np.array([f_valve_to_HP_pump, f_LP_to_HP_pump, f_HE_to_HP_pump,1])

# solve for largest part weight then use this to distribute the total weights
HP_pump_solved_W = initial_weight / sum( part_count * factors)
all_total_weights = HP_pump_solved_W * ( part_count * factors)
all_idv_weights = all_total_weights /part_count

# determine what percent of initial weight is attributed to each part (total count of parts)
percentages = ((all_idv_weights*part_count)/initial_weight) *100

# sanity check
# print(initial_weight - sum(all_total_weights))        # should equal zero

# print((all_idv_weights*part_count)/initial_weight)
# print(percentages)
# print(all_idv_weights)

# -------------------------------------------------------------------------------------------------------
# # printing all weights

print(f'LP Pump weight is: {all_idv_weights[1]:.2f} tons. \n', f'The {part_count[1]} LP Pumps make-up {percentages[1]:.2f}% total aux systems weight. \n \n' )
print(f'HP Pump weight is: {all_idv_weights[3]:.2f} tons. \n', f'The {part_count[3]} HP Pumps make-up {percentages[3]:.2f}% total aux systems weight.\n \n')
print(f'Heat Exchanger weight is: {all_idv_weights[2]:.2f} tons \n', f'The {part_count[2]} Heat exchanger make-up {percentages[2]:.2f}% total aux systems weight.\n \n')
print(f'valve weight is: {all_idv_weights[0]:.2f} tons. \n' , f'The {part_count[0]} valves make-up {percentages[0]:.2f}% total aux systems weight. \n \n' )
print(f'cross tie valve weight is: {HP_pump_solved_W * f_cross_tie_to_HP_pump:.2f} tons \n', 'Cross ties are not included in initial system weight.\n \n')

print('final system weight is', sum(all_idv_weights * part_count))

# -------------------------------------------------------------------------------------------------------
# fuel oil system 
fuel_total_weight = all_idv_weights[1]*1 + all_idv_weights[3]*1 + all_idv_weights[0]*5 
fuel_percentages = fuel_total_weight / all_idv_weights

print(f'final system weight is {fuel_total_weight:.2f} \n')
# print(f'LP Pump weight is: {fuel_percentages[1]:.2f}% total fuel system weight. \n ' )
# print(f'HP Pump weight is: {fuel_percentages[3]:.2f} % total fuel system weight.\n ')
# print(f'valve weight is: {fuel_percentages[0]:.2f} % total fuel system weight. \n ' )

# -------------------------------------------------------------------------------------------------------
# # cooling system 
cooling_total_weight = all_idv_weights[1]*1 + all_idv_weights[2]*1 + all_idv_weights[0]*4 
cooling_percentages = cooling_total_weight / all_idv_weights

print(f'final system weight is {cooling_total_weight:.2f} \n')

print('total_weight: ', fuel_total_weight +cooling_total_weight)



