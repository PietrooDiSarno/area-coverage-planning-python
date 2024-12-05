# Import external modules
import numpy as np
from pyproj import Geod

# Import local modules
from mosaic_algorithms.auxiliar_functions.polygon_functions.interpm_gpt import interpm


def interppolygon(roi0):
    """
    This function interpolates a polygon defined by longitude and latitude
    points. The interpolation distance is defined according to the minimum
    geodesic distance between the points that enclose the polygon.

    Usage:
        roi = interppolygon(roi0)

    Input:
        > roi0: A Nx2 numpy array where each row represents a point in 2D space,
                typically [longitude, latitude]

    Output:
        > roi:  Updated roi with interpolated coordinates
    """

    # Initialize the Geod object for geodesic calculations (WGS84 ellipsoid)
    geod = Geod(ellps='WGS84')

    # Extract longitude and latitude from the input polygon
    lon = roi0[:, 0]
    lat = roi0[:, 1]

    # Initialize epsilon to infinity; it will store the minimum geodesic distance
    epsilon = np.inf

    # Loop through each pair of consecutive points to find the minimum non-zero geodesic distance
    for i in range(len(lon) - 1):
        lon1, lat1 = lon[i], lat[i]         # Current point
        lon2, lat2 = lon[i + 1], lat[i + 1] # Next point

        # Skip if any of the points are NaN (used to separate polygon regions)
        if np.isnan(lon1) or np.isnan(lat1) or np.isnan(lon2) or np.isnan(lat2):
            continue

        # Calculate the geodesic distance between the two points in meters
        _, _, dist = geod.inv(lon1, lat1, lon2, lat2)

        # Skip if the distance is zero (identical points)
        if dist == 0:
            continue

        # Update epsilon if a smaller non-zero distance is found
        if dist < epsilon:
            epsilon = dist

    # Find indices where longitude is NaN to identify separate polygon regions
    indnan = np.where(np.isnan(lon))[0]

    # Initialize lists to store the new interpolated latitude and longitude values
    newlat = []
    newlon = []

    # Process each polygon region separated by NaNs
    if indnan.size > 0:
        # Append the end index to process the last region
        indnan = indnan.tolist()
        indnan.append(len(lon))

        from_idx = 0  # Start index of the current region
        for idx in indnan:
            to_idx = idx  # End index of the current region

            # Extract the latitude and longitude for the current region
            lat_segment = lat[from_idx:to_idx]
            lon_segment = lon[from_idx:to_idx]

            # Perform interpolation for the current region
            auxlat, auxlon = interpm(lat_segment, lon_segment, epsilon / 2)

            # Append the interpolated points to the new lists
            newlat.extend(auxlat.tolist())
            newlon.extend(auxlon.tolist())

            # Append NaN to separate regions
            newlat.append(np.nan)
            newlon.append(np.nan)

            # Update the start index for the next region
            from_idx = idx + 1
    else:
        # If there are no NaNs, process the entire polygon
        newlat, newlon = interpm(lat, lon, epsilon / 2)

    # Convert the lists to numpy arrays
    newlat = np.array(newlat)
    newlon = np.array(newlon)

    # Update the roi array with the interpolated latitude and longitude values
    roi = np.column_stack((newlon, newlat))

    # Optional: Sort coordinates in clockwise order (uncomment if needed)
    # Note: The equivalent of MATLAB's sortcw function would need to be implemented or replaced
    # roi = sortcw(roi)

    return roi
