from math import sin, cos, radians, degrees, acos

from shapely.geometry import Point


def calc_dist(lat_a, long_a, lat_b, long_b):
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    resToMile = degrees(acos(distance)) * 69.09
    resToMt = resToMile / 0.00062137119223733
    return resToMt#


point1 = humberstone['coords.x1'].iloc[0]
point1 = humberstone[['coords.x1', 'coords.x2']].iloc[0]

calc_dist (humberstone['coords.x1'].iloc[0], humberstone['coords.x2'].iloc[0],
            humberstone['coords.x1'].iloc[10], humberstone['coords.x2'].iloc[10])


from django.contrib.gis.geos import Point
p1 = Point(37.2676483,-6.9273579)
p2 = Point(37.2653293,-6.9249401)
distance = p1.distance(p2)
distance_in_km = distance * 100


# Read in ascii
import numpy as np
x = np.genfromtxt("E:/Msc/Dissertation/Code/Data/Generated/humberstone_slope_dd.asc", dtype=None)
print(x[0])

my_asc = "E:/Msc/Dissertation/Code/Data/Generated/humberstone_slope_dd.asc"

humberstone = pd.read_csv("E:/Msc/Dissertation/Code/Data/Generated/humberstone_slope_dd.asc") 
lines = file("E:/Msc/Dissertation/Code/Data/Generated/humberstone_slope_dd.asc").readlines()

    


# From: https://stackoverflow.com/questions/37855316/reading-grd-file-in-python
def read_grd(filename):
    with open(filename) as infile:
        ncols = int(infile.readline().split()[1])
        nrows = int(infile.readline().split()[1])
        xllcorner = float(infile.readline().split()[1])
        yllcorner = float(infile.readline().split()[1])
        cellsize = float(infile.readline().split()[1])
        nodata_value = int(infile.readline().split()[1])
        version = float(infile.readline().split()[1])
    longitude = xllcorner + cellsize * np.arange(ncols)
    latitude = yllcorner + cellsize * np.arange(nrows)
    value = np.loadtxt(filename, skiprows=7)

    return longitude, latitude, value

test = read_grd(my_asc)

import numpy as np
ascii_grid = np.loadtxt(my_asc, skiprows=6)
