import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import inspect
import math

from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable


def create_figure(figure_name: str, figure_dict: dict):
    ''' will create a figure for ploting curves
    Args: 
        figure_name; what to call the figure for referencing later and labelling the main curve
        figure_dict: a dicitonary of figures and figure names for referral if more is to be added
    Returns: 
        None
    '''

    # Define a custom style based on seaborn-darkgrid
    custom_style = {
        # 'axes.prop_cycle': plt.cycler(color=['black']),
        # 'axes.prop_cycle': plt.cycler(color=[ 'cornflowerblue', 'limegreen', 'blueviolet', 'crimson',
        #                                       'gold', 'darkturquoise', 'mediumblue', 'lightsteelblue', 
        #                                       'deeppink', 'coral', 'sienna', 'palegreen'                                               
        #                                      ]),

        'axes.prop_cycle': plt.cycler(color=[ 'black', 'blue', 'purple', 'limegreen','goldenrod', 'green', 'red' ]),
        # 'axes.prop_cycle': plt.cycler(marker=['o', 's', '^', 'p', 'd', '>', '<'])
        # Add other style configurations as needed
    }
    plt.style.use(custom_style)   
    
    # Set default font size for axis labels and tick labels
    plt.rcParams.update({'font.size': 14})
        
    fig, ax = plt.subplots(figsize=(10, 6))
    figure_dict[figure_name] = fig, ax
    
    return figure_dict[figure_name]



def determine_object_type(obj):
    ''' determines what type of curve/ curves are being plotted so the figure can be labeled accordingly
    Args: 
        obj : the object (component, component group, system, or vessel) which will be plotted to the figure
    Returns: 
        fig_name: name to refer to the figure as for this objects plot
        obj_curve_name: name for the final curve to be plotted on the graph (solid line)
    '''

    # print(type(obj))

    if inspect.getmodule(obj).__name__ == 'Model.model_component_groups':
        fig_name = 'Comp_Group_#' + str(obj.assignment)
        obj_curve_name = obj.objName
        
    elif inspect.getmodule(obj).__name__ == 'Model.model_system':
        fig_name = 'System_#' + str(obj.assignment)
        obj_curve_name = obj.objName
    
    elif inspect.getmodule(obj).__name__ == 'Model.model_vessel':
        fig_name = 'Vessel_#' + str(obj.assignment)
        obj_curve_name = obj.objName

    return fig_name, obj_curve_name




def plot_R_t(obj, figure_dict: dict, save_folder: str, figure_name:str = None):
    '''will plot and save the R_t of a group of objects (group of comps, system, or vessel)
    Args: 
        obj : the object (component, component group, system, or vessel) which will be plotted to the figure
        figure_dict: dictionary of figures that this figure should already be in or should be added to
        save_folder: folder to save the output plot to
        figure_name: title to store the generated curve under in folder directory
    Returns: 
        None   
    '''
    if figure_name == None:
        figure_name, plot_title = determine_object_type(obj)
    else:
        __ , plot_title = determine_object_type(obj)
    plot_title = plot_title + ' R(t)'
    
    # grab or create figure for this system 
    try: 
        selected_figure, selected_ax = figure_dict[figure_name]
        selected_ax.clear()
    except:
        selected_figure, selected_ax = create_figure(figure_name, figure_dict)
    
    # plot all components
    num_parts = obj.num_parts
    for i in range(num_parts):
        selected_ax.plot(obj.parts[i].t_solved , obj.parts[i].R_t_solved, '.', label = obj.parts[i].objName, markersize=2)    
    
    # plot system curve
    selected_ax.plot(obj.t, obj.R_t, '-', color='black', label = obj.objName)    #highlight system curve in red
    
    # format figure
    selected_ax.legend()
    selected_ax.set_xlabel("Time (Hours)")
    selected_ax.set_ylabel("Probability of Functioning: R(t)")
    selected_ax.set_title(plot_title)

    # Check if the folder exists, create it if not
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Save the figure to the specified folder
    save_path = os.path.join(save_folder, figure_name + '.png')
    plt.savefig(save_path)
    # plt.show()
    plt.close()
    


    
