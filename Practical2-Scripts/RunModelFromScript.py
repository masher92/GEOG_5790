'''
Script which runs a ModelBuilder model externally.
Imports the toolbox which contains the model of interest - in this case the "BombExplosion" model from the Practical1_Models.tbx.
This model simulates the impact of a bomb exploding on the buildings in its vicinity.
The model is run by specifiying the locations of the input parameters in the order they are input to the model in ArcGIS.

@author Molly Asher
@Version 1.0
'''

import arcpy

# Set workspace
arcpy.env.workspace = "E:/MSc/Advanced-Programming"

# Specify input parameters for running the model.
explosion_location = "data/input/explosion.shp"
explosion_distance = "100 Meters"
building_shpfile = "data/input/buildings.shp"

# Specify where to save outputs from the model.
destroyed_buildings = "data/generated/destucto4.shp"
# If outputs exist already, then delete them (to avoid overwriting error)
if arcpy.Exists(destroyed_buildings):
    arcpy.Delete_management(destroyed_buildings)

# Run model (with try-catch exceptions)
try:
    # Try importing the toolbox, print error message if it fails.
    try:  
        # Import custom toolbox - "Models", assign alias as Models
        arcpy.ImportToolbox("GitHub/GEOG_5790/Practical1-ModelBuilder/Explosion Toolbox.tbx", "Models")
        print ("Toolbox imported")
    except arcpy.ExecuteError as e:
        print("Import toolbox error", e)
       
    # Try running the model, print error message if it fails.
    try:
        # Run the model 'Bomb Explosion' from the toolbox with alias 'Models'.    
        arcpy.BombExplosion_Models(explosion_location, explosion_distance, building_shpfile, destroyed_buildings)                                                         
        print ("Explosion model executed")                                              
    except arcpy.ExecuteError as e:
        print("Model run error", e)
        
except Exception as e:
    print(e)





