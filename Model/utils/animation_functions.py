"""
animation_functions.py

Contains functions to create drawings onscreen of the systems being tested.

(C) 2023 Regents of the University of Michigan

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Created on Tues August 1 09:04:00 2023

@author: mdcoll, adware

Last Edited: 01 August 2023 by Andreya Ware (adware)
"""
# ------------------------------------------------------------------------------------------------------------------------------------------------ #                                                                                

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np
import textwrap
import imageio
import os

from typing import Union
from Model.model_series_component import series_comp
from Model.model_parallel_component import parallel_comp
from Model.model_component_groups import component_group
from Model.utils import calculator as calc
from Model.model_system import system
# ------------------------------------------------------------------------------------------------------------------------------------------------ #                                                                                

class animation_functions:
    
    figure_num = 0                #figure tracking index
 
    def __init__(self, i: int):
        ''' a class meant to be used as an artist to draw configured systems and groups
        Args:
            i: the artist number / assignment of this instance 
        Returns:
            None
        '''   

        # parameters for drawing parts
        self.comp_height= 2
        self.comp_width= 2
        self.spacing= 1
        
        # parameters for writing words
        self.comp_text_size= 30
        self.group_text_size = 16
        self.sys_text_size= 12  
        
        #create a figure for the animations to be drawn in                  
        self.fig = plt.figure(figsize=(9,6))  
        self.ax = self.fig.add_subplot(111)    
        
        #self.diagram.suptitle(f'Ship #{self.ship_number}')        



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def draw_series_comp(self, axs, x: float, y: float, comp: series_comp, group_or_sys: Union[component_group, system], colors: list[str]):
        ''' Draws a system diagram
        Args:
            axs: the axes to draw onto
            x,y: starting location for the next part to be drawn
            comp: the particular series component to draw
            group_or_sys: component_group object or system object being drawn 
            color: default to silver, change color ot red if this is the first part to fail 
        Returns:
            None
        '''   
        comp_height= self.comp_height
        comp_width= self.comp_width
        spacing= self.spacing
        
        # plot singular series component and its failure time
        color = colors[group_or_sys.series_parts[comp.assignment-1].assignment-1]
        comp_box = patches.Rectangle((x, y), comp_width , comp_height, linewidth=1.5, linestyle='-', edgecolor='k', facecolor=color)
        axs.add_patch(comp_box)

        y= y+comp_height/2        
            
        # for all but first component
        if comp!= group_or_sys.parts[0]:

            # draw line connection from left to the component
            axs.plot( (x-spacing, x), (y, y), '--k', linewidth = 1)        
        
        # for all but last component
        if comp!= group_or_sys.parts[-1]:
            
            # draw line connections from the right to the component
            axs.plot( (x+comp_width, x + spacing + comp_width), (y, y), 'k', linestyle='dashed', linewidth = 1)        



    def draw_parallel_comp(self, axs,  x: float, y: float, comp: parallel_comp, group_or_sys: Union[component_group, system], colors: list[str]):
        ''' Draws a system diagram
        Args:
            axs: the axes to draw onto
            x,y: starting location for the next part to be drawn
            comp: the particular component to draw (series comp from within the parallel set)
            group_or_sys: component_group object or system object being drawn 
            color: default to silver, change color ot red if this is the first part to fail 
        Returns:
            None
        '''   
        comp_height= self.comp_height
        comp_width= self.comp_width
        spacing= self.spacing
        
        # draw each component stacked vertically with connections on left   
        num_parallels= len(comp.parallel_parts)         # how many components in this parallel set
        for j in range(num_parallels):             
            
            # drawing the first part of parallel set
            if j== 0 : 
                # drawing the part
                y=0
                color = colors[group_or_sys.series_parts[comp.assignment-1+j].assignment-1]
                comp_box = patches.Rectangle((x, y), comp_width , comp_height, linewidth=1.5, linestyle='-', edgecolor='k', facecolor=color)
                axs.add_patch(comp_box)

                # drawing the lines
                y= comp_height/2
                if (comp==group_or_sys.parts[0]) & (len(group_or_sys.parts)==1): #special case (only one part)
                    axs.plot( (x-spacing/2, x), (y, y), 'k', linestyle='dashed')
                    axs.plot( (x+comp_width, x + comp_width+ spacing/2), (y, y), 'k', linestyle='dashed')                                  
                
                elif comp == group_or_sys.parts[0]: 
                    # draw connection to start diagram
                    axs.plot( (x-spacing/2,x), (y, y), 'k', linestyle='dashed')
                    axs.plot( (x+comp_width, x + comp_width+ spacing/2), (y, y), 'k', linestyle='dashed')                                  
                
                # from first box over to the next box
                elif comp != group_or_sys.parts[-1]:
                    axs.plot( (x+comp_width, x + comp_width+spacing), (y, y), 'k', linestyle='dashed')                                  
                    axs.plot( (x-spacing, x), (y, y), 'k', linestyle='dashed')    

                # if the component is the last in the set                                                                    
                elif comp == group_or_sys.parts[-1]:
                    # draw connection to end diagram
                    axs.plot( (x-spacing, x), (y, y), 'k', linestyle='dashed')    
                    axs.plot( (x+comp_width, x + comp_width+ spacing/2), (y, y), 'k', linestyle='dashed')                                  

        # for drawing all parts under the first part of parallel set
            else:
            # drawing the part
                #draw next box 1/4*spacing under the previous 
                y_next= (-comp_height-spacing)*(j) 
                # color = colors[group_or_sys.series_parts[comp.assignment-1+j].assignment]
                color= colors[group_or_sys.series_parts[comp.assignment-1+j].assignment-1]
                comp_box = patches.Rectangle((x, y_next), comp_width , comp_height, linewidth=1.5, linestyle='-', edgecolor='k', facecolor=color)
                axs.add_patch(comp_box)
            
            # drawing the lines
                #(LHS)                           
                # vertical portion of L 
                axs.plot( (x-spacing/2, x-spacing/2), (y_next+comp_height*2, y_next+comp_height/2), 'k', linestyle='dashed')                                  
                #horizontal portion of L 
                axs.plot( (x-spacing/2, x), (y_next+comp_height/2, y_next+comp_height/2), 'k', linestyle='dashed')                                
                
                # (RHS)
                #vertical portion of L 
                axs.plot( (x+comp_width+spacing/2, x+comp_width+spacing/2), (y_next+comp_height*2, y_next+comp_height/2), 'k', linestyle='dashed')                                
                #horizontal portion of L 
                axs.plot( (x+comp_width, x+comp_width+spacing/2), (y_next+comp_height/2, y_next+comp_height/2), 'k', linestyle='dashed')                                



    def draw_comp_label(self, axs,  x: float, y: float, comp: Union[series_comp, parallel_comp], group_or_sys: Union[component_group, system], fail_times: list[float]):
        # grab text writing parameters          
        comp_text_size= self.comp_text_size

        # grab size of the part 
        comp_width= self.comp_width
        comp_height = self.comp_height
        spacing = self.spacing

        if isinstance(comp, series_comp):
            # add name label on box
            label= f"#{group_or_sys.series_parts[comp.assignment-1].assignment}"
            # wrapped_label = self.fit_text_in_box(label, comp_width)
            center_x, center_y= x+ comp_width/2, y + comp_height/2
            axs.text(center_x, center_y, label, ha = 'center', va = 'bottom', fontsize=comp_text_size)

            # # add failure time to the box
            # fail_label = "{:.2f}".format(fail_times[comp.assignment-1][0])
            # center_y = center_y -comp_height/4
            # axs.text(center_x, center_y, fail_label, ha= 'center', va='bottom', fontsize=comp_text_size)

        else: 

            for j in range(len(comp.parallel_parts)):
                y_next= (-comp_height-spacing)*(j) 
                y= y_next

                # add name label on box
                label= f"#{group_or_sys.series_parts[comp.assignment-1+j].assignment}"
                # wrapped_label = self.fit_text_in_box(label, comp_width)
                center_x, center_y= x+ comp_width/2, y + comp_height/2
                axs.text(center_x, center_y label, ha = 'center', va = 'bottom', fontsize=comp_text_size)

                # # add failure time to the box
                # fail_label = "{:.2f}".format(fail_times[comp.assignment-1+j][0])
                # center_y = center_y -comp_height/4
                # axs.text(center_x, center_y, fail_label, ha= 'center', va='bottom', fontsize=comp_text_size)
                
    def draw_group_or_sys_label(self, group_or_sys: Union[component_group, system]):
        if isinstance(group_or_sys, component_group):
            large_label_size= self.group_text_size
        else: 
            large_label_size= self.sys_text_size 

        '''
        #add system label and failure time
        sys_label= "System #{:.0f} fails @".format(sys_assignment)
        center_x, center_y= centerline,  axis_y[1]- max(4, (axis_y[1]-axis_y[0])/10)
        sys_axs.text(center_x, center_y, sys_label, ha='right', va='bottom',    fontsize= sys_label_size, fontweight='bold', color='black')

        sys_fail_time= min(sys_fail)
        sys_fail_label= "{:.2f}hrs".format(sys_fail_time)                      
        sys_axs.text(center_x, center_y, sys_fail_label, ha='left', va='bottom',    fontsize=sys_label_size, fontweight='bold', color='black')
        '''



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def draw_group(self, comp_group: component_group, mission_length: float = None, save_folder: str = None, fig:plt.figure = None): # x0: float = 0, y0: float = 0
        ''' Draws a system diagram
        Args:
            comp_group: component_group object 
            save_folder: the folder to save the daigram to 
        Returns:
            save_path : string path to the image
        '''   
        # setting drawing parameters
        comp_width= self.comp_width
        spacing= self.spacing
        x,y = 0,0
        
        # call function to grab the failure times and colors for all parts to be drawn       
        group_fails, colors = self.determine_times_N_colors(comp_group, mission_length)

        # grab the figure and axis 
        if fig == None:
            __, comp_group_axs = self.fig, self.ax
            
        else: 
            comp_group_axs = plt.figure(figsize=(6,9)).add_subplot(111)

        # iterate through all parts in the group and plot accordingly         
        for i,comp in enumerate(comp_group.parts):        
                
            # determine if parallel or series component
            if isinstance(comp , parallel_comp): 
                # draw a parallel component
                self.draw_parallel_comp(comp_group_axs, x, y, comp, comp_group, colors)

                # draw comp label and fail time
                self.draw_comp_label(comp_group_axs, x, y, comp, comp_group, group_fails)

            else:
                # draw a series component
                self.draw_series_comp(comp_group_axs, x, y, comp, comp_group, colors)
                            
                # draw comp label and fail time
                self.draw_comp_label(comp_group_axs, x, y, comp, comp_group, group_fails)

            # move to next drawing space
            x= x+ (comp_width+spacing)
        
        # ensure axis is updated to only include final parts drawn
        comp_group_axs.set_xlim(comp_group_axs.get_xlim()[0]-spacing, x+spacing)
                
        # create a box border                
        rec = plt.Rectangle((comp_group_axs.get_xlim()[0], comp_group_axs.get_ylim()[0]), (comp_group_axs.get_xlim()[1] - comp_group_axs.get_xlim()[0]), (comp_group_axs.get_ylim()[1] - comp_group_axs.get_ylim()[0]), fill=False, linestyle="-", linewidth = 2)
        rec = comp_group_axs.add_patch(rec)
        
        # formatting
        comp_group_axs.axis("off")
     
        # Check if the folder exists, create it if not
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Save the figure to the specified folder
        save_path = os.path.join(save_folder, 'Group_#' + str(comp_group.assignment) +' Diagram.png')
              
        # only close plot if not plotting group as a part of a system
        if fig!= None:
            plt.savefig(save_path, bbox_inches='tight')
            return save_path
        else:        
            plt.savefig(save_path)  
            plt.close()


    def add_image(self, ax, image_path, x, y, width, height):
        img = mpimg.imread(image_path)
        ax.imshow(img, extent=[x, x + width, y, y + height], aspect='auto')


    def add_group_to_axs(self, fig, comp_group, sys_axs,saved_image_path, x, y):
        # Specify the position and size of the Axes in figure coordinates        
        # left, bottom, width, height (fractions of figure width)
        # sys_axs = fig.axes
        width=self.comp_width
        height=self.comp_height
        self.add_image(sys_axs, saved_image_path, x, y, width, height)
       
        # print("sys width size limits: ", sys_axs.get_xlim()[1])
        # print("sys height size limits: ", sys_axs.get_ylim()[1])

        # print("(x,y) = ", x, y)
       
        # left= sys_axs.get_xlim()[1] *0.75 
        # print('left: ', left)
        
        # bottom= 0.1
        # print('bottom: ', bottom)
        
        # width= 2
        # print('width: ', width)
        
        # height = 0.8
        # print('height: ', height)
                
        # group_axs = fig.add_axes([left, bottom, width, height])
        # print("group width size limits: ", group_axs.get_xlim())
        # print("group height size limits: ", group_axs.get_ylim())

        
        # img = mpimg.imread(saved_image_path)
        # group_axs.imshow(img)

        # group_axs.axis("off")
        
        # x= x + width
        # return x

        ''' inserting secondary axis (kaggle tutorial)
        fig = plt.figure()

        axes1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
        axes2 = fig.add_axes([0.2, 0.5, 0.4, 0.3]) # inset axes

        # main figure
        axes1.plot(x, y, 'r')
        axes1.set_xlabel('x')
        axes1.set_ylabel('y')
        axes1.set_title('title')

        # insert
        axes2.plot(y, x, 'g')
        axes2.set_xlabel('y')
        axes2.set_ylabel('x')
        axes2.set_title('insert title');
        '''

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def draw_sys(self, sys: system, save_folder: str= None, mission_length: float = None):                 
        ''' Draws a system diagram
        Args:
            sys: system object 
            save_folder: the folder to save the daigram to 
        Returns:
            None
        '''            
        
        # setting drawing parameters
        x,y = 0,0
        comp_width= self.comp_width
        spacing= self.spacing
        fig, sys_axs = self.fig, self.ax          
        
        # call function to grab the failure times and colors for all parts to be drawn       
        sys_fails, colors = self.determine_times_N_colors(sys, mission_length)
            
        for i,part in enumerate(sys.parts):        
            
            # if series component ...
            if isinstance(part, series_comp):
                self.draw_series_comp(sys_axs, x, y, part, sys, colors)
                
                # draw comp label and fail time
                self.draw_comp_label(sys_axs, x, y, part, sys, sys_fails)
                
            # if parallel component ...
            if isinstance(part , parallel_comp): 
                self.draw_parallel_comp(sys_axs, x, y, part, sys, colors)     
    
                # draw comp label and fail time
                self.draw_comp_label(sys_axs, x, y, part, sys, sys_fails)

            # if group of components ...
            if isinstance(part , component_group):
                
                # call a function to draw the group in the next space
                current_pos= sys_axs.get_position()    #grabs the bounding box around the current axs     
                saved_image_path = self.draw_group(part, mission_length, save_folder, fig, current_pos) # x, y
                self.add_group_to_axs( fig, part, sys_axs, saved_image_path, x, y )

            # move to next drawing space
            x= x+ (comp_width+spacing)

        # ensure axis is updated to only include final parts drawn
        # sys_axs.set_xlim(sys_axs.get_xlim()[0], x+spacing)

        # add space to show the item that was drawn
        sys_axs.set_ylim(sys_axs.get_ylim()[0] - spacing, sys_axs.get_ylim()[1])

        # create a box border                
        # rec = plt.Rectangle((sys_axs.get_xlim()[0], sys_axs.get_ylim()[0]), (sys_axs.get_xlim()[1] - sys_axs.get_xlim()[0]), (sys_axs.get_ylim()[1] - sys_axs.get_ylim()[0]), fill=False, linestyle="-", linewidth = 2)
        # rec = sys_axs.add_patch(rec)

        # formatting
        sys_axs.axis("off")

        # Check if the folder exists, create it if not
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        # Save the figure to the specified folder
        save_path = os.path.join(save_folder, 'System #' + str(sys.assignment) +' Diagram.png')
        fig.savefig(save_path)
        plt.tight_layout()        
        plt.close()
        


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def determine_times_N_colors(self, group_or_sys: Union[component_group, system], mission_time=None):
        num_comps= len(group_or_sys.series_parts)
        fail_times= np.zeros((num_comps,1))
        colors = []        
        
        if mission_time == None: 
            # grab all failure times of comps and the system 
            # all comps start silver 
            for i, part in enumerate(group_or_sys.series_parts):          
                fail_times[i] = part.t[-1]
                # fail_times[i] = np.mean(part.t)
                colors.append('white')

            true_fail = group_or_sys.t[-1]
            # true_fail = np.mean(group_or_sys.t[-1])


        else:
            # grab and normalize all failure times of comps and the system
            # all comps start silver  
            for i,part in enumerate(group_or_sys.series_parts):   
                fail_times[i] = part.t[-1] / mission_time
                # fail_times[i] = np.mean(part.t)/ mission_time
                colors.append('white')    
            
            true_fail = group_or_sys.t[-1] / mission_time
            # print('normalized sys fail is:', true_fail)
            
            # true_fail = np.mean(group_or_sys.t) / mission_time
            # print('mean sys fail is:', true_fail)

        # determine which part to mark red (failure cause)
        red_idx= fail_times == true_fail
        red_idx = np.where(red_idx == True)[0]
        colors = np.array(colors, dtype= 'str_')
        # colors[red_idx]= 'maroon'

        return fail_times, colors



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def fit_text_in_box(self, text, box_width):
        # Decides when to wrap the text to fit within the box width
        wrapped_text = textwrap.fill(text, width=box_width*8)
        
        # If the wrapped text has more lines than the box height, truncate it
        lines = wrapped_text.split('\n')
        if len(lines) > box_width:
            lines = lines[:box_width]
            wrapped_text = '\n'.join(lines)
        return wrapped_text

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
     
    def add_failure_times(self, sys):
        # setting drawing parameters
        x,y = 0,0 
        comp_height= self.comp_height
        comp_width= self.comp_width
        spacing= self.spacing            
        comp_text_size= self.comp_text_size
        sys_label_size= self.sys_text_size
        fig, sys_axs = self.diagram                  # grab the figure and axis 
        
        #must index if more then one system
        sys_assignment = sys.assignment -1
        if self.num_sys >1:
            sys_axs=sys_axs[sys_assignment]

        # VECTOR FOR STORING ALL FAIL TIMES
        sys_fail = []

        for i,comp in enumerate(sys.sysComps): 
            parallels_added = 0
            
            #determine if parallel or series component
            if isinstance(comp , parallel_comp): 

                # draw each component stacked vertically with connections on left   
                num_parallels= len(comp.parallel_parts)         # how many components in this parallel set
                for j in range(num_parallels):             
                    
                    #draw first box of set normally
                    if j== 0 : 
                        
                        # if the component is the first in the set  
                        y= comp_height/2                             
                        
                        # draw comp label and failure time on box
                        comp_label= comp.parallel_parts[j]
                        center_x, center_y= x+ comp_width/2, y
                        sys_axs.text(center_x, center_y, comp_label, ha='center', va='bottom',    fontsize=comp_text_size, fontweight='bold', color='black')

                        fail_time= self.fail_times.item(comp_label-1)
                        sys_fail.append(fail_time)
                        comp_fail_label= "{:.2f}".format(fail_time)                                 
                        center_y =center_y -comp_height/2
                        sys_axs.text(center_x, center_y, comp_fail_label, ha='center', va='bottom',    fontsize=comp_text_size, fontweight='bold', color='black')
                        
                    #for all boxes under the first, draw a L down to the box
                    else:
                        
                        #draw next box 1/4*spacing under the previous 
                        y_next= (-comp_height-comp_height/2)*(j) 
                        
                        # draw comp label and failure time on box
                        comp_label= comp.parallel_parts[j]
                        center_x, center_y= x+ comp_width/2, y_next+comp_height/2
                        sys_axs.text(center_x, center_y, comp_label, ha='center', va='bottom',    fontsize=comp_text_size, fontweight='bold', color='black')

                        fail_time= self.fail_times.item(comp_label-1)
                        sys_fail.append(fail_time)
                        comp_fail_label= "{:.2f}".format(fail_time)                      
                        center_y =center_y -comp_height/2
                        sys_axs.text(center_x, center_y, comp_fail_label, ha='center', va='bottom',    fontsize=comp_text_size, fontweight='bold', color='black')
                
            else:
                # plot singular series component and its failure time
                y=0                  
                
                # draw comp label and failure time on box
                comp_label= comp.assignment
                center_x, center_y= x+ comp_width/2, comp_height/2
                sys_axs.text(center_x, center_y, comp_label, ha='center', va='bottom',    fontsize=comp_text_size, fontweight='bold', color='black')

                fail_time= self.fail_times.item(comp_label-1)
                sys_fail.append(fail_time)
                comp_fail_label= "{:.2f}".format(fail_time)                       
                center_y =center_y -comp_height/2
                sys_axs.text(center_x, center_y, comp_fail_label, ha='center', va='bottom',    fontsize=comp_text_size, fontweight='bold', color='black')
        
            # move to next drawing space
            x= x+ (comp_width+spacing)                                
        
        #determine center and top of the plot
        centerline = np.mean(sys_axs.get_xlim())

        #add space to draw above the system 
        axis_y = sys_axs.get_ylim() 
        push_up= (-0.5, 12)
        axis_y= tuple(np.add(axis_y, push_up))            
        sys_axs.set_ylim(axis_y)

        #add system label and failure time
        sys_label= "System #{:.0f} fails @".format(sys_assignment)
        center_x, center_y= centerline,  axis_y[1]- max(4, (axis_y[1]-axis_y[0])/10)
        sys_axs.text(center_x, center_y, sys_label, ha='right', va='bottom',    fontsize= sys_label_size, fontweight='bold', color='black')

        sys_fail_time= min(sys_fail)
        sys_fail_label= "{:.2f}hrs".format(sys_fail_time)                      
        sys_axs.text(center_x, center_y, sys_fail_label, ha='left', va='bottom',    fontsize=sys_label_size, fontweight='bold', color='black')   


            
    def create_failure_gif(self, system, time_vector):
        images = []

        # Loop to add each frame to the gif
        for i in range(len(time_vector)): 
            # Create a new image with white background
            img = self.diagram
            self.draw_sys(system)
            
            # grab the Reliability value of the component at time t
            
            
            # Add some text
            

            # Append the image to the images list
            images.append(img)
            
            

        # Save the images as a gif
        imageio.mimsave('created_gif.gif', [imageio.imread(i) for i in images])

                
        
        
            
            
            
            
   