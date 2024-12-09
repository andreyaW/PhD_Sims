import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.patches import Ellipse
from graphviz import Digraph




# Markov Chain Functions
# ----------------------------------------------------------------------------------------------
def wrapLabel(label, max_length=9):
    """
    Splits a label into multiple lines if it exceeds max_length.
    """
    if len(label) <= max_length:
        return label
    wrapped_label = ""
    for i in range(0, len(label), max_length):
        wrapped_label += label[i:i + max_length] + "\n"
    return wrapped_label.strip()

def addNodes(dot, state_names, pos):
    """
    Adds nodes to the Graphviz Digraph with specified attributes and positions.
    """

    # print('the pos is : ' , pos)
    # print('the state_names is : ' , state_names)
    # print(type(dot))
    
    fixed_distance = 2.5  # Fixed distance between nodes (width)
    fixed_distance_y = 5  # Fixed distance between nodes (height)
    updated_poses = {}

    for i, state in enumerate(state_names):
        label = wrapLabel(state)
        new_pos = (0,0)

        # Failure node below others
        if state == state_names[-1]:  
            if isinstance(pos[0], tuple):
                print('here 1')
                new_pos = (pos[i][0] * fixed_distance, -15)
            else:
                new_pos = (pos[i] * fixed_distance, -15)
        
        # Other nodes in a horizontal line
        else:  
            if isinstance(pos[0], tuple):
                new_pos = (pos[i][0] * fixed_distance, pos[i][1])
            else:
                new_pos = (pos[i] * fixed_distance, 0)
        
        dot.node(state, pos=f"{new_pos[0]},{new_pos[1]}!"  , label=label, shape='circle', style='filled', fillcolor='white')

    return dot

def addEdges(dot, states, transition_matrix):
    """
    Adds edges to the Graphviz Digraph with specified attributes.
    """
    for i, state_i in enumerate(states):
        for j, state_j in enumerate(states):
            transition_prob = transition_matrix[i][j]
            if transition_prob > 0:
                label = str(round(transition_prob, 2))
                dot.edge(state_i, state_j, label=label)

def drawMarkovChain(mC):
    """
    Draws a Markov Chain using Graphviz.
    """
    # Grab necessary values from the Markov Chain object
    state_numbers = list(mC.state_space.values())
    state_names = list(mC.state_space.keys())

    # Create a Graphviz Digraph
    dot = Digraph(format='png', engine='dot')
    dot.attr(rankdir='LR', nodesep='0.5', ranksep='0.5')

    # Add nodes and edges
    dot= addNodes(dot, state_names, state_numbers)
    addEdges(dot, state_names, mC.transition_matrix)

    # Render the graph
    dot.render('markov_chain', cleanup=True)  # Generates markov_chain.png and removes intermediate files

    # Display the rendered graph
    plt.figure(figsize=(10, 10))
    plt.imshow(plt.imread('markov_chain.png'))
    plt.axis('off')
    plt.show()

    # # Display the rendered graph
    # from IPython.display import Image
    # return Image(filename='markov_chain.png')

def plotMarkovChainHistory(mC)->None:
    """
    A function to plot the history of the Markov Chain

    :param mC: MarkovChain object
    """
    plt.figure(figsize=(5,5))
    plt.plot(mC.history)
    plt.ylabel('State')
    plt.xlabel('Time')
    plt.title(f'{mC.name} Markov Chain History')
    plt.gca().invert_yaxis()
    # plt.xticks(0, len(mC.history))
    plt.yticks(range(len(mC.state_space)))
    plt.savefig("./markovChainHistoryPlot_"+ mC.name.upper(), bbox_inches='tight')
#----------------------------------------------------------------------------------------------



# Sensed Component Functions
# ----------------------------------------------------------------------------------------------

def drawSensedHistory(sensed_comp, steps):
    steps = np.arange(steps)
    component_state_sequence = np.array(sensed_comp.comp.markov_model.history)
    sensor_observation_sequence = [np.array(sensor.sensed_history) for sensor in sensed_comp.sensors]
    sensor_health_sequence = [np.array(sensor.markov_model.history) for sensor in sensed_comp.sensors]

    # print(sensor_health_sequence)

    #PRINTING THE COMPONENT STATE AND SENSOR OBSERVATION SEQUENCE TO EXCEL for post analysis 
    df = pd.DataFrame(component_state_sequence)
    df.to_excel("Component_State_Sequence.xlsx")
    df = pd.DataFrame(sensor_observation_sequence)
    df.to_excel("Sensor_Observation_Sequence.xlsx")

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot the component state as a stepped line
    plt.plot(
        steps,
        component_state_sequence,
        label="Component State \n (0=Normal, 1=Degraded, 2=Failed)",
        drawstyle="steps-post",
        color="black",
        linewidth=2,
        alpha=0.8,
        linestyle="-",
    )

    # Plot the sensor observations based on the health of the sensors over time
    colors = ["green", "red", "blue"]
    for i, sensor in enumerate(sensed_comp.sensors):

        # filter out the healthy sensor readings from the sensors sensed history
        mask = sensor_health_sequence[i] == 0
        healthy_readings = sensor_observation_sequence[i][mask]
        healthy_steps = steps[mask]
        plt.plot(
            healthy_steps,
            healthy_readings,
            '.', 
            color= colors[i],
            alpha=0.6,
            markersize=6,
            label = "Sensor " + str(i) + " Healthy Readings"
        )


        # filter out the failed sensor readings from the sensors sensed history
        mask = sensor_health_sequence[i] == 1
        failed_readings = sensor_observation_sequence[i][mask]
        failed_steps = steps[mask]
        plt.plot(
            failed_steps,
            failed_readings,
            '--',
            color= colors[i],
            alpha=0.6,
            linewidth=2 
            )

        # plot the intial sensor failure as a X
        if len(failed_steps) > 0:
            plt.plot(
                failed_steps[0],
                failed_readings[0],
                'X',
                color= colors[i],
                alpha=0.6,
                markersize=14,
                label = "Sensor " + str(i) + " Initial Sensor Failure"
                )
        
    # arrange the graph to always show all possible component states
    comp_state_space = sensed_comp.comp.markov_model.state_space
    plt.yticks(range(len(comp_state_space)), labels=["Normal", "Degraded", "Failed"])

    # Add labels, title, legend, and grid
    plt.xlabel("Time Step")
    plt.ylabel("State")
    plt.title("Simulation of Component States and Sensor Observations")
    plt.gca().invert_yaxis()
    plt.legend()
    plt.grid()

    # Display the plot
    plt.show()

# ----------------------------------------------------------------------------------------------



def drawStateSpace(mC):
    """
        Draws the state space of the Markov Chain Model
    """

    # grab necessary values from the Markov Chain object
    state_numbers = list(mC.state_space.values())
    state_names = list(mC.state_space.keys())

    # Create and draw circle graph
    plt.figure(figsize=(10, 3))

    for i, state in enumerate(state_names):

        ellipse = Ellipse((0, 0), width=0.75+0.2*i, height=1+2*i, color='black', fill=False)
        plt.text(0, i, state, fontsize=8, ha='center')
        
        #plt.gca().add_artist(plt.Circle((0, .045), radius=0.2+0.3*i, color='black', fill=False))
        plt.gca().add_artist(ellipse)

    plt.axis('off')
    plt.title(f'{mC.name.upper()} State Space')
    plt.xlim(-1, 1)
    plt.ylim(-len(state_names)+.5, len(state_names)-.5)
    plt.show()