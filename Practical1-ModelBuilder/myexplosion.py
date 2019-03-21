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

Intersect__2_ = arcpy.GetParameterAsText(3)

# Local variables:
Output_Feature_Class = "intermediate"
if arcpy.Exists(Output_Feature_Class):
    arcpy.management.Delete(Output_Feature_Class)

# Process: Buffer
arcpy.Buffer_analysis(explosion_location, Output_Feature_Class, explosion_distance , "FULL", "ROUND", "NONE", "", "PLANAR")

# Process: Intersect
arcpy.Intersect_analysis([building_shpfile ,Output_Feature_Class,], Intersect__2_, "ALL", "", "INPUT")

