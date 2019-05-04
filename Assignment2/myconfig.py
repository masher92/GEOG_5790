'''
Reading in the data.
'''
# Filepath to file containing a slope raster file.
# NB: ensure file paths contain forwardslashes (/) rather than backslashes (\) used in windows file explorer.
slope_tif_fp = "...TestData/Dales_slope_clip.tif"
# Filepath to file contaning an elevation rasterfile.
elevation_tif_fp = "...TestData/Dales_elevation_clip.tif"

# Filepath to file contaning a shapefile of the outline of the area of interest.
aoi_fp = '...TestData/AOI/Humberstone_AOI.shp'
# Projection system in which slope and elevation data is stored:
# Enter: 'British National Grid' or 'WGS84/Decimal Degrees'.
# If neither, insert code from: https://spatialreference.org/ref/epsg/
# in format '2004'
projection = 'British National Grid'

'''
Creating a set of locations to sample peat depths.
'''
# Do you have an existing dataset of peat depth samples?
# Enter: 'Yes' or 'No'
existing_samples = 'No'
# If 'Yes' to above then enter filepath, if not then enter 'None'
peat_depth_samples_fp = '...TestData/ExistingPeatDepthSamples/Humberstone_Peat_depth_points.shp'
# The number of samples you are willing to make.
n_samples = 900
# The desired minimum and maximum distance between points in metres
min_dist = 0.001
max_dist = 90
# The number of points within this distance range that each point should have.
n_close_points =  1

# Would you like to know the optimum order in which to visit sample points in order
# to minimise the distance travelled? 
# NB: This is only recommended for samples under ~ 500 samples, 
# For a sample of this size it would still be likely to take X time.
# Enter: 'Yes' or 'No'
find_optimum_route = 'No'

'''
Location to save output
'''
output_fp = "...Outputs/recommended_sample_sites.csv"
output_map_fp = "Outputs/recommended_sample_sites_map.html"






