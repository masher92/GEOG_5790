'''
Set up
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
import functions as funcs
# Import user defined variables
from myconfig_test import *

'''
Read in raster data, convert to dataframe and create categorical slope and elevation variables.
'''
# Read ASCii files to dataframes
slope_df = funcs.read_ascii(slope_asc_fp, 'slope')
elevation_df = funcs.read_ascii(elevation_asc_fp, 'elevation')

# Combine slope and elevation dataframes and keep only rows which are present in both
humberstone_df = pd.concat([slope_df['x'], slope_df['y'], slope_df['slope'], elevation_df['elevation']], axis=1, keys=['x', 'y', 'slope', 'elevation']).reset_index()
humberstone_df = humberstone_df.dropna() 

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
humberstone_gdf = funcs.df_to_gdf (aoi_fp, humberstone_df, input_crs)

# If the CRS is not in BNG then convert it to this (this is required to calculate
# distances between points in metres).
if humberstone_gdf.crs != {'init': 'epsg:27700'}:
    humberstone_gdf= humberstone_gdf.to_crs({'init': 'epsg:27700'})

# Convert back to dataframe
humberstone_df = pd.DataFrame({'x': humberstone_gdf.centroid.map(lambda p: p.x), 'y':humberstone_gdf.centroid.map(lambda p: p.y),
                               'slope' : humberstone_gdf['slope'], 'elevation': humberstone_gdf['elevation']})

# Add categorical slope and elevation variables, splitting the continous variable into chunks 
humberstone_df = funcs.create_binned_variable(humberstone_df, 'slope', 'Slope_cuts', [0, 5, 10,float('Inf')], ['0-5', '5-10', '30+'])
humberstone_df = funcs.create_binned_variable(humberstone_df, 'elevation', 'Elevation_cuts', [230, 260, 290, 320, 350, 380, 410, 440], ['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
humberstone_df['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(humberstone_df['Slope_cuts'], humberstone_df['Elevation_cuts'])]

#humberstone_df.to_csv("E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/Dales_df_bng.csv")
#humberstone_df = pd.read_csv("E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/Dales_df_bng.csv")
dd
'''
Create sample from scratch
'''
# Create a dictionary containing the user defined variable values.
sample_constraints = {'n_samples' :n_samples, 'n_close_points' : n_close_points,
                      'min_dist' : min_dist, 'max_dist': max_dist}
# Creates a sample:
# A.) Of the size specified by the user
# B.) With the same proportions of each slope and elevation categories as the AOI.
# C.) Where each point has at least n_close_points within min_dist to max_dist of it.
# N versions of the sample are created and the one which covers the smallest area is chosen.
sample = funcs.run_sampling (humberstone_df, 1, sample_constraints)

# Test whether sample still meets the required distribution.
variable_distribution = pd.DataFrame({'original_props' : round(humberstone_df['Slope/Elevation'].value_counts()/len(humberstone_df) * 100,3).reset_index(drop = True),
                     'sample_props' : round(sample['Slope/Elevation'].value_counts()/len(sample) * 100,3).reset_index(drop = True)}).fillna(0)
variable_distribution ['Difference'] = abs(variable_distribution ['sample_props']- variable_distribution ['original_props'])
print(f"Sample slope and elevation distribution matches distribution: {all (x <0.1 for x in variable_distribution['Difference'])}")

'''
Order dataframe to optomise route
'''
if find_optimum_route == 'Yes':
    print ("Optimising route")
    # Create an array containing the sample locations
    sample_locations = np.array(sample[['x', 'y']])[:5]
    # Route provides a list of the order to travel to each location by row number
    route = two_opt(sample_locations,0.001)
    # Sort the dataframe according to this order, so points appear in the order they should be visited.
    sample_locations_sorted = np.concatenate((np.array([sample_locations[route[i]] for i in range(len(route))]),np.array([sample_locations[0]])))
    # Plot the locations
    plt.scatter(sample_locations[:,0],sample_locations[:,1])
    # Plot the path.
    plt.plot(sample_locations_sorted[:,0],sample_locations_sorted[:,1])
    plt.show
    print("Distance of route: " + str(round(path_distance(route,cities),1)) + "m")
    # Return the dataframe in the order the points should be visited
    sorted_sample = sample.reindex(route)

'''
Create output
'''
# Return df
sample[['x','y']].to_csv(output_fp)

# Save output map - not plotting poitns and polygons properly?
funcs.interactive_sample_plot(sample, aoi_fp, output_map_fp)
