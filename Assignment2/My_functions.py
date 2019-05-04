# Import all functions required within the functions
# These need to be imported in here to execute functions from another file.
import time
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame, read_file
#import math
from shapely.geometry import Point, Polygon
from sklearn.metrics.pairwise import euclidean_distances
import os
import folium

# Import user defined functions
os.chdir("E:/Msc/Advanced-Programming/Github/GEOG_5790/Assignment2/")
import functions as funcs
from imported_functions import minimum_bounding_rectangle

'''
Functions for reading in data and processing
'''

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
       # print("ncols:" , ncols)
        nrows = int(infile.readline().split()[1])
     #   print("nrows: ", nrows)
        xllcorner = float(infile.readline().split()[1])
       # print ("xllcorner: ", xllcorner)
        yllcorner = float(infile.readline().split()[1])
      #  print ("yllcorner: ", yllcorner)
        cellsize = float(infile.readline().split()[1])
      #  print("Cell size: ", cellsize)
        nodata_value = int(infile.readline().split()[1])
      #  print ("NoDataValues represented as: ", nodata_value)
        
    # Create an array of latitude and longitude values using the lower left x and y coordinates, 
    # the ncols and nrows and half of the cellsize (to get the mid point of each cell)
    latitude = yllcorner + (cellsize/2) * np.arange(nrows)
    longitude = xllcorner + (cellsize/2) * np.arange(ncols)
    
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


def df_to_gdf (aoi_fp, df, df_crs):
    """
    Converts a dataframe into a geodataframe storing x,y values as geometry points.
    Only keeps rows in the dataframe which are found within an area of interest.  
    : param aoi: A filepath to the area of interest stored as a polygon.
    : param df: A dataframe containing x, y and additional values as columns. 
    : param crs: A (type?) storing the CRS in which the x, y values are stored.    
    : return gdf: A geodataframe version of the data. 
    """
    start = time.time()
   
    # Import the area of interest
    aoi = read_file(aoi_fp)
    
    # Check if the the CRS of the AOI matches the dataframe; convert if not.
    if aoi.crs == df_crs:
        print ("AOI projection matches dataframe")
    else:
        aoi =aoi.to_crs(df_crs)
        print ("AOI projection converted to match dataframe")
        
    # Create a polgyon out ot the Area of interest
    poly = Polygon(aoi.loc[0, 'geometry'])
    # Add column to dataframe specifying whether each row's geometry intersects the AOI
    df["InAoi"] = df.apply(lambda row: poly.intersects(Point(row["x"], row["y"])), axis = 1)
    # Keep only those rows which are within the AOI
    df = df[df.InAoi == True]
    print ("Dataframe cropped to AOI")
    # Store the geometry of those rows by combining their X and Y coordinates
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    # Convert those positions into a geodataframe, alongside their data values.
    gdf = GeoDataFrame(df[['slope', 'elevation']], crs = df_crs, geometry=geometry)
    print ("Geodataframe created")
    end = time.time()
    print("Time elapsed:" ,round(((end-start)/60),2) , "minutes" )
    return gdf

def create_binned_variable (dataframe, original_variable, new_variable, bins, labels):
    """
    Creates column in dataframe which splits a continuous variables into bins.
    : param dataframe: Datafame of interest.
    : param original_variable: String containing the name of the column to split into bins. 
    : param new_variable: String containing the name of the new column containing bins.
    : param bins: List containing the bins to split the variable into in.
    : param labels: List containing the labels to assign to the bins 
    : return dataframe: Dataframe containing the new column with binned variable. 
    """
    dataframe[new_variable] = pd.cut(dataframe[original_variable], bins = bins, labels = labels)
    return dataframe

def plot_df (df):
    '''
    Converts a dataframe into a geodataframe and plots it.
    : param df: A dataframe containing and x and y column containing coordinates.
    : return gdf.plot() : A plot of the input dataframe
    '''
    # Check location of samples
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    # Convert those positions into a geodataframe
    gdf = GeoDataFrame(df,  geometry=geometry)
    return gdf.plot()

