# Import Arcpy module, interface to ArcGIS
import arcpy

# Import file of user defined variables which contains filepaths to the TIFF files.
os.chdir("E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/")
from myconfig import *

# Using these filepaths construct filepaths to save the asc data to:
# E.g. in the same directory, but with the filepath converted to ASC.
slope_asc_fp = slope_tif_fp.replace('.tif', '.asc.')
elevation_asc_fp = elevation_tif_fp.replace('.tif', '.asc.') 

# Delete files if they already exists to prevent overwriting error.
if arcpy.Exists(slope_asc_fp):
    arcpy.management.Delete(slope_asc_fp)
if arcpy.Exists(elevation_asc_fp):
    arcpy.management.Delete(elevation_asc_fp)

# Convert the raster TIFF datasets to ASCii grid files representing the raster datasets.
# Slope
arcpy.RasterToASCII_conversion(slope_tif_fp,slope_asc_fp)

# Elevation
arcpy.RasterToASCII_conversion(elevation_tif_fp, elevation_asc_fp)
