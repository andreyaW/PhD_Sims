import networkx as nx
import matplotlib.pyplot as plt


def drawMarkovChain(mC)->None:
    """"
        Draw the Markov Chain as a directed graph

        :param mC: MarkovChain object
    """
    plt.figure(figsize=(10,7))
    node_size = 200

    # grab the states and transition rates from the Markov Chain object
    states = list(mC.state_space.keys())
    rates = mC.transition_matrix

    # Create a directed graph
    G = nx.MultiDiGraph()
    labels={}
    edge_labels={}
    
    for i, origin_state in enumerate(states):
        for j, destination_state in enumerate(states):
            rate = rates[i][j]
            if rate > 0:
                # G.add_nodes_from(states) # no need to add nodes
                G.add_edge(origin_state, destination_state, weight=rate, label="{:.02f}".format(rate))
                edge_labels[(origin_state, destination_state)] = label="{:.02f}".format(rate)

    
    
    # # Add nodes and edges to the graph
    # for i in range(num_states):
    #     for j in range(num_states):
    #         if mC.transition_matrix[i][j] > 0:
    #             G.add_edge(states[i], states[j], weight = mC.transition_matrix[i][j])

    # Draw the graph with labels
    pos = nx.spring_layout(G)
    # pos = {state:list(state) for state in states}
    nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_weight=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    plt.axis('off');
    plt.savefig("../markovChainImage", bbox_inches='tight')
    plt.show()

    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels = True, node_size = 500, node_color = 'blue', 
    #                 font_size = 10, font_color = 'k', font_weight = 'bold', 
    #                 width = 1, edge_color = 'b')
    # labels = nx.get_edge_attributes(G, 'weight')
    # labels = {k: round(v, 2) for k, v in labels.items()} # round the weights to 2 decimal places    
    # nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)
    # title = mC.name + " Markov Chain Model "
    # plt.title(title)
    # plt.show()