import networkx as nx
import matplotlib.pyplot as plt


def drawMarkovChain(mC)->None:
    """"
        Draw the Markov Chain as a directed graph

        :param mC: MarkovChain object
    """
    # grab the number of states and state names from the Markov Chain object
    num_states = len(mC.state_space)
    states = list(mC.state_space.keys())

    # Create a directed graph
    G = nx.Graph()
    G.add_nodes_from(states)
    
    # Add nodes and edges to the graph
    for i in range(num_states):
        for j in range(num_states):
            if mC.transition_matrix[i][j] > 0:
                G.add_edge(states[i], states[j], weight = mC.transition_matrix[i][j])

    # Draw the graph with labels
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True, node_size = 100, node_color = 'y', font_size = 10, font_color = 'k', font_weight = 'bold', width = 2, edge_color = 'b')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)
    plt.show()
