# https://www.earthdatascience.org/courses/earth-analytics-python/lidar-raster-data/crop-raster-data-with-shapefile-in-python/

import rasterio as rio
import geopandas as gpd
from shapely.geometry import mapping
from rasterio.mask import mask
from rasterio.plot import plotting_extent
import matplotlib.pyplot as plt

# Open crop extent (your study area extent boundary)
crop_extent = gpd.read_file(
    'E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')

# 
extent_geojson = mapping(crop_extent['geometry'][0])
extent_geojson

print('crop extent crs: ', crop_extent.crs)
#print('lidar crs: ', raster.crs)


with rio.open("E:/Msc/Dissertation/Code/Data/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif") as lidar_chm:
    lidar_chm_crop, lidar_chm_crop_affine = mask(lidar_chm,
                                                 [extent_geojson],
                                                 crop=True)

# Create spatial plotting extent for the cropped layer
lidar_chm_extent = plotting_extent(lidar_chm_crop[0], lidar_chm_crop_affine)


# Plot your data
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(lidar_chm_crop[0],
          extent=lidar_chm_extent,
          cmap='Greys')
ax.set_title("Cropped Raster Dataset")
ax.set_axis_off()


lidar_chm_meta.update({'transform': lidar_chm_crop_affine,
                       'height': lidar_chm_crop.shape[1],
                       'width': lidar_chm_crop.shape[2],
                       'nodata': -999.99})
lidar_chm_meta