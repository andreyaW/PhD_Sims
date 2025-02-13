from shipModel.markovChain import markovChain
import numpy as np

class sensor:

    ''' 
        a simple model of a sensor object 
        To run this file enter in terminal: python -i sensor.py    

    
        EXAMPLE:
        >>> s1 = sensor(0.98) 
        >>> s1.state
        'working'
        >>> s1.update_state(2)
        >>> s1.state
        'failed'
        >>> s1.state_num
        1

    '''

    def __init__(self, accuracy=0.98):
        '''
        Initialize a sensor object represented as a Markov Chain

        :params accuracy: float the probability of the sensor detecting state correctly
                                the default is a good sensor (high accuracy)
        '''
        self.name = "sensor"
        self.accuracy = accuracy   
        self.defineMarkovModel()

        self.sensed_history = []  # store the history of the sensor
        
# ---------------------------------------------------------------------
    def defineMarkovModel(self)-> None:
        '''
        Creates a model for self using a markov chain object
        '''

        # initialize the sensor as a 2 state markov sensor model
        num_states= 2
        transition_mat = np.array([[self.accuracy, (1.0 -self.accuracy)],
                                   [0.0  ,    1.0]])        # failed is absorbing state         # save important attributes to self 
        mC = markovChain(num_states, transition_mat)
        
        # update the name of the markov model to sensor
        mC.name = self.name                     

        # store necessary parameters of the markov model to self
        self.markov_model = mC
        self.state = mC.state
        self.state_prob = mC.state_prob
        self.state_name = mC.stateIdx2Name(mC.state)   
        
# ---------------------------------------------------------------------
    def updateState(self, num_days)-> None:
        '''
        Predicts the true state of self after a given number of days
        
        :param num_days: int number of days to predict ahead from current state
        '''

        # update the markov model
        mC = self.markov_model
        mC.updateState(num_days)

        # update the parameters of self to match the markov model
        self.state = mC.state
        self.state_prob = mC.state_prob
        self.state_name = mC.stateIdx2Name(mC.state)

# ---------------------------------------------------------------------
    def reset(self)->None:
        '''reset the component to its initial state'''
        self.markov_model.reset()
        self.sensed_history = []  # reset the history of the sensor

# ---------------------------------------------------------------------
    def senseState(self, comp):
        '''
        Determine if the sensor is still able to communicate with the component and update the sensed state accordingly
        '''
        if self.state == 0:
            self.last_sensed_state = comp.markov_model.history[-1] # sensor is in working state, and can detect changes in comp state
            self.sensed_history.append(self.last_sensed_state)
            return (self.last_sensed_state, 0)  
        else:
            self.sensed_history.append(self.last_sensed_state)
            return (self.last_sensed_state, 1)  # sensor has failed and gets no more updates from comp
        
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
def main():
    
    # Create an instance of the sensor
    s1 = sensor()

    # Print initial state
    print(f"Initial state: {s1.state_name}")

    # Update state after 2 days
    s1.updateState(2)

    # Print updated state
    print(f"State after 2 days: {s1.state_name}")

if __name__ == "__main__":
    main()