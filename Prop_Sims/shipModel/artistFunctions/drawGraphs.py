import numpy as np
# import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.patches import Ellipse
from graphviz import Digraph

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

# ----------------------------------------------------------------------------------------------
def addNodes(dot, state_names, pos):
    """
    Adds nodes to the Graphviz Digraph with specified attributes and positions.
    """

    print('the pos is : ' , pos)
    print('the state_names is : ' , state_names)
    print(type(dot))
    
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
            print('here 2')
            if isinstance(pos[0], tuple):
                new_pos = (pos[i][0] * fixed_distance, pos[i][1])
            else:
                new_pos = (pos[i] * fixed_distance, 0)
        
        dot.node(state, pos=f"{new_pos[0]},{new_pos[1]}!"  , label=label, shape='circle', style='filled', fillcolor='white')

    return dot


'''
def addNodes(dot, state_names, pos):
    """
    Adds nodes to the Graphviz Digraph with specified attributes and positions.
    Ensures nodes at (0,0), (1,0), and (2,0) are aligned horizontally.
    """
    print('the pos is:', pos)
    print('the state_names is:', state_names)
    print(type(dot))
    
    fixed_distance = 2.5  # Fixed distance between nodes (width)
    fixed_distance_y = 5  # Fixed distance between nodes (height)
    updated_poses = {}

    for i, state in enumerate(state_names):
        label = wrapLabel(state)

        # Adjust positions for horizontal alignment of specific nodes
        if pos[i][1] == 0:  # Nodes at y=0
            new_pos = (pos[i][0] * fixed_distance, 0)  # Keep y=0
        else:  # Other nodes maintain their vertical positioning
            new_pos = (pos[i][0] * fixed_distance, -pos[i][1] * fixed_distance_y)

        updated_poses[state] = new_pos
        dot.node(
            state, 
            label=label, 
            shape='circle', 
            style='filled', 
            fillcolor='white',
            pos=f"{new_pos[0]},{new_pos[1]}!"  # Explicit positioning
        )

    return updated_poses
'''

# ----------------------------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------------------------
def drawSensingHistory(sensed_comp, steps):
    steps = np.arange(steps)
    component_state_sequence = sensed_comp.comp.markov_model.history[:]
    sensor_observation_sequence = [sensor.sensed_history for sensor in sensed_comp.sensors]

    # Assuming the following sequences are the simulation results:
    # `component_state_sequence` contains the component states (0=Normal, 1=Degraded, 2=Failed)
    # `sensor_observation_sequence` contains the sensed states of the sensors individually (0=Normal, 1=Degraded, 2=Failed)

    # Parameters for the plot
    # time_steps = np.arange(len(component_state_sequence))  # Time steps

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot the component state as a stepped line
    plt.plot(
        steps,
        component_state_sequence,
        label="Component State \n (0=Normal, 1=Degraded, 2=Failed)",
        drawstyle="steps-post",
        color="black",
        linewidth=5.0,
    )

    # plot working sensors and failed sensors differently
    for i, sensor in enumerate(sensed_comp.sensors):
        if sensor.state == 0:
            plt.plot(
                steps,
                sensor_observation_sequence[i], '--.g',
                alpha=0.6,
                label = 'sensor ' + str(i),
                linewidth=5,
            )
        else:
            plt.plot(
                steps,
                sensor_observation_sequence[i], '--.r',
                alpha=0.6,
                label= 'sensor ' + str(i),
                linewidth=5,
            )

    # Add labels, title, legend, and grid
    plt.xlabel("Time Step")
    plt.ylabel("State")
    plt.title("Simulation of Component States and Sensor Observations")
    plt.gca().invert_yaxis()
    plt.legend(loc= "lower left")
    plt.grid()

    # Display the plot
    plt.show()

    print([sensor.state for sensor in sensed_comp.sensors])
