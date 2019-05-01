# Import packages
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

# Specify CRS of input ASCii file.
input_crs = {'init': 'epsg:4326'}
output_crs = {'init': 'epsg:27700'}

# Filepath to ascii
slope_asc = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/dales_slope.asc"
elevation_asc = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/dales_elevation.asc"
print ("Files read")

# Read into dataframe
slope_df = read_ascii(slope_asc, 'slope')
elevation_df = read_ascii(elevation_asc, 'elevation')

# Join and keep only rows which are present in both
humberstone_df = pd.concat([slope_df['x'], slope_df['y'], slope_df['slope'], elevation_df['elevation']], axis=1, keys=['x', 'y', 'slope', 'elevation']).reset_index()
# Check rows with NA values
null_data = humberstone_df[humberstone_df.isnull().any(axis=1)]
# Keep only rows which have values for both
humberstone_df = humberstone_df.dropna() 

# Outline
aoi = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')
#aoi = aoi.to_crs({'init': list(input_crs.values())[0]})
aoi.plot(color = 'white', edgecolor = 'black')

#### Convert to gdf
humberstone_gdf = funcs.df_to_gdf (aoi, humberstone_df, input_crs)
print ("Converted to GDF")
humberstone_gdf.plot()

'''
Convert the projection system
'''
humberstone_gdf.crs
humberstone_gdf= humberstone_gdf.to_crs(output_crs)
humberstone_gdf.head(n=2)
humberstone_gdf.plot()
humberstone_gdf.crs
print ("Converted projection")

# Convert back to dataframe
humberstone_df = pd.DataFrame({'x': humberstone_gdf.centroid.map(lambda p: p.x), 'y':humberstone_gdf.centroid.map(lambda p: p.y),
                               'slope' : humberstone_df['slope'], 'elevation': humberstone_df['elevation']})