# USING EUCLIDEAN DISTANCE FUNCTION FROM SCIKITLEARN INSTEAD
#def find_dists (sample):
#    """
#    Finds distance between each point in a dataframe and another.
#    : param sample: dataframe containing x and y coordinates.
#    : return mat: A matrix containing pairwise distances.
#    """
#    mat = []
#    for i,j in zip(sample['x'],sample['y']):
#        k = []
#        for l,m in zip(sample['x'],sample['y']):
#            k.append(math.hypot(i - l, j - m))
#            mat.append(k)
#    mat = np.array(mat)
#    return mat

def get_value_from_closest_point(input_df, row_number, df_of_interest, value_of_interest):
    """ 
    Assigns a value to each row in a dataframe based on finding the value of the point in 
    another dataframe which is geographically closest to it. 
    : param input_df: Datafame containing rows of X, Y coordinates.
    : param row_number: Row in input_df to which the function is being applied.
    : df_of_interest: Dataframe containing rows of X, Y coordinates alongside value_of_interest
    : value_of_intersest: String with name of variable to be extracted from df_of_interest.
    : return : A value relating to the value_of_interest that is added to the input_df
    """
    # Find the distance between 
    dists = euclidean_distances(input_df.iloc[[row_number]][['x', 'y']], df_of_interest[['x', 'y']])
    # 
    return  df_of_interest.iloc[[dists.argmin()]][value_of_interest].values[0]

# NOT CURRENTLY USED
#def convertCoords(row, inProj, outProj):
#    '''
#    : param row: A row in a dataframe, containing x and y columns with coordinates, which the function will be applied to using apply.
#    : param inProj: The initial projection of the row's coordinates.
#    : param outProj: The desiredm output projection of the row's coordinates.
#    '''
#    x2,y2 = pyproj.transform(inProj,outProj,row['x'],row['y'])
#    return pd.Series({'newLong':x2,'newLat':y2})

'''
Functions for sampling
'''


def find_near_neighbours (df, min_dist, max_dist, n_close_points, print_preference):
    """
    Adds a column to dataframe containing rows of X, Y coordinates specifying the number of 
    other points in the dataframe which are within a specified distance of each x, y coordinate. 
    : param df: A dataframe with X and Y coordinates stored as columns (in BNG projection)
    : param dist_min: The minimum distance apart which points may be from one another
    : param dist_max: The maximum distance apart which points may be from one another
    : return new_sample_df:  
    """
    # Find the distance between each pair of points in the sample.
    dists = euclidean_distances(df[['x', 'y']], df[['x', 'y']])
    # For each sample point, find the number of points within a distance of it.
    df['close_points'] = df.apply(lambda row:(( dists[row.name]>= min_dist) & ( dists[row.name] < max_dist)).sum(), axis = 1)   
    # Calculate the number of rows in the df without the minimum number of close points.
    close_points = df.loc[df.close_points < n_close_points, 'close_points'].count()
    # Option to print a statement counting the number of points still without the necessary number of neighbours.
    if print_preference == 'Update Progress':
        print(f"Points without {n_close_points} neighbours within {min_dist}: {max_dist}m = {close_points}.")
    return df


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
    # Delete the close points column (so it can be recreated)
    new_sample_df = new_sample_df.drop(['close_points'], axis=1)
    return new_sample_df


