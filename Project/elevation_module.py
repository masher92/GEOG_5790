import elevation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
%matplotlib inline
from rasterio.transform import from_bounds, from_origin
from rasterio.warp import reproject, Resampling
import rasterio as rio

bounds = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp').bounds
west, south, east, north = bounds = bounds.loc[0]
dtm = "E:/Msc/Dissertation/Code/Data/Generated/Humberstone_slope_dd.tif"
elevation.clip(bounds=bounds, output=dtm, product='SRTM1')


dem_raster = rio.open("E:/Msc/Dissertation/Code/Data/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif")
src_crs = dem_raster.crs
src_shape = src_height, src_width = dem_raster.shape
src_transform = from_bounds(west, south, east, north, src_width, src_height)
source = dem_raster.read(1)

dst_crs = {'init': 'EPSG:32616'}
dst_transform = from_origin(268000.0, 5207000.0, 250, 250)
dem_array = np.zeros((451, 623))
dem_array[:] = np.nan
         
reproject(source,
          dem_array,
          src_transform=src_transform,
          src_crs=src_crs,
          dst_transform=dst_transform,
          dst_crs=dst_crs,
          resampling=Resampling.bilinear)


try:
    import pycpt
    topocmap = pycpt.load.cmap_from_cptcity_url('wkp/schwarzwald/wiki-schwarzwald-cont.cpt')
except:
    topocmap = 'Spectral_r'

vmin = 180
vmax = 575




         