# Import functions
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure
import matplotlib
import matplotlib.animation as anim

# Define variables
num_of_iterations = 10
width = 10
height = 10
fire_start_x = 4
fire_start_y = 4
fuel_amount = 5

# Define function to check environment has been produced correctly
def print_environment():
    for h in range(height):
        for w in range(width):
            print(environment[h][w], end=" ")
        print("")
    print("")

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

# Check the environment
#print_environment()    

# Start a fire by reducing the fuel amount at one cell by 1.
environment[fire_start_y][fire_start_x] -= 1
#print_environment() 
   
def update(num_of_iterations):
    for step in range(num_of_iterations):
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
        matplotlib.pyplot.imshow(environment)
        matplotlib.pyplot.show()
        
    # Stopping condition: exit the iterative process once all the cells within the edge boundary are 0
        total = 0
        for h in range(1, height - 1): 
            for w in range(1, width - 1): 
                total = total + environment[h][w]
        if (total == 0):
            print("ends at iteration ", step)
            break
#update(10)

#-----------------------

"""
Initialise the GUI main window
"""
root = tkinter.Tk() # Main window.
root.wm_title("Forest fire")

"""
Initialise the GUI
"""
# Set up the figure and loop variables.
fig = Figure()
a = fig.add_subplot(111)
#a.imshow(environment)
carry_on = False
init = True
halted = False
rerunid = 0
total_ite = 0;
print("A GUI window should appear. Please select \"Run Model\" from the \"Model\" menu to run the model.")

def run():
    global animation
    animation = anim.FuncAnimation(fig, update, frames=6, repeat=False)
    #canvas.show()
    canvas.draw()

# Create a quit button
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate 
    

# Set up canvas
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# Create a menu bar
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
# Create a drop down menu called Model
menu_bar.add_cascade(label="Model", menu=model_menu)
# Creata an option to run the model
model_menu.add_command(label="Run model", command=run)

# Create the quit button
button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

# 
tkinter.mainloop()


