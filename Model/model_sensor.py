import numpy as np

class Sensor: 
    ''' A sensor model based on Partially Observable Markov Decision Processes (POMDP) for a series component'''



    def __init__(self, connected_component, ):
        '''
        Params:
            connected_component (Series_Component or Parallel_Component) :
                the component that the sensor is connected to
            
        Returns:
            sensor_reading:
                the sensed state of the connected component
        '''

        # Sensor Parameters
        self.connected_component = connected_component      # the component that the sensor is connected to
        self.sensor_reading = None                          # the sensed state of the connected component

        self.states = [0, 1]                                # the possible states of the sensor [0 = failed, 1 = working]
        # self.transition_matrix = [[1., 0.], [0.1, 0.9]]     # the transition matrix of the sensor 
        self.transition_matrix = [[0.5, 0.5], [0.5, 0.5]]   # the transition matrix of the sensor 

        self.current_state = 1                              # the initial state of the sensor is working [1]


    def sense(self):
        ''' Returns the state of the connected component
        Params:
            None
        Returns:
            sensor_reading:
                the sensed state of the connected component
        '''
        
        # update the sensors state before detecting the reading 
        self.current_state = np.random.choice(self.states, p=self.transition_matrix[self.current_state]) #***

        # go to component and determine it's current state of health
        self.sensor_reading = self.connected_component.report_state()

        # update the sensors state and the detected reading to get the sensed state of the component
        return self.sensor_reading * self.current_state



    # def update_sensor_state(self):