def resample_prioritise_new_points (sample_df, original_df, n_close_points):
    """
    Removes all points from a dataframe which were new samples and  which have less than a specified number of points close to them.
    For each row which is removed, randomly selects a row from the  original dataframe which has the same
    'Slope/Elevation' category as the removed row. 
    If there are no such points:
        Then removes one of the original sample points which have less than the specified near neighbour number.
    Join the newly sampled rows back onto the sample dataframe.
    : param sample_df: Dataframe containing sample.
    : param original_df: Dataframe from which the sample was drawn.
    : param n_close_points: Number of points required by user to be 'close' to each point in the sample. 
    : return new_sample_df:  Dataframe containing new sample of same size as input sample_df 
    """
    # If there are any new points with not enough near neighbours then resample these
    if len(sample_df.loc[(sample_df['close_points'] < n_close_points) & (sample_df['origin'] == 'new_point')]) > 0:
        # Keep only those points which have > n_close_points close to them and are NEW
        new_sample_df = sample_df.loc[((sample_df['close_points'] >= n_close_points) & (sample_df['origin'] == 'new_point'))|(sample_df['origin'] == 'original_point')]
        # Create a list of the 'Slope/Elevation values of the points which are removed from the dataframe
        # And select new points which meet the same criteria. 
        criteria = sample_df.loc[(sample_df['close_points'] < n_close_points) & (sample_df['origin'] == 'new_point'), 'Slope/Elevation']
        for i in range(0,len(criteria)):
                # For each of these create a subset of df meeting criteria
                df = original_df.loc[original_df['Slope/Elevation'] == criteria.iloc[i]]
                # Randomly sample one row from those available
                row_to_add = df.sample(n=1)
                row_to_add['origin'] = 'new_point'
                # Add it to dataframe
                new_sample_df = new_sample_df.append(row_to_add, sort = True).reset_index(drop = True)
        # Delete the close points column (so it can be recreated)
        new_sample_df = new_sample_df.drop(['close_points'], axis=1)
  
    # If there are no new points which dont have enough new neighbours, then replace one of the origina;
    # points with another with same slope/elevation criteria.
    else :
        # Randomly select a row with no neighbours, by proxy this will be an old point 
        row_to_remove = sample_df.loc[(sample_df['close_points'] < n_close_points)].copy().sample(n=1)
        # Drop from dataframe, using the index 
        sample_df = sample_df.drop(row_to_remove.index.values.astype(int)[0]).copy()
        # Find the slope/elevation criteria of the row removes and choose a similar row to replace it.
        criteria = row_to_remove['Slope/Elevation']
        row_to_add = original_df.loc[original_df['Slope/Elevation'] == criteria.iloc[0]].copy().sample(n=1)
        row_to_add['origin'] = 'new_point'
        # Add it
        new_sample_df = sample_df.append(row_to_add, sort = True).reset_index(drop = True)
        # Delete the close points column (so it can be recreated)
        new_sample_df = new_sample_df.drop(['close_points'], axis=1)
    return new_sample_df



def create_df_sample (df, sample_constraints, print_preference):
    '''
    Creates a sample from a dataframe of coordinates, according to requirements that the sample should
    have the same distribution of slope and elevation values as the original dataframe and that each point 
    should be within a certain distance of at least one other - as specified in sample_constraints.
    : param df: A dataframe containing x and y coordinates as column from which a sample should be taken.
    : param sample_constraints: A dictionary containing constraints for the sampling procedure. 
    : return sample: A dataframe containing containing a sample of the input dataframe sampled according to sample_constraints.
    '''
    start = time.time()
    # Take a sample from the dataframe that matches the proportional split between slope and elevation in the whole AOI
    sample = df.groupby(['Elevation_cuts', 'Slope_cuts'], as_index=False).apply(lambda x: x.sample (frac = sample_constraints['n_samples']/len(df))).reset_index(drop=True)
    # For each point in the sample, find the number of neighbours it has within a range between min_dist and max_dist
    sample = find_near_neighbours(sample, sample_constraints['min_dist'], sample_constraints['max_dist'], sample_constraints['n_close_points'], print_preference)
    # If 0 rows have less than the requirements for n_close_points then sampling is done.
    # Else, the dataset is resampled until this condition is met.
    done = 'Not Done'
    counter = 0
    if sample.loc[sample.close_points <= sample_constraints['n_close_points'], 'close_points'].count() == 0:
        print(f"Sampling complete after 0 resamples within {round(((time.time()-start)/60),2)} minutes.")
    else:     
        while done != 'Done':
            # Create a coutner to record how many iterations were needed.
            counter = counter + 1
            # Resample the dataset, removing any points without sufficient near neighbours
            # and replacing them with a point with the same slope/elevation profile from the original dataset .
            # Recount the near neighbours to each point.
            sample = resample_far_points (sample, df, sample_constraints['n_close_points'])
            sample = find_near_neighbours (sample, sample_constraints['min_dist'], sample_constraints['max_dist'], sample_constraints['n_close_points'], print_preference)
            # If 0 rows have less than the requirements for n_close_points then sampling is done.
            # Else, the dataset is returned for resampling.
            if sample.loc[sample.close_points <= sample_constraints['n_close_points'], 'close_points'].count()== 0:
                end = time.time()
                print(f"Sampling complete after {counter} resamples within {round(((end-start)/60),2)} minutes.")
                done = 'Done'
    return sample


