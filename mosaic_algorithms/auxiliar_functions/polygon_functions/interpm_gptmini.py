import numpy as np
from math import radians, degrees, sin, cos, atan2, asin, sqrt


def interpm(latd, lond, spacing, method='gc'):
    """
    Interpolate latitude and longitude using great circle method.

    Parameters:
      latd: List or array of latitudes (degrees).
      lond: List or array of longitudes (degrees).
      spacing: Distance in degrees for interpolation.
      method: Interpolation method; defaults to 'gc' (great circle).

    Returns:
      Interpolated latitude and longitude points.
    """
    if method != 'gc':
        raise ValueError("Currently, only 'gc' (great circle) interpolation is implemented.")

    # Convert input arrays to radians for calculations
    lat_rad = np.radians(latd)
    lon_rad = np.radians(lond)

    # Initialize lists to store interpolated points
    interp_lat = []
    interp_lon = []

    # Number of points
    n = len(lat_rad)

    # Iterate over the points to create segments
    for i in range(n - 1):
        lat1, lon1 = lat_rad[i], lon_rad[i]
        lat2, lon2 = lat_rad[i + 1], lon_rad[i + 1]

        # Calculate the great circle distance
        d = np.arccos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1))

        # Number of interpolation points
        num_points = int(np.ceil(d / radians(spacing)))  # Calculate number of points based on spacing

        # Interpolate points on the great circle
        for j in range(num_points + 1):
            f = j / num_points  # Fraction along the arc
            A = sin((1 - f) * d) / sin(d)  # Law of sines
            B = sin(f * d) / sin(d)

            x = A * cos(lat1) * cos(lon1) + B * cos(lat2) * cos(lon2)
            y = A * cos(lat1) * sin(lon1) + B * cos(lat2) * sin(lon2)
            z = A * sin(lat1) + B * sin(lat2)

            interp_lon.append(degrees(atan2(y, x)))  # Calculate interpolated longitude
            interp_lat.append(degrees(asin(z)))       # Calculate interpolated latitude

    return np.array(interp_lat), np.array(interp_lon)
