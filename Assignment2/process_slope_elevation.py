# Import packages
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

def read_ascii(filename, filetype):
    """
    Opens an ASCii file and reads in the values as a numpy array.
    Reads the xllcorner (x lower-left coordinate), yllcorner (y lower-left coordinate), cell-size,
    ncols (number of columns) and nrows (number of rows) stored in the first 6 lines of the ASCii file
    and uses this information to assign geographic information to the data values.
    : param filename: The filepath to the ASCii file to read in (str)
    : param filetype: A string containing the kind of data stored in the ASCii file.
    : return df: A dataframe containing x, y and value data stored as rows. 
    """
    start = time.time()
    with open(filename) as infile:
        ncols = int(infile.readline().split()[1])
        print("ncols:" , ncols)
        nrows = int(infile.readline().split()[1])
        print("nrows: ", nrows)
        xllcorner = float(infile.readline().split()[1])
        print ("xllcorner: ", xllcorner)
        yllcorner = float(infile.readline().split()[1])
        print ("yllcorner: ", yllcorner)
        cellsize = float(infile.readline().split()[1])
        print("Cell size: ", cellsize)
        nodata_value = int(infile.readline().split()[1])
        print ("NoDataValues represented as: ", nodata_value)
        #version = float(infile.readline().split()[1])
        #print(version)
        
    # Create an array of latitude and longitude values using the lower left x and y coordinates, 
    # the ncols and nrows and half of the cellsize (to get the mid point of each cell)
    latitude = yllcorner + (cellsize/2) * np.arange(nrows)
    longitude = xllcorner + cellsize * np.arange(ncols)
    
    # Load the data values (excluding the first 6 rows containing the descriptive information)
    value = np.loadtxt(filename, skiprows=6)
    # Flip the array as the values are upside down
    value =np.flipud(value)
    # Convert to dataframe (in same structure as array but with latitude and longitude values added)
    df = pd.DataFrame(data=value, index = latitude, columns=longitude)
    # Unstack into rows and columns
    df= pd.DataFrame(df).stack().rename_axis(['y', 'x']).reset_index(name=filetype)
    # Keep only rows containing a data value
    df = df[df[filetype] != nodata_value]
    # Add an ID tag to each row 
    df['ID'] = range(1, len(df) + 1)
    # reorder so x before y
    df = df[['x', 'y', filetype, 'ID']]
    
    end = time.time()
    print("time elapsed:" ,round(((end-start)/60),2) , "minutes" )
    return df


def df_to_gdf (aoi, df, crs):
    """
    Converts a dataframe into a geodataframe storing x,y values as geometry points.
    Only keeps rows in the dataframe which are found within an area of interest.  
    : param aoi: A shapefile containing the area of interest as a polygon.
    : param df: A dataframe containing x, y and additional values as columns. 
    : param crs: A (type?) storing the CRS in which the x, y values are stored.    
    : return gdf: A geodataframe version of the data. 
    """

    start = time.time()
    # Make a copy of the dataframe
 #   df = df.copy()
   
    # Create a polgyon out ot the Area of interest
    # poly = Polygon(aoi.loc[0, 'geometry'])
    # Add column to dataframe specifying whether each row's geometry intersects the AOI
    #df["InAoi"] = df.apply(lambda row: Polygon(poly).intersects(Point(row["x"], row["y"])), axis = 1)
    # Keep only those rows which are within the AOI
    #df = df[df.InAoi == True]
    # Store the geometry of those rows by combining their X and Y coordinates
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    # Convert those positions into a geodataframe, alongside their data values.
    gdf = GeoDataFrame(df[['slope', 'elevation']], crs = crs, geometry=geometry)
    end = time.time()
    print("time elapsed:" ,round(((end-start)/60),2) , "minutes" )
    return gdf

def find_dists (sample):
    """
    Finds distance between each point in a dataframe and another..
    : param sample: 
    : return:  

    """
    mat = []
    for i,j in zip(sample['x'],sample['y']):
        k = []
        for l,m in zip(sample['x'],sample['y']):
            k.append(math.hypot(i - l, j - m))
            mat.append(k)
    mat = np.array(mat)
    return mat