def find_area_of_rectangle (coordinates):
    """
    Finds the area of the rectangle formed by 4 sets of British National Grid coordinates.
    : param bb_coordinates: A 2D array with X coordinates in first column, and Y in second
    : return area: A
    """
    df = pd.DataFrame({'x': coordinates[:,0], 'y': coordinates[:,1]})
    # Find the distance between the last coordinate and all of the rest. 
    dists = euclidean_distances(df.iloc[[3]][['x', 'y']], df.iloc[:3][['x', 'y']])[0].tolist()
    # Keep only the two smallest distances, corresponding to the length and height of the square.
    dists.remove(max(dists))
    # Find the area as length * height.
    area = dists[0] * dists[1]
    return area
    
def run_sampling (df, n, sample_constraints, print_preference):
    '''
    Samples a dataframe of coordinates, according to requirements that the sample should
    have the same distribution of slope and elevation values as the original dataframe and that each point 
    should be within a certain distance of at least one other - as specified in sample_constraints.
    
    Repeats the sampling process n times, each time assessesing the areal coverage of the sample.
    The final sample is that whose points covers the smallest area.
    
    : param df:  A dataframe containing x and y coordinates as column from which a sample should be taken.
    : param n: An integer representing the number of times sampling should be repeated to attempt to compress the sample area.
    : param sample_constraints: A dictionary containing constraints for the sampling procedure. 
    : return best_sample: A dataframe containing a sample of the input dataframe sampled according to sample_constraints.
    '''
    # Set up bounding box with an area that should be greater than any created. 
    best_bb_area = 1000000000000000000000
    # Repeat n times the sampling process from create_df_sample.
    # Each time find the area of the smallest rectangle which all the sample points fit within.
    # If area is greater than that found in previous iterations, then dispose of the sample and try again.
    # If it is smaller then keep this sample stored as the best_sample
    # At the end return the most compact sample found over the n iterations.
    counter = 0
    while counter <n:
        print ("Sample: " + str(counter))
        sample = funcs.create_df_sample(df, sample_constraints, print_preference)
        sample_bb = minimum_bounding_rectangle (sample)
        bb_area = find_area_of_rectangle (sample_bb)
        if bb_area < best_bb_area:
            print(f"Sample covers the smallest area so far ({str(round(bb_area/1000000,2))} km^2).")
            best_sample = sample
            best_bb_area = bb_area
        else:
            print(f"Sample covers a bigger area than previous samples ({str(round(bb_area/1000000,2))} km^2).")
        print ("--------------------------------------------")
        counter = counter +1
        
    print(f"Sampling complete after {n} iterations, with samples covering {str(round(best_bb_area/1000000,2))} km^2.")
    return best_sample



def interactive_sample_plot (sample, aoi_fp, output_map_fp):
    '''
    Creates and saves to file a moveable map which displays the locations of the sample points, 
    alongside the outline of the area of interest.
    :param sample: Dataframe containing x and y coordinates.
    :param aoi_fp: Filepath to a shapefile containing the AOI.
    :param output_map_fp: Filepath to the location where the map should be stored. 
    : return NULL
    '''
    # Convert the CRS of the sample dataframe (by first converting it to a geodataframe)  
    geometry = [Point(xy) for xy in zip(sample['x'], sample['y'])]
    gdf = GeoDataFrame(sample, crs={'init': 'epsg:27700'} , geometry=geometry)
    gdf = gdf.to_crs({'init': 'epsg:4326'})
    reprojected_sample = pd.DataFrame({'x': gdf.centroid.map(lambda p: p.x), 'y':gdf.centroid.map(lambda p: p.y)})
    
    # Create a Map instance
    # Set the map centred on a locaiton derived as the midpoint of the samples
    m = folium.Map(location=[sum(reprojected_sample['y'])/len(reprojected_sample['y']), sum(reprojected_sample['x'])/len(reprojected_sample['x'])], 
                             tiles = 'cartodbpositron',zoom_start=14, control_scale=True)
    
    # Read in the aoi and reproject it to WGS84 (Folium only plots in WGS84)
    aoi= read_file(aoi_fp).to_crs(epsg=4326)
    # Create a Geo-id (unique identifier for each row) which Folium requires.
    aoi['geoid'] = aoi.index.astype(str)
    # Select data needed
    aoi = aoi[['geoid',  'geometry']]
    # Plot data
    folium.Choropleth(
            geo_data=aoi, fill_opacity = 0.1, fill_color='YlGn', ).add_to(m)
    
    # Add the sample points to the map as circles.
    # add a popup which specifies their location
    for i in range(0,len(reprojected_sample)):
        folium.CircleMarker([reprojected_sample['y'].iloc[i], reprojected_sample['x'].iloc[i]], radius = 4,color="#007849",fill_color="#007849",
                            popup=f"Latitude: {str(round(reprojected_sample['y'].iloc[i],5 ))}, Longitude: {str(round(reprojected_sample['x'].iloc[i],5 ))}.").add_to(m)
   


    # Save map
    m.save(output_map_fp)
    
