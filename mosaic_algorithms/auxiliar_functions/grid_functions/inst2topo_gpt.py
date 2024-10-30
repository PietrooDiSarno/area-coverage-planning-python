import numpy as np
from conversion_functions import *
from mosaic_algorithms.auxiliar_functions.spacecraft_operation.instpointing import instpointing


def inst2topo(grid, lon, lat, target, sc, inst, et):
    """
    Transforms grid points from instrument frame coordinates to topographical coordinates.

    Parameters:
    -----------
    grid : list of lists
        Grid points in instrument frame coordinates. Each element grid[i][j] is a 2-element list or array.
    lon : float
        Longitude of the instrument pointing in degrees.
    lat : float
        Latitude of the instrument pointing in degrees.
    target : str
        Name of the target body (e.g., 'Earth').
    sc : str
        Name of the spacecraft.
    inst : str
        Name of the instrument.
    et : float
        Ephemeris time (seconds past J2000).

    Returns:
    --------
    grid_topo : list of lists
        Grid points in topographical coordinates (longitude, latitude in degrees).
        Each element grid_topo[i][j] is a 2-element list [longitude, latitude].
    """

    # Import necessary modules
    # Note: Ensure that mat2py_xxxx functions and instpointing are properly imported
    # from their respective modules.

    # Pre-allocate variables
    # Obtain the rotation matrix from instrument frame to body-fixed frame
    # Original MATLAB function: [~, ~, rotmat] = instpointing(inst, target, sc, et, lon, lat);
    _, _, rotmat = instpointing(inst, target, sc, et, lon, lat)

    # Initialize grid_topo with the same size as grid, filled with None
    grid_topo = [[None for _ in row] for row in grid]

    method = 'ELLIPSOID'  # Method for surface intercept calculation

    # Get the target body-fixed frame ID in SPICE
    # Original MATLAB function: [~, targetframe, ~] = cspice_cnmfrm(target);
    _, targetframe, _ = mat2py_cnmfrm(target)

    # Get the rectangular coordinates of the instrument in the body-fixed reference frame
    # Original MATLAB function: instpos = cspice_spkpos(sc, et, targetframe, 'NONE', target);
    instpos, _ = mat2py_spkpos(sc, et, targetframe, 'NONE', target)

    # Convert each grid point from instrument frame to topographical coordinates
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            instp = grid[i][j]
            if instp is not None:
                instp = np.array(instp)
                # Check if the grid point does not contain NaN values
                if not np.any(np.isnan(instp)):
                    # Create a 3-element vector p in instrument frame
                    p = np.zeros(3)
                    p[0:2] = instp  # Assign the x and y components from the grid point
                    p[2] = 1        # Set z component to 1 (assuming unit vector)
                    # Transform p from instrument frame to body-fixed frame
                    p_body = np.dot(rotmat, p)
                    # Compute the surface intercept point on the target body
                    # Original MATLAB function:
                    # [xpoint, ~, ~, found] = cspice_sincpt(method, target, et, targetframe, 'NONE', sc, targetframe, p_body);
                    xpoint, _, _, found = mat2py_sincpt(method, target, et, targetframe, 'NONE', sc, targetframe, p_body)
                    if found:
                        # Convert rectangular coordinates to latitudinal coordinates (radius, longitude, latitude)
                        # Original MATLAB function: [~, lon, lat] = cspice_reclat(xpoint);
                        _, lon_rad, lat_rad = mat2py_reclat(xpoint)
                        # Convert longitude and latitude from radians to degrees
                        lon_deg = lon_rad * mat2py_dpr()
                        lat_deg = lat_rad * mat2py_dpr()
                        # Store the topographical coordinates in the output grid
                        grid_topo[i][j] = [lon_deg, lat_deg]
                    else:
                        # Surface intercept point not found
                        print(f"Point not visible from the instrument at grid position ({i}, {j})")
                else:
                    # Grid point contains NaN values; leave the corresponding grid_topo entry as None
                    pass
            else:
                # Grid point is None; leave the corresponding grid_topo entry as None
                pass

    return grid_topo
