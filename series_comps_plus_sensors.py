from Model.model_series_component import Series_Component
from Model.model_sensor import Sensor


import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# Parts Plus Sensor Demo
# a small program that demostrates the sensors ability to sense the state of a component

# create n number of series components
n = 2
series_comps = []
sensors = []
for i in range(n):
    series_comps.append(Series_Component(100, 100, 200, i+1))
    sensors.append(Sensor(series_comps[i]))                 # create a sensor for each component

# detect the state of the components "over time"
num_readings = 100
sensor_readings = np.empty((n, num_readings))                         # create a matrix to store sensor readings

# save sensed the state of the components to matrix
for i in range(num_readings):
    for j in range(n):
        sensor_readings[j, i] = sensors[j].sense()

# plot the sensed state of the components over time
for i in range(n):
    plt.plot(sensor_readings[i], 'd:', label = series_comps[i].obj_name )
plt.title("Sensor Readings of Components Over Time")
plt.xlabel("Time")
plt.ylabel("Sensor Reading")
plt.legend()
plt.show()





