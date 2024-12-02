from comp import comp
from sensor import sensor
# from markovChain import markovChain
from artistFunctions import drawGraphs as artist

import numpy as np

class sensedComp:
    def __init__(self, comp=comp(), sensors_list=[sensor(0.98) for _ in range(3)]):
        self.comp = comp
        self.sensors = sensors_list

        # set up the sensed component as a partially observed markov chain
        self.definePOMPModel()

    # ---------------------------------------------------------------------
    def definePOMPModel(self):
        "define the component and sensor pair as a partially observed markov process"

        self.definePossibleStates()
        # self.checkSensors()             # function to aggregate the sensed state to a single state and prob
        # self.setInitialState()

    # ---------------------------------------------------------------------
    def definePossibleStates(self):
        
        # define the state space of the sensed component based on the comp and sensors state spaces
        state_space = {}
        comp_state_names = list(self.comp.markov_model.state_space.values())
        sensor_state_names = list(self.sensors[0].markov_model.state_space.values())

        for i, comp_state in enumerate(comp_state_names):
            for j, sensor_state in enumerate(sensor_state_names):
                new_state_name = f"comp {comp_state} sensors {sensor_state}"  # define state indices
                new_state_idx = (i,j)                                         # define state names
                state_space[new_state_idx] = new_state_name
        
        self.state_space = state_space


    def checkSensors(self):
        '''
            Check the states of the sensors and return the majority state and the probabilities of each state
        '''
        sensor_states = [sensor.state for sensor in self.sensors]
        comp_state_probs = self.comp.state_prob

        print(sensor_states)
        print(comp_state_probs)

    def setInitialState(self):
        sensor_state, sensor_probs = self.checkSensors()
        comp_state = self.comp.state

        self.state = comp_state * len(sensor_probs) + sensor_state
        self.state_name = self.markov_model.stateIdx2Name(self.state)
        self.state_prob = self.comp.state_prob * sensor_probs[sensor_state]

    def draw(self):
        # artist.drawStateSpace(self.markov_model)
        # artist.plotMarkovChainHistory(self.markov_model)
        artist.drawSensingHistory(self)

    def updateState(self, num_steps):
        '''
            Update the state of the sensed component based on the sensor and component states
        '''
        i=0
        while i != num_steps:
            self.comp.updateState(1)
            for sensor in self.sensors:
                sensor.updateState(1)
                sensor.senseState(self.comp)
            i+=1
'''


    def createTransitionMatrix(self):
        num_states = len(self.state_space)
        transition_matrix = np.zeros((num_states, num_states))

        num_comp_states = len(self.comp.markov_model.state_space)
        num_sensor_states = len(self.sensors[0].markov_model.state_space)

        for i in range(num_comp_states):
            for j in range(num_sensor_states):
                current_idx = i * num_sensor_states + j
                for k in range(num_comp_states):
                    for l in range(num_sensor_states):
                        new_idx = k * num_sensor_states + l
                        transition_matrix[current_idx, new_idx] = (
                            self.comp.markov_model.transition_matrix[i, k]
                            * self.sensors[0].markov_model.transition_matrix[j, l]
                        )

        self.transition_matrix = transition_matrix

    def checkSensors(self):
        sensor_states = [sensor.state for sensor in self.sensors]
        counts = {state: sensor_states.count(state) for state in set(sensor_states)}

        majority_state = max(counts, key=counts.get)
        sensor_probs = np.zeros(len(self.sensors[0].markov_model.state_space))
        for state, count in counts.items():
            sensor_probs[state] = count / len(sensor_states)

        return majority_state, sensor_probs

    def setInitialState(self):
        sensor_state, sensor_probs = self.checkSensors()
        comp_state = self.comp.state

        self.state = comp_state * len(sensor_probs) + sensor_state
        self.state_name = self.markov_model.stateIdx2Name(self.state)
        self.state_prob = self.comp.state_prob * sensor_probs[sensor_state]

    def updateState(self, num_days):
        for _ in range(num_days):
            for sensor in self.sensors:
                sensor.updateState(1)
            self.comp.updateState(1)

            sensor_state, sensor_probs = self.checkSensors()
            comp_state = self.comp.state
            current_state_idx = comp_state * len(sensor_probs) + sensor_state
            next_state_probs = self.transition_matrix[current_state_idx]
            next_state_idx = np.random.choice(
                range(len(next_state_probs)), p=next_state_probs
            )
            
            # save important attributes to self                        
            self.state = next_state_idx
            self.state_name = self.markov_model.stateIdx2Name(self.state)
            self.state_prob= self.state_prob * next_state_probs

'''
# ---------------------------------------------------------------------
