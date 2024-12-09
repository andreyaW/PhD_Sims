from comp import comp
from sensor import sensor
from artistFunctions import drawGraphs as artist

import numpy as np

class sensedComp:
    def __init__(self, comp=comp(), sensors_list=[sensor(0.98) for _ in range(3)]):
        self.comp = comp
        self.sensors = sensors_list

# ---------------------------------------------------------------------

    def checkStates(self):
        '''check the state of the component and sensors'''
        comp_state = self.comp.state
        sensor_states = [sensor.state for sensor in self.sensors]
        return comp_state, sensor_states
    
    def determineSensedState(self):
        '''determine from the last sensed states the assumed state of the sensed component'''
        comp_state, sensor_states = self.checkStates()
        # print(comp_state, sensor_states)

    def reset(self):
        '''reset the component and sensors to their initial states'''
        self.comp.reset()
        for sensor in self.sensors:
            sensor.reset()

    def updateState(self, num_steps):
        '''simulate the component and sensors for a number of steps'''
        
        for _ in range(num_steps):
            self.comp.updateState(1)
            for sensor in self.sensors:
                sensor.updateState(1)
                sensor.senseState(self.comp)    # sensors must update themselves and get a reading from the comp
            self.determineSensedState()

        artist.drawSensedHistory(self, num_steps)
        self.reset()
        
# ---------------------------------------------------------------------