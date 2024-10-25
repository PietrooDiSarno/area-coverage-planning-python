import numpy as np
import spiceypy as spice
import copy
from conversion_functions import *
from mosaic_algorithms.auxiliar_functions.spacecraft_operation.instpointing import instpointing

def topo2inst(inputdata, lon, lat, target, sc, inst, et):
    """
    This function transforms a set of points from the topographic coordinate
    system(latitude and longitude on the target body) to the instrument frame
    coordinates.

    Programmers:  Paula Betriu (UPC/ESEIAAT)
    Date:         09/2022

    Usage:        outputData = topo2inst(inputdata, lon, lat, target, sc, inst, et)

    Inputs:
      > inputdata:    list of points in topographic coordinates to be
                      transformed. Each point is a row with
                      [longitude, latitude] format
      > lon:          longitude of the observation point or area center, in
                      [deg]
      > lat:          latitude of the observation point or area center, in
                      [deg]
      > target:       string name of the target body
      > sc:           string name of the spacecraft
      > inst:         string name of the instrument
      > et:           ephemeris time, TDB seconds past J2000 epoch

    Returns:
      > outputData:   A list of the input points transformed
                      to the instrument frame coordinates. The format of the
                      output matches the input (cell array or matrix)
    """

    # Handle input data in list format, ensuring all empty entries are replaced
    # with [NaN,NaN]

    ii,jj=0,0
    if isinstance(inputdata, list):
        inputdata = [point if point else [np.nan, np.nan] for point in inputdata]
        topoPoints = np.vstack(inputdata)
        inputdata_array = np.array(inputdata)
        ii,jj = np.unravel_index(np.arange(inputdata_array.size), inputdata_array.shape)
    else:
        topoPoints = copy.deepcopy(inputdata)

    # Pre-allocate variables
    _,targetframe,_ = mat2py_cnmfrm(target)  # get the target frame ID

    # Build focal plane
    fovbounds, boresight, rotmat = instpointing(inst, target, sc, et, lon, lat)
    vertex = mat2py_spkpos(sc, et, targetframe, 'NONE', target)[0]
    point = vertex + fovbounds[:, 0]

    # Create a plane based on the boresight and a point in the focal plane
    plane = mat2py_nvp2pl(boresight, point)

    # For each topographic point, find its intersection with the focal plane
    spoint = np.zeros((topoPoints.shape[0], 3))

    for i in range(topoPoints.shape[0]):
        if not np.isnan(topoPoints[i]).any():
            dir = -trgobsvec(topoPoints[i], et, target, sc)
            found, spoint[i] = mat2py_inrypl(vertex, dir, plane)
            if found:
                emnang = emissionang(topoPoints[i], et, target, sc)
                if emnang >= 90:
                    found = False
            if not found:
                spoint[i] = [np.nan, np.nan, np.nan]
        else:
            spoint[i] = [np.nan, np.nan, np.nan]

    # Transform coordinates from body-fixed to instrument frame
    tArea = np.zeros((spoint.shape[0], 3))
    for i in range(spoint.shape[0]):
        if not np.isnan(spoint[i]).any():
            vpoint = -(vertex - np.transpose(spoint[i, :])) # vector from spacecraft to intersection point
            tArea[i, :] = np.linalg.solve(rotmat, vpoint) # apply inverse rotation to
                                                          # transform to instrument frame
        else:
            tArea[i, :] = [np.nan, np.nan, np.nan]

    instcoord = tArea[:, 0:1]  # extract 2D instrument frame coordinates

    # Prepare output data matching the format of the input,i.e., cell array or
    # matrix

    if isinstance(inputdata, list):
        outputData = [[None for _ in row] for row in inputdata]
        for k in range(len(ii)):
            coord in enumerate(instcoord):
            if not np.isnan(coord).any():
                i, j = indices[0].flatten()[idx], indices[1].flatten()[idx]
                outputData[i][j] = coord.tolist()
    else:
        instcoord = instcoord[~np.isnan(instcoord).any(axis=1)]
        aux = sortcw(instcoord[:, 0], instcoord[:, 1])
        outputData = np.column_stack(aux)

    return outputData

# Additional utility functions like 'instpointing', 'trgobsvec', 'emissionang', and 'sortcw' need to be implemented as well.