def plot_lookup(obj, figure_dict: dict, save_folder: str): #Union[comp_group, system, vessel]
    '''will plot and save the looked up R_t of a group of objects (group of comps, system, or vessel)
    Args: 
        obj : the object (component, component group, system, or vessel) which will be plotted to the figure
        figure_dict: dictionary of figures that this figure should already be in or should be added to
        save_folder: folder to save the output plot to
    Returns: 
        None   
    '''
    figure_name, plot_title = determine_object_type(obj)
    plot_title = plot_title + ' R(t)'
    
    try: 
        selected_figure, selected_ax = figure_dict[figure_name]
        selected_ax.clear()
    except:
        selected_figure, selected_ax = create_figure(figure_name, figure_dict)

    # plot all components
    num_parts = obj.num_parts
    for i in range(num_parts):
        part = obj.parts[i]
        
        # #always graph the first group in blue
        # if part == obj.parts[0]:
        #     selected_ax.plot(part.lookup_t , part.lookup_R_t, ':b' , linewidth=3.5, label = part.objName) # alpha=0.15*(i+1)
        # elif part == obj.parts[-1]:
        #     selected_ax.plot(part.lookup_t , part.lookup_R_t, ':r' , linewidth=3.5, label = part.objName) # alpha=0.15*(i+1)
        # else:
        selected_ax.plot(part.lookup_t , part.lookup_R_t, ':' , linewidth=3.5, label = part.objName) # alpha=0.15*(i+1)
    
    # plot system lookup curve
    selected_ax.plot(obj.lookup_t, obj.lookup_R_t, color = 'k' ,marker='', linewidth=1.5, linestyle='-',  label = obj.objName) 
    
    # format figure
    selected_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
    # selected_ax.legend(loc='upper right', fontsize='small')
    selected_ax.set_xlabel("Time (Hours)", fontsize=16)
    selected_ax.set_ylabel("Probability of Functioning: R(t)", fontsize= 16)
    selected_ax.set_title(plot_title)

    # Check if the folder exists, create it if not
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Save the figure to the specified folder
    save_path = os.path.join(save_folder, plot_title + '.png')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path


    

def plot_R_t_with_markers(R_ts, ts, fail_labels, figure_dict: dict, figure_name:str, num_parallels:int,  save_folder: str):
   
    '''will plot and save the R_t of a group of objects (group of comps, system, or vessel) and labels the 0th element seperately
    Args: 
        R_ts : the reliabilty curves to add to the plot
        ts : the failure/plotting times for the respective R_t curves
        fail_labels: the list of indexes identifying each systems failure causing part along the R_t curve
        figure_dict: dictionary of figures that this figure should already be in or should be added to
        figure_name: which figure in the dictionary to plot curve on
        save_folder: the output folder to save the plot to
    Returns: 
        None   
    '''
    
    # grab or create a new figure
    try: 
        selected_figure, selected_ax = figure_dict[figure_name]
        selected_ax.clear()
    except:
        selected_figure, selected_ax = create_figure(figure_name, figure_dict)    

    # plot the given R_t curve with labeled parallel failures    
    parallel_fails_R_t, parallel_fails_t = [], []
    non_parallel_fails_R_t, non_parallel_fails_t = [], []

    for i,R_t in enumerate(R_ts):
        R_t= np.array(R_t)
        t= np.array(ts[i])
        fail_label = fail_labels[i]

        if i == 0:
            curve_label = f" {i+2} Low Reliability Parts in Parallel " 
        else:
            curve_label = f" {num_parallels} Low Reliability Parts in Parallel"
            
        # go through all points in the R_t and store labels accordingly
        # parallel_label = str(len(obj.parallels)) + 'n_Parts in Parallel'   ***
        mask = list(fail_label==0)
        non_parallel_fails_R_t = non_parallel_fails_R_t + list(R_t[mask])
        non_parallel_fails_t= non_parallel_fails_t + list(t[mask])

        mask=list(fail_label!=0)
        parallel_fails_R_t = parallel_fails_R_t + list(R_t[mask])
        parallel_fails_t= parallel_fails_t + list(t[mask])

        # plot system curve
        selected_ax.plot(t, R_t, '--', linewidth= 1.5+i, label =curve_label)
        
    # plot markers individually
    selected_ax.plot(parallel_fails_t, parallel_fails_R_t, '^', color= 'red', markersize=1, label="Parallel Failures")
    # selected_ax.plot(non_parallel_fails_t, non_parallel_fails_R_t, ',', linewidth= 0.25, color='green')

    # format figure
    plot_title = "Low Rel Parts in Parallel vs. High Rel Part: " + str(figure_name)
    selected_ax.set_title(plot_title)
    selected_ax.legend(fontsize='small')
    selected_ax.set_xlabel("Time (Hours)")
    selected_ax.set_ylabel("Probability of Functioning: R(t)")

    # Check if the folder exists, create it if not
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Save the figure to the specified folder
    save_path = os.path.join(save_folder, figure_name+'.png')
    # plt.show()
    plt.savefig(save_path)

    return save_path