'''
Add binned variables
'''
# Create binned variables, according to user defined groups
humberstone_df = create_binned_variable(humberstone_df, 'slope', 'Slope_cuts', [0, 5, 10,float('Inf')], ['0-5', '5-10', '30+'])
humberstone_df = create_binned_variable(humberstone_df, 'elevation', 'Elevation_cuts', [230, 260, 290, 320, 350, 380, 410, 440], ['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
humberstone_df['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(humberstone_df['Slope_cuts'], humberstone_df['Elevation_cuts'])]

'''
Create sammple from scratch
'''
min_dist = 0.001
max_dist = 90
n_samples = 900
n_close_points = 1

sample = create_df_sample(humberstone_df, min_dist, max_dist, n_samples, n_close_points )

# Check location of samples
geometry = [Point(xy) for xy in zip(sample.x, sample.y)]
# Convert those positions into a geodataframe
gdf = GeoDataFrame(sample[['slope', 'elevation']], crs= output_crs, geometry=geometry)
# Plot
gdf.plot()
dists = euclidean_distances(sample[['x', 'y']], sample[['x', 'y']])
tes= dists[1]
test =np.sort(tes)

# Check if sample points fit the distribution
# Check values in each
sample_props = round(sample['Slope/Elevation'].value_counts()/len(sample) * 100,3).reset_index(drop = True)
original_props = round(humberstone_df['Slope/Elevation'].value_counts()/len(humberstone_df) * 100,3).reset_index(drop = True)
# Check if they are the same - because of rounding they are not, so need to decide whether I need this.
sample_props ==original_props


'''
Create sample using existing dataset
'''
# Read in original with no slope and elevation
pdp = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/PeatDepth/Humberstone_Peat_depth_points.shp')
pdp.plot()
pdp.crs

# Cnvert to a dataframe (done think we need to do this)
pdp_df = pd.DataFrame({'x': pdp.centroid.map(lambda p: p.x), 'y':pdp.centroid.map(lambda p: p.y)})

# Find its slope and elevation values
pdp_df['slope'] = [get_value_from_closest_point(pdp_df, row_number, humberstone_df, 'slope')  for row_number in range(0,len(pdp_df))]
pdp_df['elevation'] = [get_value_from_closest_point(pdp_df, row_number, humberstone_df,'elevation')  for row_number in range(0,len(pdp_df))]

# Add binned variables
pdp_df = create_binned_variable(pdp_df, 'slope', 'Slope_cuts', [0, 5, 10,float('Inf')], ['0-5', '5-10', '30+'])
pdp_df = create_binned_variable(pdp_df, 'elevation', 'Elevation_cuts', [230, 260, 290, 320, 350, 380, 410, 440], ['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
pdp_df['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(pdp_df['Slope_cuts'], pdp_df['Elevation_cuts'])]
pdp_df =pdp_df[['x','y', 'Slope/Elevation']]

# make copy
original_df = copy.deepcopy(humberstone_df)
original_df =original_df[['x','y', 'Slope/Elevation']]

# Add some extra points randomly to the original sample points
extra = original_df.sample(n=100)

# Tag
pdp_df['origin'] = 'original_point'
extra['origin'] = 'new_point'
        
# Starting dataframe
resample= pdp_df.append(extra, sort = True).reset_index(drop = True)
# Find near neihgbours in original sample
resample = find_near_neighbours(resample, min_dist, max_dist)

# If all points have enough points near them, then done....
if resample.loc[resample.close_points <= n_close_points, 'close_points'].count() == 0 :
   print("Done")
# If not then....resample the bad points 
else:
    nope = 'nope'
    while nope == 'nope':
        resample = resample_far_points2 (resample, original_df, n_close_points)
        resample = find_near_neighbours (resample, min_dist, max_dist)
        # IF any rows in dataframe have less than specified number of close points then resample
        if resample.loc[resample.close_points <= n_close_points, 'close_points'].count()> 0:
                print("Resampling")
        else:
                print ("Sampling complete")
                nope = 'Yup'
        # Delete the close points column (so it can be recreated)
        #new_sample = new_sample.drop(['close_points'], axis=1)

# Check location of samples
geometry = [Point(xy) for xy in zip(resample.x, resample.y)]
# Convert those positions into a geodataframe
gdf = GeoDataFrame(resample[['Slope/Elevation', 'origin', 'close_points']],  geometry=geometry)

# Sjow where new points are/
gdf['origin'] =gdf['origin'] .astype('category')
gdf.plot(column = 'close_points', cmap = 'brg')    
gdf.plot(column = 'origin', cmap = 'brg')    

'''
Need to edit it so that if there are 0 new points which < n_close_points to randomly resample


Minimum number of new points which could be added to achieve a sample size of X which meets criteria

Or, assume that there is a minimum sample size needed for the model
And try and resample keeping as many of the old points as possible adding new ones.

'''

min_dist = 0.001
max_dist = 90
n_samples_already = len(pdp)
n_samples = 800
min_requirement = n_samples-  n_samples_already
n_close_points = 1

# make copy
original_df = copy.deepcopy(humberstone_df)
original_df =original_df[['x','y', 'Slope/Elevation']]

# Add some extra points randomly to the original sample points
extra = original_df.sample(n=88)

# Tag
pdp_df['origin'] = 'original_point'
extra['origin'] = 'new_point'

# Given n_samples, this is the required distribution 
requirements = pd.DataFrame({'numbers_needed' : round(humberstone_df['Slope/Elevation'].value_counts()/len(humberstone_df) * n_samples, 0)})

# Create first sample with the minimum number of points added
resample= pdp_df.append(extra, sort = True).reset_index(drop = True)
# Check distances
resample = find_near_neighbours(resample, min_dist, max_dist)

      
# From function        
# Keep only those points which have > n_close_points close to them.
new_sample_df = sample_df.loc[((sample_df['close_points'] >= n_close_points) & (sample_df['origin'] == 'new_point'))|(sample_df['origin'] == 'original_point')]
# Create a list of the 'Slope/Elevation values of the points which are removed from the dataframe
criteria = sample_df.loc[(sample_df['close_points'] < n_close_points) & (sample_df['origin'] == 'new_point'), 'Slope/Elevation']
   
    # Add one row matching each of these criteria to the new sample dataframe 
    for i in range(0,len(criteria)):
        # For each of these create a subset of df meeting criteria
        df = original_df.loc[original_df['Slope/Elevation'] == criteria.iloc[i]]
        # Randomly sample one row from those available
        row_to_add = df.sample(n=1)
        row_to_add['origin'] = 'new_point'
        
        # Add it to dataframe
        new_sample_df = new_sample_df.append(row_to_add, sort = True).reset_index(drop = True)
       # print (i)
    # Delete the close points column (so it can be recreated)
    new_sample_df = new_sample_df.drop(['close_points'], axis=1)
    
    
'''
Buffer Roads
'''
# Read in original with no slope and elevation
roads = gpd.read_file('E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/SE_Road.shp')
roads.head(n=2)

# plot the data
fig, ax = plt.subplots(figsize  = (8, 6))
gdf.plot( ax = ax)#, legend = True)
roads.plot(ax = ax, cmap = 'magma')
#ax.set_axis_off()
#plt.axis('equal')
plt.show()

### CHECK AOI projection
# Create a polgyon out ot the Area of interest
poly = Polygon(aoi.loc[0, 'geometry'])
# Add column to dataframe specifying whether each row's geometry intersects the AOI
roads["InAoi"] = roads.apply(lambda row: Polygon(poly).intersects(row.geometry), axis = 1)    
    
# Keep only those rows which are within the AOI
roads = roads[roads.InAoi == True]
roads.plot()
