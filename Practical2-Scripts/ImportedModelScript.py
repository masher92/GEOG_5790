import arcpy

arcpy.AddMessage("Script running")

## Change settings in arcGIS: Geoprocessing: Options: Select overwrite outputs
arcpy.env.overwriteOutput=True 

# Specify input parameters
explosion_location = arcpy.GetParameterAsText(0)
explosion_distance = arcpy.GetParameterAsText(1)
building_shpfile = arcpy.GetParameterAsText(2)

# Set up a local variable to store the buffer zone (this should not be saved anywhere externally)
# Prevent overwriting error i.e. if this local variable already exists, then delete it.
Output_Feature_Class = "intermediate"
if arcpy.Exists(Output_Feature_Class):
    arcpy.management.Delete(Output_Feature_Class)

# Specify where to save outputs
destroyed_buildings = arcpy.GetParameterAsText(3)    

## Specify a default value if an output location is not given.
#if destroyed_buildings == '#' or not destroyed_buildings 
#    destroyed_buildings = "E:/Msc/Advanced-Programming/Practical1" # provide a default value if unspecified

arcpy.AddMessage("Imported files")

# If results already exist at the location specified, then delete them (to avoid overwriting error)
if arcpy.Exists(destroyed_buildings):
    arcpy.Delete_management(destroyed_buildings)
    print("Deleted")
else:
    print("Not deleted")

# Run model (with try-catch exceptions)    
# Print error message if running model fails
try:
        # Run buffer analysis
        arcpy.Buffer_analysis(explosion_location, Output_Feature_Class, explosion_distance , "FULL", "ROUND", "NONE", "", "PLANAR")
	arcpy.AddMessage("Created buffer")
        # Process: Intersect
        arcpy.Intersect_analysis([building_shpfile ,Output_Feature_Class,], destroyed_buildings, "ALL", "", "INPUT")
        pythonaddins.MessageBox("Process run", "Update")
except arcpy.ExecuteError as e:
        print("Model run error", e)