def count_close_points(row, dists, dist_min, dist_max):
    """
    Calculates the number of points within a specified distance of an x, y coordinate.
    : param row: A row number in a dataframe with X and Y coordinates stored as columns. 
    : param dists: A matrix containing the distance of all rows in a dataframe to each other. 
    : param dist_min : The minimum distance apart which points may be from one another.
    : param dist_max : The maximum distance apart which points may be from one another.
    : return close_points.sum(): The number of points within the specified distance range (integer/float)  
    """
    # Should i recreate dists each time this is run?
    close_points = (( dists[row.name]>= dist_min) & ( dists[row.name] <= dist_max))
    #print(close_points.sum())
    #print(row.name, point,close_points.sum() )
    return close_points.sum()

def find_near_neighbours (df, dist_min, dist_max ):
    """
    Adds a column to dataframe containing rows of X, Y coordinates specifying the number of 
    points from the dataframe which are within range(dist_min, dist_max) of that point. 
    : param df: A dataframe with X and Y coordinates stored as columns (in BNG projection)
    : param dist_min: The minimum distance apart which points may be from one another
    : param dist_max: The maximum distance apart which points may be from one another
    : return new_sample_df:  

    """
    # Find the distance between each pair of points in the sample
    dists = euclidean_distances(df[['x', 'y']], df[['x', 'y']])
    # For each sample point, find the number of points within a distance of it.
    df['close_points'] = df.apply(count_close_points, dists = dists, dist_min = dist_min, dist_max = dist_max, axis=1)
    # Check numbers
    print("Number points :", df.loc[sample.close_points <= n_close_points, 'close_points'].count())
    return sample


def resample_far_points (sample_df, original_df, n_close_points):
    """
    Removes rows from a dataframe which have less than a specified number of points close to them.
    For each row which is removed, randomly selects a row from the  original dataframe which has the same
    'Slope/Elevation' category as the removed row. 
    Join the newly sampled rows back onto the sample dataframe.
    : param sample_df: Dataframe containing rows which were sampled from original_df
    : param original_df: Dataframe from which the sample was drawn.
    : param n_close_points: Number of points required by user to be 'close' to each point in the sample. 
    : return new_sample_df:  Dataframe containing new sample of same size as input sample_df 

    """
    # Keep only those points which have > n_close_points close to them.
    new_sample_df = sample_df.loc[sample_df['close_points'] > n_close_points]
    # Create a list of the 'Slope/Elevation values of the points which are removed from the dataframe
    criteria = sample_df.loc[sample_df['close_points'] <= n_close_points, 'Slope/Elevation']
    # Add one row matching each of these criteria to the new sample dataframe 
    for i in range(0,len(criteria)):
        # For each of these create a subset of df meeting criteria
        df = original_df.loc[original_df['Slope/Elevation'] == criteria.iloc[i]]
        # Randomly sample one row from those available
        row_to_add = df.sample(n=1)
        # Add it to dataframe
        new_sample_df = new_sample_df.append(row_to_add, sort = True).reset_index(drop = True)
       # print (i)
    # Delete the close points column (so it can be recreated)
    new_sample_df = new_sample_df.drop(['close_points'], axis=1)
    return new_sample_df



# Specify CRS of input ASCii file.
input_crs = {'init': 'epsg:4326'}
output_crs = {'init': 'epsg:27700'}

# Filepath to ascii
slope_asc = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/humberstone_slope.asc"
elevation_asc = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/humberstone_elevation.asc"
print ("Files read")

# Read into dataframe
slope_df = read_ascii(slope_asc, 'slope')
elevation_df = read_ascii(elevation_asc, 'elevation')

# Join
humberstone_df = pd.concat([slope_df['x'], slope_df['y'], slope_df['slope'], elevation_df['elevation']], axis=1, keys=['x', 'y', 'slope', 'elevation'])

# Outline
aoi = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')
print ("Old AOI CRS: ", aoi.crs)
aoi = aoi.to_crs({'init': list(input_crs.values())[0]})
print ("New AOI CRS: ", aoi.crs)
aoi.plot(color = 'white', edgecolor = 'black')

#### Convert to gdf
humberstone_gdf = df_to_gdf (aoi, humberstone_df, input_crs)
print ("Converted to GDF")

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
humberstone_df['Slope_cuts'] = pd.cut(humberstone_df['slope'], bins=[0, 5, 10,float('Inf')],
           labels=['0-5', '5-10', '30+'])
