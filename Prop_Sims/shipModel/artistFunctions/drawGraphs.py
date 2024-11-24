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
    
        # Position the nodes
        if type(pos[0]) == tuple :
            new_pos = (pos[i][0]*fixed_distance, pos[i][1])  # for two level horizontal graph (sensed comp)
            updated_poses.update({state:new_pos})  
        if type(pos[0]) == int:
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
        recurrent_prob = transition_matrix[i][i]
        if recurrent_prob > 0:
            G.add_edge(state_i, state_i, weight=recurrent_prob)  # Recurrent transitions (self-loops)

        for j, state_j in enumerate(states):
        
            forward_prob = transition_matrix[i][j]
            backward_prob = transition_matrix[j][i]
            
            if forward_prob > 0:
                G.add_edge(state_i, state_j, weight=forward_prob)  # Forward transition

            if backward_prob > 0:
                G.add_edge(state_j, state_i, weight=backward_prob) # Backward transition
    return G
    # return edge_labels

# ----------------------------------------------------------------------------------------------
def drawMarkovChain(mC)->None:
    # grab necessary values from the Markov Chain object
    state_numbers = list(mC.state_space.values())
    state_names = list(mC.state_space.keys())
    graph_params ={ 'node_size': 4250, 
                    'node_color': 'none', 
                    'font_size' : 10, 'font_weight': 'bold', 
                    'arrowsize': 10, 'arrowstyle': '->',
                    'edge_color':'black'}   

    # Create and draw a directed graph
    plt.figure(figsize=(10, 3))
    G = nx.DiGraph()
    pos = add_nodes(G, state_numbers, state_names)
    add_edges(G, state_names, mC.transition_matrix)    
    nx.draw(G, pos, with_labels=False, node_size=graph_params['node_size'], node_color=graph_params['node_color'],
            edgecolors='grey', edge_color=graph_params['edge_color'],
            font_size=graph_params['font_size'], font_weight=graph_params['font_weight'], 
            arrowsize=graph_params['arrowsize'], arrowstyle=graph_params['arrowstyle'])

    # Use custom labels for nodes (use the 'label' attribute)
    node_labels = nx.get_node_attributes(G, 'label')  # Get wrapped labels from node attributes
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=graph_params['font_size'], font_weight=graph_params['font_weight'])


    #---- Not working as expected ----
    # Create edge labels (including self-loop edges)
    edge_labels = {}
    edge_label_pos = {}
    for i, j in G.edges:
        weight = round(G[i][j]['weight'], 2)
        edge_labels[(i, j)] = str(weight)  # Assign weights as edge labels

        # Custom positioning for self-loops
        if i == j:  # Self-loop
            x, y = pos[i]  # Position of the node
            edge_label_pos[(i, j)] = (x, y + 0.2)  # Move label slightly above the node
        else:
            # For other edges, position the label at the midpoint (default behavior)
            edge_label_pos[(i, j)] = ((pos[i][0] + pos[j][0]) / 2, (pos[i][1] + pos[j][1]) / 2)

    # check that the edge labels and egde positions have the same keys
    print(edge_labels.keys() == edge_label_pos.keys())

    # Debugging Aid
    print("Graph Edges:", list(G.edges))
    print("Edge Labels:", edge_labels.keys())
    print("Edge Label Positions:", edge_label_pos.keys())       
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=graph_params['font_size'], font_weight=graph_params['font_weight'], bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgrey'), alpha=0.8)

    # nx.draw_networkx_edge_labels(G, edge_label_pos, edge_labels= edge_labels, font_size=graph_params['font_size'], font_weight=graph_params['font_weight'], bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='lightgrey'), alpha=0.8)

    # Update the axis limits
    x0, x1 = plt.xlim()  # Get current axis limits
    plt.xlim(x0 - 0.5, x1 + 0.5)
    y0, y1 = plt.ylim()
    plt.ylim(y0 - 0.5, y1 + 0.5)

    # Finalize the plot
    plt.title("Markov Chain: " + mC.name)
    plt.axis('off')
    plt.show()
# ----------------------------------------------------------------------------------------------

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
