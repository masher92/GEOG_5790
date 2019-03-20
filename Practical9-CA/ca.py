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

''' Define the model
# Any cell next to a cell on fire, becomes on fire in the next iteration.
Boundary - ignoring the edge (e.g. specifying height -1 and width -1)
'''

# Define number of iterations to run the loop for
num_iterations = 3
# For each of these iterations
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
            
# Loop through number_of_iterations
# Loop through height with variable h
# Loop through width with variable w
# Check values around environment[h][w] for fire
# If fire found, and value in [h][w] > 1, reduce value by 1.