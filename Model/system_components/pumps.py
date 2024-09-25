import numpy as np

# averaging the failures of each pump from (Knežević et al., 2022). 
pump_fail_rates = np.array([1.1844e-4, 6.7684e-5, 5.0763e-5, 6.7684e-5, 1.0152e-4, 8.4605e-5])
avg_fail_rate = np.mean(pump_fail_rates)
# print(avg_fail_rate)

# using the system failure rate (fails/hour) * millions of operating hours = # fails in million operating hours
# print(0.4907e-3*10**6)


# ----------------------------------------------------------------------------------------------------------
# finding MTTF

# pump 1
pump_1_f_t = np.array([1050, 8680, 16357, 31005, 46335, 51445, 54805])
pump_1_MTTF = np.mean(np.diff(pump_1_f_t))
print("pump 1 MTTF: ", pump_1_MTTF)

# pump 2
pump_2_f_t = np.array([5886, 8826, 40820, 48193])
pump_2_MTTF = np.mean(np.diff(pump_2_f_t))
print("pump 2 MTTF: ",pump_2_MTTF)

# pump 3
pump_3_f_t = np.array([6473, 46513, 48193])
pump_3_MTTF = np.mean(np.diff(pump_3_f_t))
print("pump 3 MTTF: ", pump_3_MTTF)

# pump 4
pump_4_f_t = np.array([13193, 45463, 48193, 54805])
pump_4_MTTF = np.mean(np.diff(pump_4_f_t))
print("pump 4 MTTF: ", pump_4_MTTF)

# pump 5
pump_5_f_t = np.array([10253, 27893, 28314, 41915, 45275, 46093])
pump_5_MTTF = np.mean(np.diff(pump_5_f_t))
print("pump 5 MTTF: ", pump_5_MTTF)

# pump 6
pump_6_f_t = np.array([5970, 11679, 38955, 42735, 48193])
pump_6_MTTF = np.mean(np.diff(pump_6_f_t))
print("pump 6 MTTF: ", pump_6_MTTF)

# average MTTF of all pumps 
pump_avg_MTTF= np.mean([pump_1_MTTF, pump_2_MTTF, pump_3_MTTF, pump_4_MTTF, pump_5_MTTF, pump_6_MTTF])
# pump_avg_MTTF= 29/ (avg_fail_rate)
print(pump_avg_MTTF)

pump_avg_MTTF = np.mean(np.diff(np.concatenate([pump_1_f_t, pump_2_f_t, pump_3_f_t, pump_4_f_t, pump_5_f_t, pump_6_f_t])))
print(pump_avg_MTTF)
