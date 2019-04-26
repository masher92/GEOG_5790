# Import libraries 
import pandas as pd 
import matplotlib.pyplot as plt

# Read data 
humberstone = pd.read_csv("E:/Msc/Dissertation/Code/Data/Generated/humberstone.csv") 
# Preview the first 5 lines of the loaded data 
humberstone.head()

# Create binned variables, according to user defined groups
humberstone['Slope_cuts'] = pd.cut(humberstone['Slope_5m'], bins=[0, 5, 10,float('Inf')],
           labels=['0-5', '5-10', '30+'])
humberstone['Elevation_cuts'] = pd.cut(humberstone['elevation'], bins=[230, 260, 290, 320, 350, 380, 410, 440],
           labels=['230-260', '260-290', '290-230', '320 - 350', '350-380', '380-410', '410-440'])
# Create bins according to number of bins
#humberstone['Slope_cuts'] =pd.cut(humberstone['Slope_5m'], 5)
#humberstone['Elevation_cuts'] =pd.cut(humberstone['elevation'], 8)

# Take a sample of 1% of the data according to slope or elevation
output = humberstone.groupby('Slope_cuts').apply(lambda x: x.sample (frac=0.01))
output = humberstone.groupby('Elevation_cuts').apply(lambda x: x.sample (frac=0.01))
output = humberstone.groupby(['Elevation_cuts', 'Slope_cuts'], as_index=False).apply(lambda x: x.sample (frac=0.01))
output2 = humberstone.groupby(['Elevation_cuts', 'Slope_cuts']).apply(lambda x: x.sample (frac=0.01))
# Check values in each
output.Elevation_cuts.value_counts()

# Find the number/proportion of pixels in each category (mixing the slope and elevation cats)
count = humberstone.groupby(['Slope_cuts', 'Elevation_cuts'])['Slope_cuts'].count()
count_df = pd.Series.to_frame(count)
count_df['slope_cut'] = list(count.index)
count_df['Proportion'] = (count_df['Slope_cuts']/len(humberstone)) *100
# Series with just proportions
props = pd.Series(count_df['Proportion'])

# Another way allowing creation of the info in a table
tab = humberstone.groupby(['Elevation_cuts', 'Slope_cuts']).size()
tab.unstack()
props.unstack().transpose()

# Plot histogram
humberstone['Slope_5m'].hist(bins = 20)
humberstone['elevation'].hist(bins = 30)
   

# Convert dataframe to a geodataframe
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(humberstone['coords.x1'], humberstone['coords.x2'])]
humberstone2 = humberstone.drop(['coords.x1', 'coords.x2'], axis=1)
crs = {'init': 'epsg:27700'}
gdf = GeoDataFrame(humberstone2, crs=crs, geometry=geometry)

### Plot
# Point DataSource
psource = ColumnDataSource(humberstone)
# Initialize our plot figure
p = figure(title="A map of address points from a Shapefile")
# Add the points to the map from our 'psource' ColumnDataSource -object
p.circle('coords.x1', 'coords.x2', source=psource, color='red', size=10)

# Initialize our figure
p = figure(title="ss")

# Plot grid
p.patches('x', 'y', source=gsource,
         fill_alpha=1.0, line_color="black", line_width=0.05)

# Output filepath
outfp = "E:/Msc/Advanced-Programming/points_map.html"


# Save the map
save(p, outfp)

###------------
import geopandas as gpd
data= gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')
# Re-project to WGS84
data = data.to_crs(epsg=4326)

# Check layer crs definition
print(data.crs)

# Make a selection (only data above 0 and below 1000)
data = data.loc[(data['ASUKKAITA'] > 0) & (data['ASUKKAITA'] <= 1000)]

# Create a Geo-id which is needed by the Folium (it needs to have a unique identifier for each row)
data['geoid'] = data.index.astype(str)

# Select only needed columns
data = data[['geoid',  'geometry']]

# Convert to geojson (not needed for the simple coropleth map!)
#pop_json = data.to_json()

#check data
data.head()


# Create a Map instance
m = folium.Map(location=[60.25, 24.8], tiles = 'cartodbpositron', zoom_start=10, control_scale=True)

# Plot a choropleth map
# Notice: 'geoid' column that we created earlier needs to be assigned always as the first column
folium.Choropleth(
    geo_data=data,
    data=data,
    legend_name= 'Population in Helsinki').add_to(m)

#Show map
m


# Convert points to GeoJson
points_gjson = folium.features.GeoJson(humberstone, name = "Sample points")
# Create a Map instance
m = folium.Map(location=[-1.797, 54], tiles = 'cartodbpositron', zoom_start=10, control_scale=True)

# Create a Map instance
m = folium.Map(location=[54, -1.797],
    zoom_start=12, control_scale=True)
# Convert points to GeoJson
points_gjson = folium.features.GeoJson(humberstone, name = "Sample points")
# Add points to the map instance
points_gjson.add_to(m)

# Alternative syntax for adding points to the map instance
#m.add_child(points_gjson)

# Output filepath
outfp = "E:/Msc/Advanced-Programming/points_map.html"


# Save the map
m.save(outfp)



#---------
# Random sample of 10% of points
random_sample = humberstone.iloc[
    np.random.randint(
        0, 
        len(humberstone), 
        int(len(humberstone) / 1000)
    )
]

# Random Stratified Sampling (100 observations out of 100k)
stratified_sample = list(map(lambda x : humberstone[
    (humberstone['Slope_cuts'] == count.index[x][0]) 
    &
    (humberstone['Elevation_cuts'] == count.index[x][1])
].sample(frac=0.001), range(len(count))))

stratified_sample = pd.concat(stratified_sample)
