# Import all functions required within the functions
# These need to be imported in here to execute functions from another file.
import time
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
import math
from shapely.geometry import Point, Polygon
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
    latitude = yllcorner + cellsize * np.arange(nrows)
    longitude = xllcorner + cellsize * np.arange(ncols)
    
    # Load the data values (excluding the first 6 rows containing the descriptive information)
    value = np.loadtxt(filename, skiprows=6)
   # value = np.genfromtxt(filename, invalid_raise = False)
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


def df_to_gdf (aoi, df, df_crs):
    """
    Converts a dataframe into a geodataframe storing x,y values as geometry points.
    Only keeps rows in the dataframe which are found within an area of interest.  
    : param aoi: A shapefile containing the area of interest as a polygon.
    : param df: A dataframe containing x, y and additional values as columns. 
    : param crs: A (type?) storing the CRS in which the x, y values are stored.    
    : return gdf: A geodataframe version of the data. 
    """

    start = time.time()
   
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

def get_value_from_closest_point(input_df, row_number, df_of_interest, value_of_interest):
    """ 
    Assigns a value to each row in a dataframe based on finding the value of the point in 
    another dataframe which is geographically closest to it. 
    : param input_df: Datafame containing rows of X, Y coordinates.
    : param row_number: Row in input_df to which the function is being applied.
    : df_of_interest: Dataframe containing rows of X, Y coordinates alongside value_of_interest
    : value_of_interset: String with name of variable to be extracted from df_of_interest.
    """
    dists = euclidean_distances(input_df.iloc[[row_number]][['x', 'y']], df_of_interest[['x', 'y']])
    #dists = euclidean_distances(pdp.iloc[[row_number]]['geometry'], df_of_interest[['x', 'y']])
    return  df_of_interest.iloc[[dists.argmin()]][value_of_interest].values[0]

def convertCoords(row):
    x2,y2 = pyproj.transform(input_crs,output_crs,row['x'],row['y'])
   # return pd.Series({'newLong':x2,'newLat':y2})
   # to run
      #df = df.join(df.apply(convertCoords, axis=1))
    return pd.Series({'newLong':x2,'newLat':y2})


def find_near_neighbours (df, min_dist, max_dist ):
    """
    Adds a column to dataframe containing rows of X, Y coordinates specifying the number of 
    other points in the dataframe which are within a specified distance of each x, y coordinate. 
    : param df: A dataframe with X and Y coordinates stored as columns (in BNG projection)
    : param dist_min: The minimum distance apart which points may be from one another
    : param dist_max: The maximum distance apart which points may be from one another
    : return new_sample_df:  
    """
    # Find the distance between each pair of points in the sample
    dists = euclidean_distances(df[['x', 'y']], df[['x', 'y']])
    # For each sample point, find the number of points within a distance of it.
    df['close_points'] = df.apply(lambda row:(( dists[row.name]>= min_dist) & ( dists[row.name] < max_dist)).sum(), axis = 1)   
    # Check numbers
    close_points = df.loc[df.close_points < n_close_points, 'close_points'].count()
    #print("Number points without", n_close_points, "neighbours within", dist_min ,df.loc[df.close_points <= n_close_points, 'close_points'].count())
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
       # print (i)
    # Delete the close points column (so it can be recreated)
    new_sample_df = new_sample_df.drop(['close_points'], axis=1)
    return new_sample_df

def resample_far_points2 (sample_df, original_df, n_close_points):
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
    new_sample_df = sample_df.loc[((sample_df['close_points'] >= n_close_points) & (sample_df['origin'] == 'new_point'))|(sample_df['origin'] == 'original_point')]
    # Create a list of the 'Slope/Elevation values of the points which are removed from the dataframe
    criteria = sample_df.loc[(sample_df['close_points'] < n_close_points) & (sample_df['origin'] == 'new_point'), 'Slope/Elevation']
    if len(criteria) > 0 :
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
    else :
        row_to_remove = sample_df.loc[(sample_df['close_points'] < n_close_points) & (sample_df['origin'] == 'original_point')].sample(n=1)
        criteria = row_to_remove = row_to_remove['Slope/Elevation']
        # Choose a new row to add
        df = original_df.loc[original_df['Slope/Elevation'] == criteria.iloc[0]].sample(n=1)
        
        print("no")
        
    return new_sample_df

def create_df_sample (df, min_dist, max_dist, n_samples, n_close_points):
    start = time.time()
    # Take a sample from the dataframe that matches the proportional split between slope and elevation in the whole AOI
    sample = df.groupby(['Elevation_cuts', 'Slope_cuts'], as_index=False).apply(lambda x: x.sample (frac = n_samples/len(df))).reset_index(drop=True)
    # For each point in the sample, find the number of neighbours it has within a range between min_dist and max_dist
    sample = find_near_neighbours(sample, min_dist, max_dist)
    # FUnctiona lso adds the close points column on 
    # If this sample contains no points which do not have a neighbour within Xm then say the process is done
    done = 'Not Done'
    # Count the close_points value for each row.
    if sample.loc[sample.close_points <= n_close_points, 'close_points'].count() == 0:
        print("DONE")
    # Otherwise,  
    else:
        while done != 'Done':
        # Check whether it contains any far points
            sample = resample_far_points (sample,df, n_close_points)
            sample = find_near_neighbours (sample, min_dist, max_dist)
    #        print(sample.loc[sample.close_points== 0, 'close_points'].count())
            # IF any rows in dataframe have less than specified number of close points then resample
            if sample.loc[sample.close_points <= n_close_points, 'close_points'].count()> 0:
                print("Resampling")
            else:
                print ("Sampling complete")
                done = 'Done'
        end = time.time()
        print("time elapsed:" ,round(((end-start)/60),2) , "minutes" )
        
        
    # Check if sample fits the distribution
    return sample