humberstone_df['Elevation_cuts'] = pd.cut(humberstone_df['elevation'], bins=[230, 260, 290, 320, 350, 380, 410, 440],
           labels=['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
humberstone_df['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(humberstone_df['Slope_cuts'], humberstone_df['Elevation_cuts'])]

'''
Group by binned variables
'''
#sample = humberstone_df.groupby(['Elevation_cuts', 'Slope_cuts'], as_index=False).apply(lambda x: x.sample (frac=0.01)).reset_index(drop=True)

# Check values in each
#sample.Elevation_cuts.value_counts()


''' Check spatial distribution of classes'''
humberstone_gdf['Slope_cuts'] = pd.cut(humberstone_gdf['slope'], bins=[0, 5, 10,float('Inf')],
           labels=['0-5', '5-10', '30+'])
humberstone_gdf['Elevation_cuts'] = pd.cut(humberstone_gdf['elevation'], bins=[230, 260, 290, 320, 350, 380, 410, 440],
           labels=['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
# Add a combined variable
humberstone_gdf['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(humberstone_gdf['Slope_cuts'], humberstone_gdf['Elevation_cuts'])]
#humberstone_gdf.plot(column = 'Slope/Elevation', cmap='OrRd')

# plot the data
#fig, ax = plt.subplots(figsize  = (8, 6))
#humberstone_gdf.plot(column = 'Slope/Elevation', ax = ax)#, legend = True)
#ax.set_axis_off()
#plt.axis('equal')


'''
Find nearest neighbours
'''

min_dist = 0.001
max_dist = 20
n_samples = 400
n_close_points = 6

start = time.time()
done = 'Not Done'
# Take a sample from the dataframe that matches the proportional split between slope and elevation in the whole AOI
sample = humberstone_df.groupby(['Elevation_cuts', 'Slope_cuts'], as_index=False).apply(lambda x: x.sample (frac = n_samples/len(humberstone_df))).reset_index(drop=True)
# For each point in the sample, find the number of neighbours it has within a range between min_dist and max_dist
sample = find_near_neighbours(sample, min_dist, max_dist)
# FUnctiona lso adds the close points column on 
# If this sample contains no points which do not have a neighbour within Xm then say the process is done
if sample.loc[sample.close_points <= n_close_points, 'close_points'].count() == 0:
    print("DONE")
# Otherwise,  
else:
    while done != 'Done':
    # Check whether it contains any far points
        sample = resample_far_points (sample)
        sample = find_near_neighbours (sample, min_dist, max_dist)
#        print(sample.loc[sample.close_points== 0, 'close_points'].count())
        if sample.loc[sample.close_points <= n_close_points, 'close_points'].count()> 0:
            print("NOT DONE")
        else:
            print ("Done")
            done = 'Done'
    end = time.time()
    print("time elapsed:" ,round(((end-start)/60),2) , "minutes" )

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
Save shapefile
'''
# Save
#dales_gdf.to_file(driver = 'ESRI Shapefile', filename= "E:/Msc/Dissertation/Code/Data/Generated/dales_gdf.shp")
sample.to_csv("E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/sample.csv", index=False)

'''
Read in points
'''
# Original with no slope and elevation
#pdp = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/PeatDepth/Humberstone_Peat_depth_points.shp')
#pdp.plot()
#pdp.crs
#pdp = pdp.to_crs({'init':'epsg:27700'})

# Find their slope and elevation values
#test =gpd.sjoin(pdp, humberstone_gdf, how='left', op='intersects', lsuffix='left', rsuffix='right')
#humberstone_gdf['geometry'] = round(humberstone_gdf['geometry'][0], 3)

# With slope and elevation
pdp = gpd.read_file('E:/Msc/Dissertation/Code/Data/Generated/humberstone.shp')
# Create binned variables, according to user defined groups
pdp['Slope_cuts'] = pd.cut(pdp['Slope_5m'], bins=[0, 5, 10,float('Inf')],
           labels=['0-5', '5-10', '30+'])
pdp['Elevation_cuts'] = pd.cut(pdp['elevation'], bins=[230, 260, 290, 320, 350, 380, 410, 440],
           labels=['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
pdp['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(pdp['Slope_cuts'], pdp['Elevation_cuts'])]

#
n_samples = 700
original= round(humberstone_df['Slope/Elevation'].value_counts()/len(humberstone_df) ,3)

df = pd.DataFrame({'numbers_got' : pdp['Slope/Elevation'].value_counts(),
                    'numbers_needed' : original * n_samples})
df = df.fillna(0)

df['numbers_still_needed']  = np.where(df['numbers_needed'] - df['numbers_got'] > 0 , 
  df['numbers_needed'] - df['numbers_got'],
  0)
  

