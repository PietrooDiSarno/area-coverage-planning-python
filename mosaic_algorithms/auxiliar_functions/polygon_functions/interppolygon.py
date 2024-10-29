import numpy as np
import math
from geopy.distance import geodesic
from mosaic_algorithms.auxiliar_functions.polygon_functions.sortcw import  sortcw

def interppolygon(roi0):
    """
    This function interpolates a polygon defined by longitude and latitude
    points. The interpolation distance is defined according to the minimum
    Euclidean distance between the points that enclose the polygon

    Programmers:  Paula Betriu (UPC/ESEIAAT)
    Date:         1/2024

    Usage:        roi = interppolygon(roi0)

    Input:
      > roi0:     A Nx2 matrix where each row represents a point in 2D space,
                  typically [longitude, latitude]

    Output:
      > roi:      Updated roi with interpolated coordinates
    """

    # Definition of maximum allowable distance
    # Initialize variables to store longitude and latitude from the polygon.
    lon = roi0[:, 0]
    lat = roi0[:, 1]
    epsilon = np.inf  # initialize epsilon to infinity. This will be used to find the minimum distance between points.

    # Loop through each pair of points to find the minimum non-zero distance
    for i in range(len(lon) - 1):
        p1 = np.array([lon[i], lat[i]])  # current point
        p2 = np.array([lon[i + 1], lat[i + 1]])  # next point
        dist = np.linalg.norm(p2 - p1) # calculate Euclidean distance between points
        if dist == 0:
            continue  # skip if points are identical
        if dist < epsilon:
            epsilon = dist  # update minimum distance

    # Find number of regions of polygon
    indnan = np.where(np.isnan(roi0[:, 0]))[0]
    newlat = []
    newlon = []
    if len(indnan) > 0:
        indnan[-1] =  roi0.shape[0] + 1
        from_idx = 1
        for i in range(len(indnan)):
            to = indnan[i] - 1
            # Perform great circles interpolation of the latitude and longitude based
            # on the minimum distance found
            latd = lat[from_idx:to]
            lond = lon[from_idx:to]
            auxlat, auxlon = interpm(latd, lond, math.ceil(epsilon / 2), 'gc')
            newlat.extend(auxlat)
            newlat.append(np.nan)
            newlon.extend(auxlon)
            newlon.append(np.nan)
            from_idx = to + 2
    else:
        # Perform great circles interpolation of the latitude and longitude based
        # on the minimum distance found
        newlat, newlon = interpm(lat, lon, math.ceil(epsilon / 2), 'gc')

    # Update the roi array with the interpolated latitude and longitude values
    roi = np.column_stack((newlon, newlat))

    # Sort coordinates in clockwise order
    # [roi[:, 0], roi[:, 1]] = sortcw(roi[:, 0], roi[:, 1])
    return roi

def interpm(lat, lon, num_points, method):
    """
    Interpolates points along a great circle path.
    """
    from scipy.interpolate import interp1d
    import numpy as np

    if method == 'gc':
        distances = [0]
        for i in range(1, len(lat)):
            distances.append(distances[-1] + geodesic((lat[i-1], lon[i-1]), (lat[i], lon[i])).meters)
        distances = np.array(distances)
        total_distance = distances[-1]
        new_distances = np.linspace(0, total_distance, num_points)
        interp_lat = interp1d(distances, lat, kind='linear')(new_distances)
        interp_lon = interp1d(distances, lon, kind='linear')(new_distances)
        return interp_lat, interp_lon
    else:
        raise ValueError("Unsupported interpolation method")
