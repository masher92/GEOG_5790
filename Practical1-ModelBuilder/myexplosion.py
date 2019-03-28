"""
Script exported from a model built in ArcGIS.

It takes as inputs:
    The location of an explosion (shp)
    The distance from the explosion in which its impact is felt
    The buildings in the area (shp)

From this it builds a buffer around the explosion area.
This is intersected with the buildings to find those which have been destroyed.
"""

# Import arcpy module
import arcpy

# Specifies which location the particular parameter will be found at
# in the list of parameters fed to it in Arc.
explosion_location = arcpy.GetParameterAsText(0)
explosion_distance = arcpy.GetParameterAsText(1)
building_shpfile = arcpy.GetParameterAsText(2)

# Define location of where to save the shapefile of the buildings destroyed by the bomb.
destroyed_buildings = arcpy.GetParameterAsText(3)

# Define local variables
buffer_zone = "intermediate"
if arcpy.Exists(buffer_zone):
    arcpy.management.Delete(buffer_zone)

# Process: Buffer
# Creates a circular buffer zone extending out in all directions from the explosion location by the distance specified in the explosion distance.
# Stores this as an intermediate variable.
arcpy.Buffer_analysis(explosion_location, buffer_zone, explosion_distance , "FULL", "ROUND", "NONE", "", "PLANAR")

# Process: Intersect
# Intersects the locations of the buildings with the buffer zone to find those buildings which would be destroyed by the bomb.
# Saves the output as destroyed_buildings file. 
arcpy.Intersect_analysis([building_shpfile ,buffer_zone,], destroyed_buildings, "ALL", "", "INPUT")

