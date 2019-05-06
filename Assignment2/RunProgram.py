'''
Set up required functions and import user defined variables
'''
# Import system packages
import os
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import time
from scipy.spatial.distance import pdist, squareform
import math
from sklearn.metrics.pairwise import euclidean_distances
import copy
from pyproj import Proj
import pyproj

# Import user defined functions
os.chdir("E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/")
import My_functions as funcs
from Imported_functions import two_opt 
# Import user defined variables
from myconfig import *

print ("Program initialising")

'''
Read in raster data, convert to dataframe and create categorical slope and elevation variables.
'''
# Read ASCii files to dataframe
slope_df = funcs.read_ascii(slope_tif_fp.replace('.tif', '.asc.'), 'slope')
elevation_df = funcs.read_ascii(elevation_tif_fp.replace('.tif', '.asc.'), 'elevation')

# Combine slope and elevation dataframes and keep only rows which are present in both
combined_df = pd.concat([slope_df['x'], slope_df['y'], slope_df['slope'], elevation_df['elevation']], axis=1, keys=['x', 'y', 'slope', 'elevation']).reset_index()
combined_df = combined_df.dropna() 

# Set CRS definition to apply to geodataframe on the basis of user's projection definition.
if projection == 'British National Grid':
    input_crs = {'init': 'epsg:27700'}
elif projection == 'WGS84/Decimal Degrees':
     input_crs = {'init': 'epsg:4326'}   
else:
    input_crs = {'init': 'epsg:' + projection}

# Trim the slope/elevation dataframe to the area of interest and convert
# to a geodataframe storing x,y coordinates as a geometry column, setting the CRS
# according to user definition.
combined_gdf = funcs.df_to_gdf (aoi_fp, combined_df, input_crs)

# If the CRS is not in BNG then convert it to this (this is required to calculate
# distances between points in metres).
if combined_gdf.crs != {'init': 'epsg:27700'}:
    combined_gdf= combined_gdf.to_crs({'init': 'epsg:27700'})

# Convert back to dataframe
combined_df = pd.DataFrame({'x': combined_gdf.centroid.map(lambda p: p.x), 'y':combined_gdf.centroid.map(lambda p: p.y),
                               'slope' : combined_gdf['slope'], 'elevation': combined_gdf['elevation']})

# Add categorical slope and elevation variables, splitting the continous variable into chunks 
combined_df = funcs.create_binned_variable(combined_df, 'slope', 'Slope_cuts', [0, 5, 10,float('Inf')], ['0-5', '5-10', '30+'])
combined_df = funcs.create_binned_variable(combined_df, 'elevation', 'Elevation_cuts', [230, 260, 290, 320, 350, 380, 410, 440], ['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
combined_df['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(combined_df['Slope_cuts'], combined_df['Elevation_cuts'])]


print ('Data reading and processing complete.')
'''
Create sample from scratch
'''
# Create a dictionary containing the user defined variable values,
# for easy writing to functions.
sample_constraints = {'n_samples' :n_samples, 'n_close_points' : n_close_points,
                      'min_dist' : min_dist, 'max_dist': max_dist}
# Creats a sample:
# A.) Of the size specified by the user
# B.) With the same proportions of each slope and elevation categories as the AOI.
# C.) Where each point has at least n_close_points within min_dist to max_dist of it.
# N versions of the sample are created and the one which covers the smallest area is chosen.
# Setting print_prefercombiendence to "Update Progress" prints update statements, setting it to 'None'
# silences them.
sample = funcs.run_sampling (combined_df, 1, sample_constraints, print_preference = "Update Progress")

# Test whether sample still meets the required distribution.
variable_distribution = pd.DataFrame({'original_props' : round(combined_df['Slope/Elevation'].value_counts()/len(combined_df) * 100,3).reset_index(drop = True),
                     'sample_props' : round(sample['Slope/Elevation'].value_counts()/len(sample) * 100,3).reset_index(drop = True)}).fillna(0)
variable_distribution ['Difference'] = abs(variable_distribution ['sample_props']- variable_distribution ['original_props'])
print ('Sample created.')
print(f"Sample slope and elevation distribution matches distribution of values in whole AOI: {all (x <0.1 for x in variable_distribution['Difference'])}")

#'''
#Create sample with old points.
# INSERT CODE HERE
#'''

'''
Order dataframe to optomise route
'''
# If user has indicated, then find the optimal route to visit the sample locations
# in order to minimise the distance travelled. 
if find_optimum_route == 'Yes':
    start = time.time()
    print ("Optimising route")
    # Create an array containing the sample locations
    sample_locations = np.array(sample[['x', 'y']])
    # Route provides a list of the order to travel to each location by row number
    route = two_opt(sample_locations,0.001)
    # Sort the dataframe according to this order, so points appear in the order they should be visited.
    sample_locations_sorted = np.concatenate((np.array([sample_locations[route[i]] for i in range(len(route))]),np.array([sample_locations[0]])))
    # Plot the locations
    plt.scatter(sample_locations[:,0],sample_locations[:,1])
    # Plot the path.
    plt.plot(sample_locations_sorted[:,0],sample_locations_sorted[:,1])
    plt.show
    # Function to calculate the euclidian distance in n-space of the route r traversing locations c, ending at the path start.
    path_distance = lambda r,c: np.sum([np.linalg.norm(c[r[p]]-c[r[p-1]]) for p in range(len(r))])
    print("Distance of route: " + str(round(path_distance(route,sample_locations),1)) + "m")
    # Return the dataframe in the order the points should be visited
    sample = sample.reindex(route)
    end = time.time()
    print(f"Optimal route to visit sample points identified within {round(((time.time()-start)/60),2)} minutes.")

'''
Create outputs
'''
# Save a csv file containing x and y coordinates and slope.elevation categories
sample[['x','y', 'Slope/Elevation']].to_csv(output_fp, index=False)

# Save interactive output map as HTML, allowing exploration of the sample locations.
# Clicking on a sample point brings up a pop-up showing its coordinates.
funcs.interactive_sample_plot(sample, aoi_fp, output_map_fp)

print ("Outputs saved to file")