def interactive_resample_plot (sample, aoi_fp, output_map_fp):
    '''
    Creates and saves to file a moveable map which displays the locations of the sample points, 
    alongside the outline of the area of interest.
    Colours the points so that original sample poitns and new sample points can be differentiated.
    :param sample: Dataframe containing x and y coordinates.
    :param aoi_fp: Filepath to a shapefile containing the AOI.
    :param output_map_fp: Filepath to the location where the map should be stored. 
    : return NULL
    '''
    # Convert the CRS of the sample dataframe (by first converting it to a geodataframe)  
    geometry = [Point(xy) for xy in zip(sample['x'], sample['y'])]
    gdf = GeoDataFrame(sample, crs={'init': 'epsg:27700'} , geometry=geometry)
    gdf = gdf.to_crs({'init': 'epsg:4326'})
    reprojected_sample = pd.DataFrame({'x': gdf.centroid.map(lambda p: p.x), 'y':gdf.centroid.map(lambda p: p.y), 'origin' : gdf['origin']})
    
    # Create a Map instance
    # Set the map centred on a locaiton derived as the midpoint of the samples
    m = folium.Map(location=[sum(reprojected_sample['y'])/len(reprojected_sample['y']), sum(reprojected_sample['x'])/len(reprojected_sample['x'])], 
                             tiles = 'cartodbpositron',zoom_start=14, control_scale=True)
    
    # Read in the aoi and reproject it to WGS84 (Folium only plots in WGS84)
    aoi= read_file(aoi_fp).to_crs(epsg=4326)
    # Create a Geo-id (unique identifier for each row) which Folium requires.
    aoi['geoid'] = aoi.index.astype(str)
    # Select data needed
    aoi = aoi[['geoid',  'geometry']]
    # Plot data
    folium.Choropleth(
            geo_data=aoi, fill_opacity = 0.1, fill_color='YlGn', ).add_to(m)
    
    # Create seperate dataframes containing new and old sample points
    new = reprojected_sample.loc[reprojected_sample['origin'] == 'new_point']
    old = reprojected_sample.loc[reprojected_sample['origin'] == 'original_point']
    
    # Add the sample points to the map as circles.
    # add a popup which specifies their location
    for i in range(0,len(old)):
        folium.CircleMarker([old['y'].iloc[i], old['x'].iloc[i]], radius = 4,color="#007849",fill_color="#007849",
                            popup=f"Latitude: {str(round(reprojected_sample['y'].iloc[i],5 ))}, Longitude: {str(round(reprojected_sample['x'].iloc[i],5 ))}.").add_to(m)
   

    for i in range(0,len(new)):
        folium.CircleMarker([new['y'].iloc[i], new['x'].iloc[i]], radius = 4,color="black",fill_color="black",
                            popup=f"Latitude: {str(round(reprojected_sample['y'].iloc[i],5 ))}, Longitude: {str(round(reprojected_sample['x'].iloc[i],5 ))}.").add_to(m)
    # Save map
    m.save(output_map_fp)