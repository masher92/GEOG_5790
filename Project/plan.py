import rasterio

# 1. Read in a shapefile of the area of interest

## 1. Read in DTM

## Trim the DTM to the area of interest

## 2. Extract slope and elevation from the DTM


## 3. Define n number of sample points to use
n = 100 

## 4. Run clustering algorithm to organise all the pixels into N groups based on the  metrics used.

## 5. Pick locations within each of these groups
# Could try to minimise distance between sample points
# or to roads/ paths
# 


# To use roads -
# need to build a buffer zone around the roads in which the points have to fall


# http://www.guilles.website/2018/06/12/tutorial-exploring-raster-and-vector-geographic-data-with-rasterio-and-geopandas/
# e.g.
roads = geopandas.read_file()
# Analyse data
print ("Number of features in roads file: ", len (roads))


wpgt_file = "E:/Msc/Dissertation/Code/Data/Generated/Humberstone_slope_dd.tif"
wpgt_r = rasterio.open(wpgt_file)
wpgt = wpgt_r.read()
