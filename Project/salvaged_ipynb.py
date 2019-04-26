import bokeh
from bokeh.io import output_notebook, show, reset_output
from bokeh.plotting import figure, output_file, show, save
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource
import geopandas as gpd
# Import markdown
from IPython.core.display import Markdown
#Markdown(open(\"README.md\").read())
#output_notebook(resources=INLINE)

def getPointCoords(row, geom, coord_type):
    #Calculates coordinates ('x' or 'y') of a Point geometry
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y

def getPolyCoords(row, geom, coord_type):
    #\"\"\"Returns the coordinates ('x' or 'y') of edges of a Polygon exterior\"\"\"
    # Parse the exterior of the coordinate
    exterior = row[geom].exterior
    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list( exterior.coords.xy[0] )
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list( exterior.coords.xy[1] )

# Set up the filepaths
points_fp = "E:/Msc/Dissertation/Code/Data/Generated/Humberstone.shp"
aoi_fp = "E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp"
dtm_fp = "E:/Msc/Dissertation/Code/Data/Generated/Humberstone_slope_dd.tif"
# Read the data
points = gpd.read_file(points_fp)
polygon = gpd.read_file(aoi_fp)
# Inspect the data
polygon
polygon['geometry']   
 

# Add a column to the dataframe containing the X and Y coordinates
points['x'] = points.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
points['y'] = points.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

# Add a column to the dataframe containing the X and Y coordinates
polygon['x'] = polygon.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
polygon['y'] = polygon.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)

# Make a copy and drop the geometry column
p_df = points.drop('geometry', axis=1).copy()
polygon_df = polygon.drop('geometry', axis=1).copy()

# See head
p_df.head(2)
polygon_df.head(2)

polygon_df[['x', 'y']]#.head(5)


# Point DataSource
psource = ColumnDataSource(p_df)
gsource = ColumnDataSource(polygon_df)
# What is it?
psource

# Initialize our plot figure
p = figure(title="A map of address points from a Shapefile")
# Add the points to the map from our 'psource' ColumnDataSource -object
p.circle('x', 'y', source=psource, color='red', size=10)

# Initialize our figure
p = figure(title="ss")

# Plot grid
p.patches('x', 'y', source=gsource,
         fill_alpha=1.0, line_color="black", line_width=0.05)

# Output filepath
outfp = "E:/Msc/Advanced-Programming/points_map.html"

# Save the map
save(p, outfp)


import rasterio
from rasterio.plot import show
fp = "E:/Msc/Dissertation/Code/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif"
raster = rasterio.open(fp)

import xarray as xr
import numpy as np
import pandas as pd
import bokeh
print(bokeh.__version__)

import holoviews as hv
import geoviews as gv
import geoviews.feature as gf
import cartopy
from cartopy import crs as ccrs
from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import WMTSTileSource

hv.notebook_extension('bokeh')
tiles = {'OpenMap': WMTSTileSource(url='http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'),
         'ESRI': WMTSTileSource(url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg'),
         'Wikipedia': WMTSTileSource(url='https://maps.wikimedia.org/osm-intl/{Z}/{X}/{Y}@2x.png'),
         'Stamen Toner': STAMEN_TONER}

opts WMTS [width=450 height=250 xaxis=None yaxis=None]
hv.NdLayout({name: gv.WMTS(wmts, extents=(0, -90, 360, 90), crs=ccrs.PlateCarree())
            for name, wmts in tiles.items()}, kdims=['Source']).cols(2)





