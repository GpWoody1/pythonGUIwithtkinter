
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTk, FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

#-----------------------------------------------------------------------------------------------------------------------
##Define common functions
#-----------------------------------------------------------------------------------------------------------------------

def set_label_stuff(plot,ylab,xlab):
    """
    Function for setting labels of x and y axis
    plot(matplotlib.axes object): The plot to set label
    ylab(string): The label on y axis
    xlab(string): The label on x axis
    """
    plot.set_xlabel(xlab, fontsize='small', fontweight='bold')
    plot.set_ylabel(ylab, fontsize='small', fontweight='bold')
    
    
def emptyplotspace(places):
    """
    function to empty a widget
    places(Tk object): the tk object to empty
    """
    for widgets in places.winfo_children():
        widgets.destroy()   


def plot_me(axis,where):   
    
    """
    function to create matplotlib axis and figure for plots
    axis(list): a list of subplots to make
    where(Tk object): The tk object on which to make the plot
    """
    plotly=[]
    fig = Figure(figsize = (8,5),dpi = 145)
    for i in range(len(axis)):
        my_axis = fig.add_subplot(axis[i])
        plotly.append(my_axis)
    canvas = FigureCanvasTkAgg(fig,where)  
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,where)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    pslabel = Label(where, text= 'Use the Navigation bar below to adjust height and widths of plot for better view', font = ('Helvetica',8,'bold'), bg= '#AA4A44', fg='white')
    pslabel.pack()
    clrplt = Button (where, text= 'Clear Plot', command= lambda:emptyplotspace(where), font = ('Helvetica',10,'bold'), bg= 'red', fg='white')
    clrplt.pack()
    return (plotly,fig)


def covpg1_clr(*cov):
    """
    Function to clear tk variables on screen
    *cov: takes any number of TK var and set them to blank
    """
    for covs in cov:
        covs.set('')

def go_bk(tetris):
    """
    Function to go back. 
    Destroys a toplevel page
    tetris: A tk object
    """
    tetris.destroy()

def end_program(root):
    """
    Function to destroy page. 
    Perform same as go_bk however I defined this to seperate when I call each instance in the program
    root: A tk object
    """
    root.destroy()
