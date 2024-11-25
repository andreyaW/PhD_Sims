import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------
def wrap_label(label, max_length=9):
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
def add_nodes(G, pos, state_names):
    """
    Adds the nodes of the graph with specified attributes.
    """
    fixed_distance = 2.5  # Fixed distance between nodes
    updated_poses = {}

    # Add states (nodes) to the graph
    for i, state in enumerate(state_names):
        G.add_node(state, label = wrap_label(state))  # Add nodes with wrapped labels
    
        # Position the nodes (failure node below all others)
        if state == state_names[-1]:
            if type(pos[0]) == tuple :
                new_pos = (pos[i][0]*fixed_distance, pos[i][1] -10)  # for two level horizontal graph (sensed comp)
                updated_poses.update({state:new_pos})  
            elif type(pos[0]) == int:
                new_pose = (pos[i]*fixed_distance, -10) # for horizontal graph (comp or sensor only)
                updated_poses.update({state:new_pose}) 
        
        elif type(pos[0]) == tuple :
            new_pos = (pos[i][0]*fixed_distance, pos[i][1])  # for two level horizontal graph (sensed comp)
            updated_poses.update({state:new_pos})  
        elif type(pos[0]) == int:
            new_pose = (pos[i]*fixed_distance, 0) # for horizontal graph (comp or sensor only)
            updated_poses.update({state:new_pose}) 
    
    pos = updated_poses
    return pos


# ----------------------------------------------------------------------------------------------
def add_edges(G, states, transition_matrix):
    """
    Adds the edges of the graph with specified attributes.
    """    
    # Add edges to the graph
    for i,state_i in enumerate(states):

        for j, state_j in enumerate(states):

            transition_prob = transition_matrix[i][j]
            if transition_prob > 0:
                G.add_edge(state_i, state_j, weight=transition_prob, label=round(transition_prob, 2), connectionstyle='arc3,rad=-5') 
               
# ----------------------------------------------------------------------------------------------
def drawMarkovChain(mC)->None:
    # grab necessary values from the Markov Chain object
    state_numbers = list(mC.state_space.values())
    state_names = list(mC.state_space.keys())
    graph_params ={ 'node_size': 1750, 
                    'node_color': 'white', 
                    'node_font_size' : 7, 'probs_font_size': 15, 'font_weight': 'bold', 
                    'arrowsize': 8, 'arrowstyle': '->',
                    'edge_color':'black'}   

    # Create and draw a directed graph
    plt.figure(figsize=(10, 3))

    G = nx.MultiDiGraph()
    pos = add_nodes(G, state_numbers, state_names)
    add_edges(G, state_names, mC.transition_matrix)    
    nx.draw(G, pos, with_labels=False, node_size=graph_params['node_size'], node_color=graph_params['node_color'],
            edgecolors='grey', edge_color=graph_params['edge_color'],
            font_size=graph_params['node_font_size'], font_weight=graph_params['font_weight'], 
            arrowsize=graph_params['arrowsize'], arrowstyle=graph_params['arrowstyle'])

    # Use custom labels for nodes (use the 'label' attribute)
    node_labels = nx.get_node_attributes(G, 'label') 
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=graph_params['node_font_size'], font_weight=graph_params['font_weight'])

    # Use custom labels for edges (use the 'weight' attribute)
    edge_labels= nx.get_edge_attributes(G, 'weight')

    # update each pos to move up
    edge_label_pos = {}
    for position in pos:
        edge_label_pos[position] = (pos[position][0], pos[position][1] + 1) 
    nx.draw_networkx_edge_labels(G, edge_label_pos, edge_labels=edge_labels, font_size=graph_params['probs_font_size']-5, font_weight=graph_params['font_weight'], bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgrey'), alpha=0.8)

    # Update the axis limits
    x0, x1 = plt.xlim()  # Get current axis limits
    # plt.axis('off')
    plt.title("Markov Chain: " + mC.name, fontsize=10)
    y0, y1 = plt.ylim()
    plt.ylim(y0-2, y1 +2)
    print(f"y0: {plt.ylim()[0]}, y1: {plt.ylim()[1]}")

    plt.axis('on')
    plt.show()
    nx.drawing.nx_pydot.write_dot(G, 'markov.dot')

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
