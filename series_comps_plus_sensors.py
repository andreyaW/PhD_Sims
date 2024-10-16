from Model.model_series_component import Series_Component
from Model.model_sensor import Sensor


import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------------------------------------------------------------------------------------ #
# Parts Plus Sensor Demo
# a small program that demostrates the sensors ability to sense the state of a component

# create n number of series components
n = 1
series_comps = []
sensors = []
for i in range(n):
    series_comps.append(Series_Component(100, 100, 200, i+1))   # create a series component
    series_comps[i].simulate()                                  # create a heatlh curve for the component
