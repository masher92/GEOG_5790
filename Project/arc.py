import arcpy
#arcpy.RasterToASCII_conversion("E:/Msc/Dissertation/Code/Data/Generated/Humberstone_slope_dd.tif", "E:/Msc/Dissertation/Code/Data/Generated/Humberstone.asc")
#print ("Done")

arcpy.RasterToASCII_conversion("E:/Msc/Dissertation/Code/Data/Input/DTM/Dales_Nidderdale_Moorland_Line_DTM_5m.tif",
                               "E:/Msc/Dissertation/Code/Data/Generated/Dales_Nidderdale_Moorland_Line_DTM_5m.asc")
print ("Done")
