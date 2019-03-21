'''
Script which

'''

import arcpy

# Set workspace
w = "E:/MSc/Advanced-Programming"
arcpy.env.workspace = w

# Specify input parameters
explosion_location = w + "data/input/explosion.shp"
explosion_distance = "100 Meters"
building_shpfile = w + "data/input/buildings.shp",

# Specify intermediate parameter
# ?

# Specify where to save output outputs
destroyed_buildings = w + "/data/generated/result_test.shp"

# Output results file path
results = w + "/data/generated/result_test.shp"

# If results exist already, then delete them (to avoid overwriting error)
if arcpy.Exists(results):
    arcpy.Delete_management(results)

arcpy.ImportToolbox(w + "/GitHub/GEOG_5790/Practical1-ModelBuilder/Practical1_Models.tbx", "Models")
arcpy.MyExplosion_Models(explosion_location,explosion_distance,
                                 building_shpfile, destroyed_buildings)                                                        
                                                          
'''
# Run model (with try-catch exceptions)
try:
    # Print error message if Model toolbox import fails
    try:  
        # Import custom toolbox - "Models", rename as Models
        arcpy.ImportToolbox(w + "/GitHub/GEOG_5790/Practical1-ModelBuilder/Practical1_Models.tbx", "Models")
    except arcpy.ExecuteError as e:
        print("Import toolbox error", e)
       
    # Print error message if running model fails
    try:
        # Run MyExplosion, feeding in parameters.    
        arcpy.MyExplosion_Models(explosion_location,explosion_distance,
                                 building_shpfile, destroyed_buildings)                                                        
                                                          
    except arcpy.ExecuteError as e:
        print("Model run error", e)
        
except Exception as e:
    print(e)

'''


