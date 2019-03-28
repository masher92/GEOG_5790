"""
Converts a layer file into a shapefile and saves it.
"""

import arcpy

# Name the layer
lyr =  "explosion_lyr"

# Define location of existing layer file and desired location of generated shape file.
sf = "E:/MSc/Advanced-Programming/input/explosion.shp"
lf = "E:/MSc/Advanced-Programming/Practical2/data/generated/explosion.lyr"

# Make a layer in memory
arcpy.management.MakeFeatureLayer(sf, lyr)
# Save this layer in memory to a file
arcpy.management.SaveToLayerFile(lyr, lf, "ABSOLUTE")

