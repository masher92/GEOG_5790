'''
Script which runs a ModelBuilder Model as a tool within ArcGIS (NB: it does not function as a stand alone script)
This model constructs a buffer around the locations of a burglaries . 

It takes as inputs:
    The location of burglaries (shp)
    The distance from a burglary in which the increased risk of burglary is felt
    The buildings in the area (shp)

From this it builds a buffer around the explosion area.
This is intersected with the buildings to find those which have been destroyed.

@author Molly Asher
@Version 1.0
'''

import arcpy

# Set working space.
arcpy.env.workspace = "E:/Msc/Advanced-Programming/"

# Specify input parameters.
Burglaries = arcpy.GetParameterAsText(0)
Distance = arcpy.GetParameterAsText(1)
Buildings = arcpy.GetParameterAsText(2)
Out = "data/generated/Practical4/crime.shp"
#Out_sorted = "data/generated/Practical4/crime_sorted.shp"

# If results already exist at the location specified, then delete them (to avoid overwriting error).
if arcpy.Exists(Out):
    arcpy.Delete_management (Out)

# Import custom toolbox - "Practical4_Models", rename as models
arcpy.ImportToolbox("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical4-GUI/Practical4Models.tbx", "models")
# Run the TraffordModel, from within the models toolbox
arcpy.TraffordModel_models(Burglaries, Distance, Buildings, Out)

# 
#if arcpy.Exists(Out_sorted):
#    arcpy.Delete_management (Out_sorted)
# Create the output data, sorted. 
#arcpy.Sort_management(Out, Out_sorted, [["Join_Count", "DESCENDING"]])

# Display the results
# Get current map document
#mxd = arcpy.mapping.MapDocument("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical4-GUI/Prac4.mxd")
# Get bit of it currently showing
#df = mxd.activeDataFrame
# Make a new layer from the data
#newlayer = arcpy.mapping.Layer("data/generated/Practical4/crime_sorted.shp")
# Make a new layer from the example layer file
#layerFile = arcpy.mapping.Layer("data/input/buildings.lyr")
# Update the data layer with the symbolism from the example
#arcpy.mapping.UpdateLayer(df, newlayer, layerFile, True)
# Say that we want it coloured by the values in the "Joint_Count" column.
#newlayer.symbology.valueField = "Join_Count"
# Add all the unique Joint_Count values to the symbolism (otherwise it just displays one colour).
#newlayer.symbology.addAllValues()
# Add the data layer to the map at the TOP.
#arcpy.mapping.AddLayer(df, newlayer,"TOP")
