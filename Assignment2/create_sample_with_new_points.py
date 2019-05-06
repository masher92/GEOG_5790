'''
Create sample with old points.
'''
# Read in original peat depth sample points. 
pdp = gpd.read_file(peat_depth_samples_fp)

# Convert to a dataframe
pdp_df = pd.DataFrame({'x': pdp.centroid.map(lambda p: p.x), 'y':pdp.centroid.map(lambda p: p.y)})

# Find its slope and elevation values
# Finds the geographic point in the combined_df closest to each of the sample points and
# takes its slope and elevation values. 
pdp_df['slope'] = [funcs.get_value_from_closest_point(pdp_df, row_number, combined_df, 'slope')  for row_number in range(0,len(pdp_df))]
pdp_df['elevation'] = [funcs.get_value_from_closest_point(pdp_df, row_number, combined_df,'elevation')  for row_number in range(0,len(pdp_df))]

# Add binned variables
pdp_df = funcs.create_binned_variable(pdp_df, 'slope', 'Slope_cuts', [0, 5, 10,float('Inf')], ['0-5', '5-10', '30+'])
pdp_df = funcs.create_binned_variable(pdp_df, 'elevation', 'Elevation_cuts', [230, 260, 290, 320, 350, 380, 410, 440], ['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
pdp_df['Slope/Elevation'] = ['Slope:' + x + ', Elevation:' + y for x, y in zip(pdp_df['Slope_cuts'], pdp_df['Elevation_cuts'])]


# Identify some random extra points to add
extra = combined_df.sample(n=150)

# Tag points as to whether they are from the original dataset, or a new point.
pdp_df['origin'] = 'original_point'
extra['origin'] = 'new_point'
        
# Combine to make a first version of a sample.
resample= pdp_df.append(extra, sort = True).reset_index(drop = True)
# Find near neighbours in this first sample
resample = funcs.find_near_neighbours(resample, min_dist, max_dist, n_close_points, 'no_print')

# If all points have enough points near them, then done....
if resample.loc[resample.close_points < n_close_points, 'close_points'].count() == 0 :
   print("Done")
# If not then....resample the bad points 
else:
    done = 'nope'
    while done == 'nope':
        # Conduct resampling and recount, each round involves:
        # First replacing all new points without sufficient near neighbours with others.
        # If there are none, then replace one of the original points with another.
        resample = resample_prioritise_new_points (resample, combined_df, n_close_points)
        resample = funcs.find_near_neighbours (resample, min_dist, max_dist, n_close_points, 'Update Progress')
        # If any rows in dataframe have less than specified number of close points then resample
        if resample.loc[resample.close_points < n_close_points, 'close_points'].count()> 0:
                print("Resampling")
        else:
                print ("Sampling complete")
                done = 'Yup'

# Check location of samples
geometry = [Point(xy) for xy in zip(resample.x, resample.y)]
# Convert those positions into a geodataframe
gdf = GeoDataFrame(resample[['Slope/Elevation', 'origin', 'close_points']],  geometry=geometry)

# Sjow where new points are/
gdf['origin'] =gdf['origin'] .astype('category')
#gdf.plot(column = 'close_points', cmap = 'brg')    
gdf.plot(column = 'origin', cmap = 'brg')    


# Check the distributon of new points compared to old points.
resample['origin'].value_counts()
