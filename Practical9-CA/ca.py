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
print_environment()    

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
# Stopping condition: exit the iterative process once all the cells within the edge boundary are 0
    total = 0
    for h in range(1, height - 1): 
        for w in range(1, width - 1): 
            total = total + environment[h][w]
    if (total == 0):
        print("ends at iteration ", step)
        break
                
