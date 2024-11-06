# Import external modules
import numpy as np
from pyproj import Geod


# Function to interpolate points along the great circle path
def interpm(lat, lon, maxdist):
    """
    Densify latitude and longitude vectors according to a maximum distance between points.

    Parameters:
        lat (numpy array): Array of latitude values.
        lon (numpy array): Array of longitude values.
        maxdist (float): Maximum allowed distance between points in meters.

    Returns:
        tuple: Arrays of interpolated latitude and longitude values.
    """

    # Initialize the Geod object for geodesic calculations (WGS84 ellipsoid)
    geod = Geod(ellps='WGS84')

    interp_lat = []
    interp_lon = []
    for i in range(len(lat) - 1):
        lat1, lon1 = lat[i], lon[i]
        lat2, lon2 = lat[i + 1], lon[i + 1]

        # Append the current point
        interp_lat.append(lat1)
        interp_lon.append(lon1)

        # Calculate the distance between the current and next point
        az12, az21, dist = geod.inv(lon1, lat1, lon2, lat2)

        # Determine the number of intermediate points needed
        num_points = int(np.ceil(dist / maxdist))

        if num_points > 1:
            # Generate intermediate points along the geodesic
            lonlats = geod.npts(lon1, lat1, lon2, lat2, num_points - 1)
            for lon_interp, lat_interp in lonlats:
                interp_lat.append(lat_interp)
                interp_lon.append(lon_interp)

    # Append the last point
    interp_lat.append(lat[-1])
    interp_lon.append(lon[-1])

    return np.array(interp_lat), np.array(interp_lon)
