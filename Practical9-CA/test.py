# Import packages
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import csv
import numpy as np
import matplotlib.animation as anim
import matplotlib
import matplotlib.pyplot as pyplot

# Define function to check environment has been produced correctly
def print_environment():
    for h in range(height):
        for w in range(width):
            print(environment[h][w], end=" ")
        print("")
    print("")
    
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate    


"""
Step 1: Initialise parameters.
"""
number_of_iterations = 10
width = 10
height = 10
fire_start_x = 4
fire_start_y = 4
fuel_amount = 5

"""
Step 2: Initialise GUI main window.
"""
print("Step 2: Initialise GUI main window")
root = tkinter.Tk() # Main window.
root.wm_title("Model")
fig = Figure()
a = fig.add_subplot(111)
#a.imshow(environment)

"""
Step 3: Initialise environment containing information about area in which fire 
takes place.
"""
# Create a 2D environment containing the fuel amount in each point.
environment = []
results = []
for h in range(height):
    row = []
    results_row = []
    for w in range (width):
        row.append (fuel_amount)
        results_row.append (fuel_amount)
    environment.append(row)
    results.append(results_row)
    #matplotlib.pyplot.imshow(environment)
    #matplotlib.pyplot.show()    
    
"""
Step 5: Animate the spread of the fire.
"""    
def update(num_iterations):
    for step in range(num_iterations):
        for h in range(1, height - 1):
            for w in range(1, width - 1):
                global environment
                # For each position in the environment, check if that cell or any of 
                # the neighbouring cells are on fire  
                status = "NotOnFire"
                if (environment [h][w]) < fuel_amount: status = "OnFire"
                if (environment [h-1][w-1]) < fuel_amount: status = "OnFire"
                if (environment [h-1][w]) < fuel_amount: status = "OnFire"   
                if (environment [h-1][w+1]) < fuel_amount: status = "OnFire"   
                if (environment [h+1][w-1]) < fuel_amount: status = "OnFire"
                if (environment [h+1][w]) < fuel_amount: status = "OnFire"   
                if (environment [h+1][w+1]) < fuel_amount: status = "OnFire"   
                if (environment [h][w-1]) < fuel_amount: status = "OnFire"
                if (environment [h][w+1]) < fuel_amount: status = "OnFire"  
                # If status in any of these cells is OnFire, then set cell on fire
                if (status == 'OnFire') & (environment[h][w] > 0):
                    results[h][w] -= 1
        environment= results
        print_environment()
        #matplotlib.pyplot.imshow(environment)
        #matplotlib.pyplot.show()
        
    # Stopping condition: exit the iterative process once all the cells within the edge boundary are 0
        total = 0
        for h in range(1, height - 1): 
            for w in range(1, width - 1): 
                total = total + environment[h][w]
        if (total == 0):
            print("ends at iteration ", step)
            break

update(10)


"""
Step 4: Initialise the GUI
"""
print("Step 6: Initialising GUI.")
# Set up the figure and loop variables.
fig = pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
carry_on = True
init = True
halted = False
rerunid = 0
total_ite = 0;
print("A GUI window should appear. Please select \"Run Model\" from the \"Model\" menu to run the model.")

animation = anim.FuncAnimation(fig, update, frames=10, repeat=False)        


canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def run():
    global animation
    animation = anim.FuncAnimation(fig, update, frames=10, repeat=False)
    #canvas.show()
    canvas.draw()
    
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)
#model_menu.add_command(label="Exit", command=root.quit)
#model_menu.add_command(label="Destroy", command=root.destroy)

root = tkinter.Tk()


canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()    
#root.protocol('WM_DELETE_WINDOW', exiting) 

tkinter.mainloop() # Wait for interactions.

print("Thank you for running the model.")