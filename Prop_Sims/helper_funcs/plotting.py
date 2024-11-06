import matplotlib.pyplot as plt

def plot_sensed_comps(results, title, graph_type):
                                
    if graph_type == 'bar':                
        # Very simple DataFrame bar plot
        results = results[2:]
        results.plot(kind='bar', stacked=True)
                    #color= [(0.2, 0.6, 0.2), (0.8, 0.8, 0.5), (0.8, 0.2, 0.2), (0.2, 0.2, 0.6)]) # setup for only for options, can be changed

    if graph_type == 'line':
       
        # plot simulation data
        fig = plt.subplots(figsize =(10, 6))
        plt.plot(results['time'], results['number of working comps'], '--*g', label = 'number working comps')
        plt.plot(results['time'], results['number of failed sensors'], '--*y', label = 'number partially working comps')
        plt.plot(results['time'], results['number of failed comps'], '--^r', label = 'number failed comps')
        plt.plot(results['time'], results['number of failed sensors'], '--.b', label = 'number failed sensors')
    
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.title('Sensed Component States over Time: ' + title)
    plt.xlabel('Time')
    plt.ylabel('Number of Components')
    
    
    
    return plt.gcf()



    
def plot_multiple_plots(list_of_plots):
        
    ' a function to take a list of figures and make the one large subplot'
    
    num_plots = len(list_of_plots)
    fig, axs = plt.subplots(num_plots, 1, figsize=(10, num_plots * 5))

    for i, plot in enumerate(list_of_plots):
        for ax in plot.get_axes():
            print('here')
            ax.figure = fig
            fig._axstack.add(fig._make_key(ax), ax)
            fig.axes.append(ax)
            fig.add_axes(ax)
            axs[i].remove()
            fig.add_axes(ax)

    plt.tight_layout()
    plt.show()
    
