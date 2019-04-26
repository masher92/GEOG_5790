import rasterio
from rasterio.plot import show
import geopandas as gpd

import numpy as np
import os
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio.plot import plotting_extent
from rasterio.mask import mask
from shapely.geometry import mapping
import geopandas as gpd
plt.ion()

import seaborn as sns

# Open the DTM:
dtm = rasterio.open("E:/Msc/Dissertation/Code/Data/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif")
show(dtm)
# Check the crs
print ("CRS of DTM: ", dtm.crs)

# Open crop extent (your study area extent boundary)
aoi = gpd.read_file('E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')
# Check the crs
print ("CRS of AOI: ", aoi.crs)

# Plot the AOI - can this be changed so there is no fill
fig, ax = plt.subplots(figsize=(6, 6))
aoi.plot(ax=ax)
ax.set_title("Humberstone AOI",
             fontsize=16)

# Convert the AOI to a GeoJSON
aoi_geojson = mapping(aoi['geometry'][0])
aoi_geojson

# Crop
with rio.open("E:/Msc/Dissertation/Code/Data/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif") as dtm:
    slope_crop, slope_crop_affine = mask(dtm,
                                                 [aoi_geojson],
                                                 crop=True)
# Create spatial plotting extent for the cropped layer
slope_extent = plotting_extent(slope_crop[0], slope_crop_affine)


# Plot your data - have we lost the slope information?
fig, ax = plt.subplots(figsize=(6, 4))
ax.imshow(slope_crop[0],
          extent=slope_extent)
ax.set_title("Humberstone DTM")
ax.set_axis_off()
show(slope_crop)

humberstone_slope.read(1)





