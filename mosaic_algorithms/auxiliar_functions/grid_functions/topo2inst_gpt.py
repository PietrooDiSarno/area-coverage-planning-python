import numpy as np
from conversion_functions import *
from mosaic_algorithms.auxiliar_functions.plot.trgobsvec import trgobsvec
from mosaic_algorithms.auxiliar_functions.spacecraft_operation.instpointing import instpointing


def topo2inst(inputdata, lon, lat, target, sc, inst, et):
    """
    Transforms topographical coordinates to instrument frame coordinates.

    Parameters:
    -----------
    inputdata : list of lists or numpy array
        Topographical points (longitude, latitude in degrees). Can be a nested list or a numpy array.
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
    outputData : list of lists or numpy array
        Instrument frame coordinates corresponding to the input topographical points.
        If inputdata is a nested list, outputData will be a nested list with the same structure.
        If inputdata is a numpy array, outputData will be a numpy array.
    """

    # Import necessary modules
    # Note: Ensure that mat2py_xxxx functions, instpointing, and trgobsvec are properly imported.

    # Check if inputdata is a list (nested list representing a cell array)
    if isinstance(inputdata, list):
        # Flatten the inputdata into topoPoints, and keep track of indices
        aux = []
        ii = []
        jj = []
        for i, row in enumerate(inputdata):
            for j, item in enumerate(row):
                if item is not None:
                    aux.append(item)
                else:
                    aux.append([np.nan, np.nan])
                ii.append(i)
                jj.append(j)
        # Convert aux to numpy array for vectorized operations
        topoPoints = np.array(aux)
    else:
        # Inputdata is already a numpy array
        topoPoints = np.array(inputdata)
        # No need to keep track of indices
        ii = None
        jj = None

    # Pre-allocate variables
    # Get the target body-fixed frame ID in SPICE
    _, targetframe, _ = mat2py_cnmfrm(target)

    # Build focal plane
    # Get the field of view bounds, boresight vector, and rotation matrix from instrument frame to body-fixed frame
    fovbounds, boresight, rotmat = instpointing(inst, target, sc, et, lon, lat)

    # Get the position of the spacecraft in the target frame
    vertex, _ = mat2py_spkpos(sc, et, targetframe, 'NONE', target)

    # Define a point in the focal plane using the first column of fovbounds
    point = vertex + fovbounds[:, 0]

    # Define the plane using the normal vector (boresight) and a point in the plane
    plane = mat2py_nvp2pl(boresight, point)

    # Initialize spoint array to store intersection points
    spoint = np.zeros((topoPoints.shape[0], 3))

    # Intersect topoPoints with focal plane
    for i in range(topoPoints.shape[0]):
        if not np.any(np.isnan(topoPoints[i, :])):
            # Convert longitude and latitude from degrees to radians
            lon_rad = topoPoints[i, 0] / mat2py_dpr()
            lat_rad = topoPoints[i, 1] / mat2py_dpr()
            # Compute the position vector from latitude and longitude
            # Original MATLAB function may have used a function like cspice_latrec
            xpoint = mat2py_latrec(lon_rad, lat_rad, 1.0)  # Assuming unit radius
            # Compute the direction vector from target to observer (spacecraft)
            # Note: trgobsvec is a custom function that needs to be defined
            dir_vector = -trgobsvec(topoPoints[i, :], et, target, sc)
            # Find the intersection of the line with the plane
            # Original MATLAB function: [found, spoint(i, :)] = cspice_inrypl(vertex, dir, plane);
            found, spoint_i = mat2py_inrypl(vertex, dir_vector, plane)
            if found:
                spoint[i, :] = spoint_i
            else:
                # Intersection not found
                print(f"No intersection at point index {i}")
                spoint[i, :] = np.array([np.nan, np.nan, np.nan])
        else:
            # topoPoint contains NaN values
            spoint[i, :] = np.array([np.nan, np.nan, np.nan])

    # Transform coordinates from body-fixed frame to instrument frame
    tArea = np.zeros((spoint.shape[0], 3))
    for i in range(spoint.shape[0]):
        if not np.any(np.isnan(spoint[i, :])):
            # Compute the vector from vertex (spacecraft) to spoint
            vpoint = -(vertex - spoint[i, :])
            # Transform to instrument frame coordinates using the rotation matrix
            # Original MATLAB operation: tArea(i, :) = rotmat \ vpoint;
            tArea[i, :] = np.linalg.solve(rotmat, vpoint)
        else:
            tArea[i, :] = np.array([np.nan, np.nan, np.nan])

    # Extract the first two components (x, y) as instrument coordinates
    instcoord = tArea[:, 0:2]

    # Prepare the output data in the same structure as inputdata
    if isinstance(inputdata, list):
        # Reconstruct outputData as a nested list with the same structure as inputdata
        outputData = [[None for _ in row] for row in inputdata]
        for idx in range(len(ii)):
            i = ii[idx]
            j = jj[idx]
            if not np.any(np.isnan(instcoord[idx, :])):
                outputData[i][j] = instcoord[idx, :].tolist()
            else:
                outputData[i][j] = None
    else:
        # Inputdata was a numpy array; return instcoord as numpy array
        outputData = instcoord

    return outputData
