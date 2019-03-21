"""
Cellular Automata model of the spread of a forest fire.
An environment is established, with an amount of fuel present at each location.  
A fire is started at one location by decreasing the amount of fuel there.
Any cell next to a cell on fire will also catch fire.
The amount of fuel at a location determines whether it is, is not or has been on fire.
With each time step, the fuel at a location on fire decreases by 1.
The model ends once the whole area is burnt out (e.g. the amount of fuel is 0)
For the purposes of the model, the boundary cells are ignored. (e.g. specifying height -1 and width -1)
@author Molly Asher
@Version 1.0
"""

import matplotlib

# Define variables
number_of_iterations = 10
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
print_environment() 

# Model the spread of fire through the environment over X number iterations
num_iterations = 30
for step in range(num_iterations):
    for h in range(1, height - 1):
        for w in range(1, width - 1):
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
Step 2: Initialise GUI main window.
"""
# Import packages
import os
import agentframework9 as af
import random
#import operator
from sys import argv
import csv
import matplotlib
matplotlib.use('TkAgg') # Needs to be before any other matplotlb imports
#matplotlib.use('TkInter')
import matplotlib.pyplot as pyplot
import matplotlib.animation as anim
import tkinter
import requests
import bs4

print("Step 2: Initialise GUI main window")
root = tkinter.Tk() # Main window.
root.wm_title("Model")

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


#animation = anim.FuncAnimation(fig, update, interval=1, repeat=False, frames=num_of_iterations)

def run():
    global animation
    animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    #canvas.show()
    canvas.draw()

canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)