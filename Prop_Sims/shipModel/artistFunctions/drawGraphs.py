import networkx as nx
import matplotlib.pyplot as plt


def drawMarkovChain(mC)->None:
    """"
        Draw the Markov Chain as a directed graph

        :param mC: MarkovChain object
    """
    plt.figure(figsize=(10,6))
    node_size = 2000
    font_size= 12

    # grab the states and transition rates from the Markov Chain object
    states = list(mC.state_space.keys())
    state_space = list(mC.state_space)
    print(state_space)
    num_states = len(states)

    # Create a directed graph
    G = nx.DiGraph()
    # G.add_nodes_from(mC.state_space) # no need to add nodes, they are added automatically when edges are added
    
    # add transition probabilities as edges
    for i in range(num_states):
        for j in range(num_states):
            p_ij = mC.transition_matrix[i][j]
            state_i = state_space[i]
            state_j = state_space[j]

            G.add_edge(state_i, state_j, weight=p_ij, label="{:.02f}".format(p_ij), arrowstyle='|-|>', arrowsize=20)

    # Draw the graph with labels
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_size=node_size, node_color='skyblue', edge_color = 'gray', 
            font_size=font_size, font_weight='bold', arrowsize=20, arrowstyle='-|>')
    plt.axis('off')
    
    checkGraphAttributes(G)
    
    plt.savefig("./markovChainImage_"+ mC.name.upper(), bbox_inches='tight')
    plt.show()

# ---------------------------------------------------------------------

def checkGraphAttributes(G)->None:
    """
    A helper functin to check the attributes of the graph object

    """
    print("The graph nodes are : " , list(G.nodes))
    # print("The graph edges are : " ,list(G.edges))
    # print("The graph adjectives are : " ,list(G.adj))
    # print("The graph degrees are : " ,list(G.degree))
    