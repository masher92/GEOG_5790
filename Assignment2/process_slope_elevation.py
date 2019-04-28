#https://gis.stackexchange.com/questions/190561/find-points-that-intersect-a-user-defined-polygon-in-gdal

''' ASCII file reader
ASCii files store raster data as text in equally sixed square rows and columns with a simple header. 
Each cell contains a single numeric value representing feature of the terrain. 
ASCII file format, includes first 6 lines containing:
    ncols: 
    nrows:
    xllcorner:
    yllcorner:
    cellsize:
    NODATA_value:

'''

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

# From: https://stackoverflow.com/questions/37855316/reading-grd-file-in-python
# Should it be cellsize divided by 2 to get the point in the cell
def read_grd(filename, filetype):
    '''
    
    '''
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
      #  nodata_value = int(infile.readline().split()[1])
    #    print ("NoDataValues represented as: ", nodata_value)
        #version = float(infile.readline().split()[1])
        #print(version)
    # Starting from the lower left corner create a point at the distance of each cell.   
  #  longitude = yllcorner + cellsize * np.arange(nrows)
   # latitude = xllcorner + cellsize * np.arange(ncols)
   
    latitude = yllcorner + cellsize * np.arange(nrows)
    longitude = xllcorner + cellsize * np.arange(ncols)
    
    # Load just the data values
    value = np.loadtxt(filename, skiprows=6)
   # value = value.T
    value =np.flipud(value)
    # Convert to dataframe
    df = pd.DataFrame(data=value, index = latitude, columns=longitude)
    # Unstack into rows and columns
    df= pd.DataFrame(df).stack().rename_axis(['y', 'x']).reset_index(name=filetype)
    # Keep only complete cases
    df = df[df[filetype] != -9999]
    # Add ID
    df['ID'] = range(1, len(df) + 1)
    # reorder so x before y
    df = df[['x', 'y', filetype, 'ID']]
    
    end = time.time()
    print("time elapsed:" ,round(((end-start)/60),2) , "minutes" )
    return df
    #return longitude, latitude, value

def df_to_gdf (aoi, df, crs):
    """
    Convert a DataFrame with longitude and latitude columns
    to a GeoDataFrame.
    Keepping only those values found within an AOI.
    """
    start = time.time()
    # Make a copy of the dataframe
    df = df.copy()
    
    # Test polygon
    #poly = [(409840,459080), (409840,489080), (489840,489080), (489840,459080)]
    
    # Define a polgyon around the Area of interest
   # poly = Polygon(aoi.loc[0, 'geometry'])
    # Add a column specifying whether each position in the DF is found within the AOI
    #df["polygon1"] = df.apply(lambda row: Polygon(poly).intersects(Point(row["x"], row["y"])), axis = 1)
    # Keep only those areas which are within the AOI
    #df = df[df.polygon1 == True]
    # For those positions, create geometry combining their X and Y coordinates
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    # Convert those positions into a geodataframe
    gdf = GeoDataFrame(df[['slope', 'elevation']], crs = crs, geometry=geometry)
    end = time.time()
    print("time elapsed:" ,round(((end-start)/60),2) , "minutes" )
    return gdf

def find_dists (sample):
    mat = []
    for i,j in zip(sample['x'],sample['y']):
        k = []
        for l,m in zip(sample['x'],sample['y']):
            k.append(math.hypot(i - l, j - m))
            mat.append(k)
    mat = np.array(mat)
    return mat

def count_close_points(row, dists, dist_min, dist_max):
    close_points = (( dists[row.name]>= dist_min) & ( dists[row.name] <= dist_max))
    #print(close_points.sum())
   # print(row.name, point,close_points.sum() )
    return close_points.sum()

