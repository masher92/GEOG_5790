'''
Script which runs a ModelBuilder Model as a tool within ArcGIS (NB: it does not function as a stand alone script).

Research suggests that in the 4 weeks following a house getting burgled there is an increased risk of burglary for the houses in the burgled house's immediate vicinity.
This model uses this theory to analyse the probability of houses in an area getting burgled.  

The model takes as inputs:
* The location of burglaries (shp)
* The distance from a burglary in which the increased risk of burglary is felt
* The buildings in the area (shp)

A buffer is built around the locations of the burglaries and then for each building in the area a count is made of how many of
the burglary buffer zones it intersect with.

This is visualised in....

@author Molly Asher
@Version 1.0
'''

import arcpy

# Set working space.
#arcpy.env.workspace = "E:/Msc/Advanced-Programming/"

# Specify input parameters to be used in the model which is run from the toolbox (define the order in which they should be given)
Burglaries = arcpy.GetParameterAsText(0)
Distance = arcpy.GetParameterAsText(1)
Buildings = arcpy.GetParameterAsText(2)

# Specify location for output files to save to (these will be hardwired into the model i.e. the user will not be asked for them)
crime = "E:/Msc/Advanced-Programming/data/generated/Practical4/crime.shp"
crime_sorted = "E:/Msc/Advanced-Programming/data/generated/Practical4/crime_sorted.shp"

# If results already exist at the location specified, then delete them (to avoid overwriting error).
if arcpy.Exists(crime):
    arcpy.Delete_management (crime)
if arcpy.Exists(crime_sorted):
    arcpy.Delete_management (crime_sorted)

# Import custom toolbox - "Practical4_Models", set alias as models
arcpy.ImportToolbox("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical4-GUI/Practical4Models.tbx", "models")

# Run the TraffordModel from within the models toolbox.
# This will create a 'crime' shapefile, assigning each building a risk of burglary (based on how many burglary buffer zones each house is found within).
arcpy.TraffordModel_models(Burglaries, Distance, Buildings, crime)

# Sort the crime file in descending order, so those at most risk appear at the top.
if arcpy.Exists(crime_sorted):
    arcpy.Delete_management (crime_sorted)
arcpy.Sort_management(crime, crime_sorted, [["Join_Count", "DESCENDING"]])

# Colour code the crime file on the basis of the risk of burglary 
# Apply symbology to it by taking one manually applied to another layer and copying and adapting it:

# Get current map document
mxd = arcpy.mapping.MapDocument("CURRENT")
# Get bit of it currently showing
df = mxd.activeDataFrame

# Make a layer from the crime_sorted file which we want to set the symbology on
newlayer = arcpy.mapping.Layer("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical4-GUI/crime_sorted.shp")
arcpy.mapping.AddLayer(df, newlayer,"TOP")  #BOTTOM or AUTO_ARRANGE

# Make a layer from the file which we want to steal the symbology from.
oldlayer = arcpy.mapping.Layer("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical4-GUI/albertsquare/buildings.lyr")
# Add it to the map (to test if it is being read correctly)
#arcpy.mapping.AddLayer(df, oldlayer,"TOP")  #BOTTOM or AUTO_ARRANGE

# Update the crime layer with the symbolism from the example
arcpy.mapping.UpdateLayer(df, newlayer, oldlayer, True)
# Say that we want it coloured by the values in the "Joint_Count" column.
newlayer.symbology.valueField = "Join_Count"
# Add all the unique Joint_Count values to the symbolism (otherwise it just displays one colour).
newlayer.symbology.addAllValues()
# Add the data layer to the map at the TOP.
arcpy.mapping.AddLayer(arcpy.mapping.MapDocument("CURRENT").activeDataFrame, newlayer,"TOP")

