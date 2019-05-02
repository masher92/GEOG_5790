import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Point

def minimum_bounding_rectangle(df):
    """
    Find the smallest bounding rectangle for a set of points.
    Returns a set of points representing the corners of the bounding box.

    :param df: A dataframe of coordinates stored in X and Y columns
    :value: an nx2 matrix of coordinates
    """
    from scipy.ndimage.interpolation import rotate
    pi2 = np.pi/2.
    
    points = np.array(df[['x', 'y']])
    
    # get the convex hull for the points
    hull_points = points[ConvexHull(points).vertices]

    # calculate edge angles
    edges = np.zeros((len(hull_points)-1, 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    # find rotation matrices
    # XXX both work
    rotations = np.vstack([
        np.cos(angles),
        np.cos(angles-pi2),
        np.cos(angles+pi2),
        np.cos(angles)]).T
#     rotations = np.vstack([
#         np.cos(angles),
#         -np.sin(angles),
#         np.sin(angles),
#         np.cos(angles)]).T
    rotations = rotations.reshape((-1, 2, 2))

    # apply rotations to the hull
    rot_points = np.dot(rotations, hull_points.T)

    # find the bounding points
    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    # find the box with the best area
    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    # return the best box
    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)

    return rval

def two_opt(locations,improvement_threshold):
    """
    Adapted from: https://stackoverflow.com/questions/25585401/travelling-salesman-in-scipy.
    This uses the 2-opt algorithm adapted from https://en.wikipedia.org/wiki/2-opt to calculate
    the optimum order in which to visit a set of coordinates in order to minimise the distance travelled.
    This also is based on the route ending where it started.
    : param locations: Nx2 array containing X and Y coordinates.
    : param improvement_threshold:
    : return route: An array containing the order of index values of df in which sites should be visited.
    """
    # Calculate the euclidian distance in n-space of the route r traversing locations c, ending at the path start.
    path_distance = lambda r,c: np.sum([np.linalg.norm(c[r[p]]-c[r[p-1]]) for p in range(len(r))])
    # Reverse the order of all elements from element i to element k in array r.
    two_opt_swap = lambda r,i,k: np.concatenate((r[0:i],r[k:-len(r)+i-1:-1],r[k+1:len(r)]))
    # Make an array of row numbers corresponding to locations.
    route = np.arange(locations.shape[0]) 
    # Initialize the improvement factor.
    improvement_factor = 1 
    # Calculate the distance of the initial path
    best_distance = path_distance(route,locations) 
    while improvement_factor > improvement_threshold: # If the route is still improving, keep going!
        # Record the distance at the beginning of the loop.
        distance_to_beat = best_distance 
        # From each location except the first and last
        for swap_first in range(1,len(route)-2): 
            # to each of the locations following,
            for swap_last in range(swap_first+1,len(route)): 
                # try reversing the order of these locations
                new_route = two_opt_swap(route,swap_first,swap_last) 
                # and check the total distance with this modification.
                new_distance = path_distance(new_route,locations)
                # If the path distance is an improvement,
                if new_distance < best_distance: 
                    # Make this the accepted best route
                    route = new_route 
                    # and update the distance corresponding to this route.
                    best_distance = new_distance 
         # Calculate how much the route has improved.                    
        improvement_factor = 1 - best_distance/distance_to_beat
    # When the route is no longer improving substantially, stop searching and return the route -->
    return route 
