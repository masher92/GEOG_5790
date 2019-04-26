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
from shapely.geometry import Point
from geopandas import GeoDataFrame

# From: https://stackoverflow.com/questions/37855316/reading-grd-file-in-python
def read_grd(filename):
    with open(filename) as infile:
        ncols = int(infile.readline().split()[1])
        print(ncols)
        nrows = int(infile.readline().split()[1])
        print(nrows)
        xllcorner = float(infile.readline().split()[1])
        yllcorner = float(infile.readline().split()[1])
        cellsize = float(infile.readline().split()[1])
        print("Cell size: ", cellsize)
        nodata_value = int(infile.readline().split()[1])
        version = float(infile.readline().split()[1])
    longitude = xllcorner + cellsize * np.arange(ncols)
    latitude = yllcorner + cellsize * np.arange(nrows)
    value = np.loadtxt(filename, skiprows=6)
    
    # Convert to dataframe
    df = pd.DataFrame(data=value, index=latitude, columns=longitude)  # 1st row as the column names
    # Unstack into rows and columns
    df = pd.DataFrame(df).stack().rename_axis(['y', 'x']).reset_index(name='slope')
    # Keep only complete cases
    df = df[df.slope != -9999]
    # Add ID
    df['ID'] = range(1, len(df) + 1)
    return df
    #return longitude, latitude, value


def df_to_gdf (df, crs):
    """
    Convert a DataFrame with longitude and latitude columns
    to a GeoDataFrame.
    """
    df = input_df.copy()
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf

# Filepath to ascii
my_asc = "E:/Msc/Dissertation/Code/Data/Generated/humberstone.asc"
my_asc = "E:/Msc/Dissertation/Code/Data/Generated/dales_nidderdale_moorland_line_dtm_5m.asc"

# Read in just the data values from the ASCii
# This skips the header but doesnt keep the information, so we lose the spatial information
ascii_grid = np.loadtxt(my_asc, skiprows=6)

# Read into dataframe
slope = read_grd(my_asc)

#### Convert to gdf
slope_gdf = df_to_gdf (slope, {'init': 'epsg:27700'} )

# Plot
slope_gdf.plot(column = 'slope', cmap='OrRd')

# Convert to WGS84
slope_gdf = slope_gdf.to_crs = {'init' :"+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"}
#slope_gdf = slope_gdf.to_crs({'init': 'epsg:3395'})
slope_gdf.crs


# Outline
aoi = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')
aoi.plot(cmap='Greys',ax=ax, alpha=.5)

# Plot the data
fig, ax = plt.subplots(figsize=(12, 8))
aoi.plot(alpha=.5,
                         ax=ax)
aoi.plot(cmap='Greys',
                       ax=ax,
                       alpha=.5)
slope_gdf.plot(ax=ax)
plt.axis('equal')
ax.set_axis_off()
plt.show()


# CLip by AOI
pointInPolys = sjoin(slope_gdf, aoi, how='left')
pointInPolys.head()

pip_mask = data.within(aoi.loc[0, 'geometry'])
pip_data = data.loc[pip_mask]