def resample_far_points (sample):
    # Find rows where close points = 0 
    far_points = sample.loc[sample['close_points'] <= n_close_points]
    # Keep only those points which are close enough
    close_points = sample.loc[sample['close_points'] > n_close_points]
    # Create a list of the characteristics needed    
    criteria = sample.loc[sample['close_points'] <= n_close_points, 'Slope/Elevation']
    # Add one row matching each of these criteria to the dataframe 
    for i in range(0,len(criteria)):
        # For each of these create a subset of df meeting criteria
        row = criteria.iloc[i]
        df = humberstone_df.loc[humberstone_df['Slope/Elevation'] == row]
        # Randomly sample one row
        row_to_add = df.sample(n=1)
        # Add it to dataframe
        close_points = close_points.append(row_to_add, sort = True).reset_index(drop = True)
       # print (i)
    # Delete the close points column
    close_points = close_points.drop(['close_points'], axis=1)
    return close_points

def check_for_far_points (sample, min_dist, max_dist ):
    # Find the distance between each pair of points in the sample
    dists = euclidean_distances(sample[['x', 'y']], sample[['x', 'y']])
    # For each sample point, find the number of points within a distance of it.
    sample['close_points'] = sample.apply(count_close_points, dists = dists, dist_min = min_dist, dist_max = max_dist, axis=1)
    # Check numbers
    print("Number points :", sample.loc[sample.close_points <= n_close_points, 'close_points'].count())
    return sample


# Specify variables
input_crs = {'init': 'epsg:4326'}
output_crs = {'init': 'epsg:27700'}



# Filepath to ascii
slope_asc = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/humberstone_slope.asc"
elevation_asc = "E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/Data/humberstone_elevation.asc"

# Read in just the data values from the ASCii
# This skips the header but doesnt keep the information, so we lose the spatial information
#ascii_grid = np.loadtxt(my_asc, skiprows=6)

# Read into dataframe
slope_df = read_grd(slope_asc, 'slope')
elevation_df = read_grd(elevation_asc, 'elevation')

# Join
humberstone_df = pd.concat([slope_df['x'], slope_df['y'], slope_df['slope'], elevation_df['elevation']], axis=1, keys=['x', 'y', 'slope', 'elevation'])
#humberstone_df = humberstone_df.dropna() 

# Outline
aoi = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')
print ("Old AOI CRS: ", aoi.crs)
aoi = aoi.to_crs({'init': list(input_crs.values())[0]})
print ("New AOI CRS: ", aoi.crs)
aoi.plot(color = 'white', edgecolor = 'black')

#### Convert to gdf
humberstone_gdf = df_to_gdf (aoi, humberstone_df, input_crs)

'''
Convert the projection system
'''
humberstone_gdf.crs
humberstone_gdf= humberstone_gdf.to_crs(output_crs)
humberstone_gdf.head(n=2)
humberstone_gdf.plot()
humberstone_gdf.crs

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
humberstone_gdf.plot(column = 'Slope/Elevation', cmap='OrRd')

# plot the data
fig, ax = plt.subplots(figsize  = (8, 6))
humberstone_gdf.plot(column = 'Slope/Elevation', ax = ax)#, legend = True)
ax.set_axis_off()
plt.axis('equal')


'''
Find nearest neighbours
'''

min_dist = 0.001
max_dist = 120
n_samples = 400
n_close_points = 2

done = 'Not Done'
# Take a sample from the dataframe that matches the proportional split between slope and elevation in the whole AOI
sample = humberstone_df.groupby(['Elevation_cuts', 'Slope_cuts'], as_index=False).apply(lambda x: x.sample (frac = n_samples/len(humberstone_df))).reset_index(drop=True)
# Find close points
sample = check_for_far_points(sample, min_dist, max_dist)
# FUnctiona lso adds the close points column on 
# If this sample contains no points which do not have a neighbour within Xm then say the process is done
if sample.loc[sample.close_points <= n_close_points, 'close_points'].count() == 0:
    print("DONE")
# Otherwise,  
else:
    while done != 'Done':
    # Check whether it contains any far points
        sample = resample_far_points (sample)
        sample = check_for_far_points (sample, min_dist, max_dist)
#        print(sample.loc[sample.close_points== 0, 'close_points'].count())
        if sample.loc[sample.close_points <= n_close_points, 'close_points'].count()> 0:
            print("NOT DONE")
        else:
            print ("Done")
            done = 'Done'


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








