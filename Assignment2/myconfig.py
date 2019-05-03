'''
Reading in the data.
'''
# Filepath to file containing a slope raster file.
slope_tif_fp = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/TestData/Dales_slope_clip.tif"
# Filepath to file contaning an elevation rasterfile.
elevation_tif_fp = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/TestData/Dales_elevation_tif.asc"
# Filepath to file contaning a shapefile of the outline of the area of interest.
aoi_fp = 'E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/TestData/AOI/Humberstone_AOI.shp'

# Projection system which slope and elevation data is stored:
# Enter: 'British National Grid' or 'WGS84/Decimal Degrees'.
# If neither, insert code from: https://spatialreference.org/ref/epsg/
# in format '2004'
projection = 'British National Grid'

'''
Creating a set of locations to sample peat depths.
'''
# Do you have an existing dataset of peat depth samples?
# Enter: 'Yes' or 'No'
existing_samples = 'Yes'
# If 'Yes' to above then enter filepath, if not then enter 'None'
peat_depth_samples_fp = 'E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/TestData/ExistingPeatDepthSamples/Humberstone_Peat_depth_points.shp'
# The number of samples you are willing to make.
n_samples = 900
# The desired minimum and maximum distance between points in metres
min_dist = 0.001
max_dist = 90
# The number of points within this distance range that each point should have.
n_close_points = 1

# Would you like to know the optimum order in which to visit sample points in order
# to minimise the distance travelled? NB: For a sample size of X this might take X time.
# Enter: 'Yes' or 'No'
find_optimum_route = 'Yes'

'''
Location to save output
'''
output_fp = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/output.csv"
output_map_fp = "E:/Msc/Advanced-Programming/points_map_new.html"






