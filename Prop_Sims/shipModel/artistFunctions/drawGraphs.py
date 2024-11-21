import networkx as nx
import matplotlib.pyplot as plt



def drawMarkovChain(mC)->None:
    # Create a figure and axes
    fig, ax = plt.subplots()

    states= mC.state_space.keys()
    transition_matrix = mC.transition_matrix

    # Draw the states as nodes
    for i, state in enumerate(states):
        ax.add_patch(plt.Circle((i, 0), radius=0.25, color="white", ec="black"))
        ax.text(i, 0, state, ha="center", va="center", fontsize=12)

    # Draw the transitions as arrows
    for i, row in enumerate(transition_matrix):
        for j, prob in enumerate(row):
            if prob > 0:
                ax.annotate("", xy=(j, 0), xytext=(i, 0),
                            arrowprops=dict(arrowstyle="-|>", color="black", lw=prob*3))
                ax.text((i+j)/2, 0.1, f"{prob:.2f}", ha="center", va="center", fontsize=10)

    # Set the axis limits and labels
    ax.set_xlim(-0.5, len(states)-0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.axis('off')

    # Show the plot
    plt.show()



def drawMarkovChain(mC)->None:
    """"
        Draw the Markov Chain as a directed graph

        :param mC: MarkovChain object
    """
    plt.figure(figsize=(10,10))

    # grab the states and transition rates from the Markov Chain object
    states = list(mC.state_space.keys())
    state_space = list(mC.state_space)
    num_states = len(states)

    # Create a directed graph
    G = nx.DiGraph()
    # G.add_nodes_from(mC.state_space) # no need to add nodes, they are added automatically when edges are added
    
    # add transition probabilities as edges
    edge_labels = []
    for i in range(num_states):
        for j in range(num_states):
            p_ij = mC.transition_matrix[i][j]
            state_i = state_space[i]
            state_j = state_space[j]
            
            label_ij = "{:.02f}".format(p_ij)
            edge_labels.append((state_i, state_j, label_ij))
            G.add_edge(state_i, state_j, weight=p_ij, label=label_ij, arrowstyle='|-|>', arrowsize=20)

    # Draw the graph with labels
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    options = {
    "with_labels": True,
    "font_size": 7,
    "font_weight": "bold",
    "node_size": 8000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 1,
    "arrowstyle": '-|>',
    "arrowsize": 5,
    }
    nx.draw(G, pos, **options)
    plt.axis('off')
    
    # checkGraphAttributes(G)
    plt.savefig("./markovChainImage"+ mC.name.upper(), bbox_inches='tight')

# ---------------------------------------------------------------------

def checkGraphAttributes(G)->None:
    """
    A helper functin to check the attributes of the graph object

    """
    print("The graph nodes are : " , list(G.nodes))
    # print("The graph edges are : " ,list(G.edges))
    # print("The graph adjectives are : " ,list(G.adj))
    # print("The graph degrees are : " ,list(G.degree))

# ---------------------------------------------------------------------
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
