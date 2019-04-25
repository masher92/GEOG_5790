"""
Script exported from a model built in ArcGIS (NB: it does not function as a stand alone script)

It takes as inputs:
    The location of an explosion (shp)
    The distance from the explosion in which its impact is felt
    The buildings in the area (shp)

From this it builds a buffer around the explosion area.
This is intersected with the buildings to find those which have been destroyed.

@author Molly Asher
@Version 1.0
"""

# Import arcpy module
import arcpy

# Print inititalising message
arcpy.AddMessage("Script running")

# Define which parameter (in a list of parameters fed to Arc) will be used for each of the following:
explosion_location = arcpy.GetParameterAsText(0)
explosion_distance = arcpy.GetParameterAsText(1)
building_shpfile = arcpy.GetParameterAsText(2)

# Set up a local variable to store the buffer zone (this should not be saved anywhere externally)
# Prevent overwriting error i.e. if this local variable already exists, then delete it.
buffer_zone = "intermediate"
if arcpy.Exists(buffer_zone):
    arcpy.management.Delete(buffer_zone)

# Define which parameter will be used to save the shapefile of the buildings destroyed by the bomb.
# Prevent overwriting error i.e. if this local variable already exists, then delete it.
destroyed_buildings = arcpy.GetParameterAsText(3)
if arcpy.Exists(destroyed_buildings):
    arcpy.management.Delete(destroyed_buildings)
arcpy.AddMessage("Imported files")    
    
# Process: Buffer
# Creates a circular buffer zone extending out in all directions from the explosion location by the distance specified in the explosion distance.
# Stores this as an intermediate variable.
arcpy.Buffer_analysis(explosion_location, buffer_zone, explosion_distance , "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.AddMessage("Created buffer")

# Process: Intersect
# Intersects the locations of the buildings with the buffer zone to find those buildings which would be destroyed by the bomb.
# Saves the output as destroyed_buildings file. 
arcpy.Intersect_analysis([building_shpfile ,buffer_zone,], destroyed_buildings, "ALL", "", "INPUT")
arcpy.AddMessage("Identified destroyed buildings")

# Print completion message
arcpy.AddMessage("Model run complete.")
