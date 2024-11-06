import numpy as np

from mosaic_algorithms.auxiliar_functions.polygon_functions.interpm_gptmini import interpm


def interppolygon(roi0):
    """
    This function interpolates a polygon defined by longitude and latitude
    points. The interpolation distance is defined according to the minimum
    Euclidean distance between the points that enclose the polygon.

    Usage: roi = interppolygon(roi0)

    Input:
      roi0: A Nx2 numpy array where each row represents a point in 2D space,
             typically [longitude, latitude].

    Output:
      roi: Updated roi with interpolated coordinates.
    """

    # Initialize variables to store longitude and latitude from the polygon
    lon = roi0[:, 0]
    lat = roi0[:, 1]
    epsilon = np.inf  # Initialize epsilon to infinity for minimum distance calculation

    # Loop through each pair of points to find the minimum non-zero distance
    for i in range(len(lon) - 1):
        p1 = np.array([lon[i], lat[i]])  # Current point
        p2 = np.array([lon[i + 1], lat[i + 1]])  # Next point
        dist = np.linalg.norm(p2 - p1)  # Calculate Euclidean distance between points
        if dist == 0:
            continue  # Skip if points are identical
        if dist < epsilon:
            epsilon = dist  # Update minimum distance

    # Find number of regions of polygon (NaN entries)
    indnan = np.where(np.isnan(roi0[:, 0]))[0]
    newlat = []  # Initialize new latitude array
    newlon = []  # Initialize new longitude array

    if indnan.size > 0:
        indnan = np.append(indnan, roi0.shape[0])  # Add end index
        from_idx = 0
        for to_idx in indnan:
            # Perform great circles interpolation of the latitude and longitude
            # based on the minimum distance found
            latd = lat[from_idx:to_idx]
            lond = lon[from_idx:to_idx]
            auxlat, auxlon = interpm(latd, lond, int(np.ceil(epsilon / 2)), 'gc')
            newlat.extend(auxlat)
            newlon.extend(auxlon)
            newlat.append(np.nan)  # Add NaN as separator
            newlon.append(np.nan)  # Add NaN as separator
            from_idx = to_idx + 1
    else:
        # Perform great circles interpolation of the latitude and longitude
        # based on the minimum distance found
        newlat, newlon = interpm(lat, lon, int(np.ceil(epsilon / 2)), 'gc')

    # Update the roi array with the interpolated latitude and longitude values
    roi = np.zeros((len(newlat), 2))  # Initialize roi array
    roi[:, 0] = newlon  # Set interpolated longitudes
    roi[:, 1] = newlat  # Set interpolated latitudes

    # Note: Sorting coordinates in clockwise order is not implemented as the original
    # MATLAB code indicates it is commented out. If needed, implement sortcw functionality.

    return roi

# Note: The 'interpm' function should be defined elsewhere in your code,
# corresponding to the MATLAB version that performs the great circle interpolation.
