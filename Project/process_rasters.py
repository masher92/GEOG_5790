import numpy
from rasterio.plot import show
import rasterio as rio
#import rastertodataframe
from rastertodataframe import raster_to_dataframe
import numpy.core.multiarray as multiarray

# Read in slope file
humberstone_slope = rio.open("E:/Msc/Dissertation/Code/Data/Generated/Humberstone_slope_dd.tif")
#show((humberstone_slope, 1), cmap='Reds')
show(humberstone_slope)


band1 = humberstone_slope.read(1)
type(band1)
band1.dtype
 

# Read in slope file
slope = rio.open("E:/Msc/Dissertation/Code/Data/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif")
show(slope, cmap = 'Reds')

# Extract all image pixels (no vector).
df = raster_to_dataframe("E:/Msc/Dissertation/Code/Data/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif")

                         'E:/Msc/Dissertation/Code/Data/Input/Site_AOIs/Humberstone_AOI.shp')

# Extract only pixels the vector touches and include the vector metadata.
#df = raster_to_dataframe(raster_path, vector_path=vector_path)



