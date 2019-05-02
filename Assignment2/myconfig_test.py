'''
Reading in the data.
'''
# Filepath to file containing a slope raster file.
slope_asc_fp = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/humberstone_slope.asc"
# Filepath to file contaning...
elevation_asc_fp = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/humberstone_elevation.asc"
# Filepath to file contaning...
aoi_fp = 'E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp'

# Projection system which slope and elevation data is stored:
# Choose from: 'British National Grid' or 'WGS84/Decimal Degrees'.
# If neither, insert code from: https://spatialreference.org/ref/epsg/
# in format '2004'
projection = 'WGS84/Decimal Degrees'

'''
Creating a set of locations to sample peat depths.
'''
# Do you have an existing dataset of peat depth samples?
existing_samples = 'Yes'
# If 'Yes' to above then enter filepath, if not then enter 'None'
peat_depth_samples_fp = 'E:/Msc/Dissertation/Code/Data/Input/PeatDepth/Humberstone_Peat_depth_points.shp'
# The number of samples you are willing to make.
n_samples = 900
# The desired minimum and maximum distance between points
min_dist = 0.001
max_dist = 90
# The number of points within this distace range that each point should have.
n_close_points = 1


'''
Location to save output
'''
output_fp = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/output.csv"

