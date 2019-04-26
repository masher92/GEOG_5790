import folium
import geopandas as gpd

# Filepaths
fp = 'E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp'

# Read Data
data = gpd.read_file(fp)
ad = humberstone

# Re-project to WGS84
data['geometry'] = data['geometry'].to_crs(epsg=4326)
ad['geometry'] = ad['geometry'].to_crs(epsg=4326)

# Update the CRS of the GeoDataFrame
data.crs = from_epsg(4326)
ad.crs = from_epsg(4326)

# Make a selection (only data above 0 and below 1000)
data = data.ix[(data['ASUKKAITA'] > 0) & (data['ASUKKAITA'] <= 1000)]

# Create a Geo-id which is needed by the Folium (it needs to have a unique identifier for each row)
data['geoid'] = data.index.astype(str)
ad['geoid'] = ad.index.astype(str)

# Select data
data = data[['geoid', 'geometry']]

# Save the file as geojson
jsontxt = data.to_json()

# Create a Clustered map where points are clustered
marker_cluster = folium.MarkerCluster().add_to(map_osm)


# Create Choropleth map where the colors are coming from a column "ASUKKAITA".
# Notice: 'geoid' column that we created earlier needs to be assigned always as the first column
# with threshold_scale we can adjust the class intervals for the values
map_osm.choropleth(geo_str=jsontxt, data=data, columns=['geoid', 'ASUKKAITA'], key_on="feature.id",
                   fill_color='YlOrRd', fill_opacity=0.9, line_opacity=0.2, line_color='white', line_weight=0,
                   threshold_scale=[100, 250, 500, 1000, 2000],
                   legend_name='Population in Helsinki', highlight=False, smooth_factor=1.0)


# Create Address points on top of the map
for idx, row in ad.iterrows():
    # Get lat and lon of points
    lon = row['geometry'].x
    lat = row['geometry'].y

    # Get address information
    address = row['address']
    # Add marker to the map
    folium.RegularPolygonMarker(location=[lat, lon], popup=address, fill_color='#2b8cbe', number_of_sides=6, radius=8).add_to(marker_cluster)

# Save the output
outfp = r'/home/geo/data/pop15.html'
map_osm.save(outfp)