def calculate_subplot_layout(num_figures):
    """
    Calculate the number of rows and columns required for subplots based on the number of figures.

    Parameters:
        num_figures (int): The number of figures.

    Returns:
        tuple: A tuple containing the number of rows and columns required for subplots.
    """
    # Calculate the number of rows and columns needed
    num_rows = int(math.sqrt(num_figures))
    num_columns = num_figures // num_rows if num_figures % num_rows == 0 else num_figures // num_rows + 1
    
    return num_rows, num_columns



def plot_all_subplots(num_rows, num_cols, file_names, save_folder):
        
    # Create a new figure for the matrix of subplots
    # Set figure size and DPI for good viewing quality
    fig_width = 12  # inches
    fig_height = 12  # inches
    dpi = 500  # dots per inch
    fig, axes = plt.subplots(num_cols, num_rows, figsize=(fig_width, fig_height),  gridspec_kw={'wspace': 0.005, 'hspace' : 0.005}, dpi=dpi)
    # fig, axes = plt.subplots(num_cols, num_rows, figsize=(fig_width, fig_height),  dpi=dpi)
    

    # go to each subplot and add the desired figures
    for i, name in enumerate(file_names):
        row_index = i % num_cols
        col_index = i // num_cols
               
        img = plt.imread(name)  # Read the saved image
        axes[row_index, col_index].imshow(img)
        # axes[row_index, col_index].set_title(name)
        axes[row_index, col_index].axis('off')

    # Adjust layout
    # plt.tight_layout()
    # fig.legend(labels= ['cross tie', 'cooling groups', 'heat excahnge groups'])
    save_path = os.path.join(save_folder, 'matrix_plot.png')
    plt.savefig(save_path)
    # plt.show()
    


    
# function to delete a folder
def delete_folder_contents(folder_path):
    # check folder exists
    if os.path.exists(folder_path):
        # Iterate over the contents of the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            # Check if it's a file or directory
            if os.path.isfile(item_path):
                # If it's a file, delete it
                os.remove(item_path)
                # print(f"File '{item_path}' deleted.")
            elif os.path.isdir(item_path):
                # If it's a directory, recursively call delete_folder_contents
                delete_folder_contents(item_path)
        # After deleting all contents, remove the folder itself
        os.rmdir(folder_path)
    else:
        # create a new empty folder if it was not there to begin with
        os.mkdir(folder_path)



# create a plot for the HMP test
def feasibility_plot(mission_lengths, lifetime_fractions, results, save_folder):

    # close all previous figures
    plt.close("all")


    # Create 3D plot
    fig = plt.figure(figsize=(10,8))
    ax= fig.add_subplot(111,projection='3d')
    # # ax= plt.gca(projection='3d')
    # ax= plt.gca()

    # Plot the points
    X= np.array(mission_lengths)
    Y= np.array(lifetime_fractions)
    Z= np.array(results)
    
    intensity = (Z - np.min(Z)) / (np.max(Z) - np.min(Z))  # Scale Z values between 0 and 1

    sc = ax.scatter(X, Y, Z , c=Z, cmap='jet', marker='s', s=30,edgecolor='black', depthshade=False) #facecolors=plt.cm.jet(intensity)

    # Create color bar on the right
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("bottom", size="5%", pad=0.2)
    # cbar = plt.colorbar(sc, orientation='horizontal', shrink=0.4, label='# of Low Reliability Parts in Parallel')
    # cbar.ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Add labels and title
    ax.set_xlabel('\n \n Mission Length (ML)\n ( in Months)')
    ax.set_ylabel('\n \n Low Reliability Part Lifetime \n (Fraction of Mission Length)')
    ax.set_zlabel('# of Low Reliability \n Parts in Parallel')
    ax.set_title('Necessary Levels of Parallel Redundancy')
    
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))               # make x labels integers
    ax.zaxis.set_major_locator(plt.MaxNLocator(integer=True))               # make z labels integers
    
    # ax.set_shading('flat')
    ax.view_init(23, 47)
    plt.axis('tight')
    # plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

    save_path = os.path.join(save_folder, 'feasibility_plot.png')
    plt.savefig(save_path, dpi=1200)