from shipModel.comp import comp
from shipModel.sensor import sensor
from artistFunctions import drawGraphs as artist

import numpy as np

class sensedComp:
    def __init__(self, comp=comp(), sensors_list=[sensor(0.98) for _ in range(3)]):
        self.comp = comp
        self.sensors = sensors_list
        self.history = []
        self.sensed_history = []
        # self.state = self.determineSensedState()    # set initial state of the sensed component

# ---------------------------------------------------------------------

    def grabCurrentStates(self):
        '''check the state of the component and sensors'''
        comp_state = self.comp.state
        sensor_states = [sensor.state for sensor in self.sensors]
        return comp_state, sensor_states

# ---------------------------------------------------------------------
    def updateState(self, num_steps):
        '''simulate the component and sensors for a number of steps'''

        for _ in range(num_steps):
            self.comp.updateState(1)
            for sensor in self.sensors:
                sensor.updateState(1)
                sensor.senseState(self.comp)    # sensors must update themselves and get a reading from the comp
            self.determineSensedState()

        artist.drawSensorAndCompHistory(self, num_steps)
        artist.drawSensedCompHistory(self, num_steps)
        self.reset()

# ---------------------------------------------------------------------
    def reset(self):
        '''reset the component and sensors to initial states'''
        self.comp.reset()
        for sensor in self.sensors:
            sensor.reset()
        self.history = []
        self.sensed_history = []

# ---------------------------------------------------------------------
    def determineSensedState(self):
        '''determine from the last sensed states the assumed state of the sensed component'''
        comp_state, sensor_states = self.grabCurrentStates()
        num_sensor = len(sensor_states)

        # determine the mode of the sensor states
        majority_sensor_state = max(set(sensor_states), key=sensor_states.count)
        
        # true state of the component is the mode of the sensor states and the true component state
        self.true_state = (comp_state, majority_sensor_state)
        self.history.append(self.true_state)

        # if all or majority of sensors are working, then you get the correct sensed state
        if majority_sensor_state == 0:
            self.state = self.true_state
        
        # else, the sensed state is the mode of the last sensed states
        else:
            last_sensed_states = [self.sensors[i].last_sensed_state for i in range(num_sensor)]
            majority_comp_sensed_state = max(set(last_sensed_states), key=last_sensed_states.count)
            self.state = (majority_comp_sensed_state, majority_sensor_state)
        self.sensed_history.append(self.state)

        return self.state

# ---------------------------------------------------------------------

    # def determineSensedState(self):
    #     '''determine from the last sensed states the assumed state of the sensed component'''
    #     comp_state, sensor_states = self.grabCurrentStates()
    #     num_sensor = len(sensor_states)

    #     # if all or majority of sensors are working, then you get the correct sensed state
    #     if sensor_states.count(0) >= num_sensor/2:
    #         self.state = (comp_state, 0)
       
    #     # if some sensors have failed, use the last sensed states to determine the predicted the component is in
    #     else:
    #         last_sensed_states = [self.sensors[i].last_sensed_state for i in range(num_sensor)]
    #         majority_state = max(set(last_sensed_states), key=last_sensed_states.count)
    #         self.state = (majority_state, 1)
    #         self.true_state = (comp_state, 1)

    #     self.history.append(self.state)
    #     return self.state
        
# ---------------------------------------------------------------------
    def likelihood(self):
        '''calculate the likelihood of the sensor readings given the true state of the component'''
        
        # get the true state of the component and the sensor readings
        comp_state, sensor_states = self.checkStates()
        print(comp_state, sensor_states)
        

        # get the state probabilities of all possible states
        comp_state_probs = self.comp.state_prob
        sensor_state_probs = [sensor.state_prob for sensor in self.sensors]

        print(comp_state_probs)
        for sensor_state_prob in sensor_state_probs:
            print("Sensor state probs: ", sensor_state_prob)


        # # calculate the likelihood of the sensor readings given the true state of the component
        # likelihood = 1
        # for sensor_state in sensor_states:
        #     likelihood *= self.sensors[sensor_state].state_prob[comp_state]
        # print (likelihood)





# ---------------------------------------------------------------------
def main():        
        # Create an instance of the component
        c1 = comp()
        
        # Create an instance of the sensor
        s1 = sensor()
        
        # Create an instance of the sensed component
        sc1 = sensedComp(c1, [s1 for _ in range(3)])
        
        # Print initial state
        print(f"Initial state: {sc1.comp.state_name}")
        
        # Update state after 2 days
        sc1.updateState(2)
        
        # Print updated state
        print(f"State after 2 days: {sc1.comp.state_name}")
