import matplotlib.pyplot as plt

def plot_sensed_comps(results, title, graph_type):
                                
    if graph_type == 'bar':                
        # Very simple DataFrame bar plot
        results.plot(kind='bar', stacked=True,
                     color= [(0.2, 0.6, 0.2), (0.8, 0.2, 0.2), (0.2, 0.2, 0.6)])


        # # set plot parameters
        # barWidth = 300     # width of bar 
        # fig = plt.subplots(figsize =(12, 8))  

        # # Horizontal Bar Plot
        # plt.bar(results['time'], results['number of working comps'], 
        #         color ='g', width = barWidth, edgecolor ='grey', label ='working components', bottom=0)
        # # plt.bar(results['time'], results['number of failed comps'], 
        # #         color ='r', width = barWidth, edgecolor ='grey', label ='failed components')
        # plt.bar(results['time'], results['number of failed sensors'], 
        #         color ='b', width = barWidth, edgecolor ='grey', label ='failed sensors')
        # plt.legend()

    if graph_type == 'line':
       
        # plot simulation data
        fig = plt.subplots(figsize =(10, 6))
        plt.plot(results['time'], results['number of working comps'], '*g', label = 'number working comps')
        plt.plot(results['time'], results['number of failed comps'], '^r', label = 'number failed comps')
        plt.plot(results['time'], results['number of failed sensors'], '.b', label = 'number failed sensors')
    
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.title('Sensed Component States over Time: ' + title)
    plt.xlabel('Time')
    plt.ylabel('Number of Components')

