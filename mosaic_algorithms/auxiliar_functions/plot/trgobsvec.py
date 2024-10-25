import numpy as np
import copy
from conversion_functions import *

def trgobsvec(srfpoint, t, target, obs, frame=None):
    """
    Distance vector between the target point P and the observer at time t

    Programmers:  Paula Betriu (UPC/ESEIAAT)
    Date:         10/2022

    Usage:        obsvec = trgobsvec(srfpoint, t, target, obs)
                  obsvec = trgobsvec(srfpoint, t, target, obs, frame)

    Inputs:
      > srfpoint: target surface point. It can be input either in latitudinal
                  coordinates (in [deg]) or Cartesian coordinates (in [km])
                  with respect to the body-fixed reference frame
      > t:        time epoch in TDB seconds past J2000 epoch. It can be
                  either a single point in time or a discretized vector of
                  different time values
      > target:   string SPICE name of the target body
      > obs:      string SPICE name of the observer body
      > frame:    string SPICE name of the reference frame with respect to
                  which the vector is going to be expressed. If this
                  variable is not input, the body-fixed reference frame is
                  used by default

    Returns:
      > obsvec:   observer position vector as seen from the target surface
                  point in the target body-fixed reference frame, in [km]
    """
    # Pre-allocate variables
    input_frame = copy.deepcopy(frame)
    _,frame,_ = mat2py_cnmfrm(target) # target frame ID in SPICE
    abcorr = 'NONE'  # assumption: this function calculates the distance vector
                     # between the two objects considering the geometric position, no light
                     # aberrations are considered (see cspice_spkpos)

    # If srfpoint has been input with the latitudinal coordinates, change to
    # rectangular
    if len(srfpoint) == 2:
        srfpoint = srfpoint*mat2py_rpd # [deg] to [rad]
        srfpoint = mat2py_srfrec(mat2py_bodn2c(target), srfpoint[0], srfpoint[1]) # surface point in
        # rectangular coordinates (body modeled as a tri-axial ellipsoid)
    elif np.size(srfpoint, 0) == 1: # if srfpoint is input as a 1x3 instead of a 3x1, transpose array
        srfpoint = srfpoint.reshape((3, 1))

    # Compute the observer position as seen from the srfpoint
    obspos = mat2py_spkpos(obs, t, frame, abcorr, target)  # compute observer position
    # as seen from the target body in the body-fixed ref frame
    obsvec = obspos - srfpoint  # srfpoint-observer distance vector


    # A different reference frame is requested
    if input_frame is not None:
        from_frame = frame
        to_frame = input_frame
        rotmat = mat2py_pxform(from_frame, to_frame, t)  # Rotation matrix from body-fixed
        # reference frame to the requested one
        if isinstance(t, (list, np.ndarray)) and len(t) > 1:
            for i in range(np.max(rotmat.shape)):
                obsvec[:, i] = np.dot(rotmat[:, :, i], obsvec[:, i])
        else:
            obsvec = np.dot(rotmat, obsvec)

    # Compute distance
    dist = np.linalg.norm(obsvec)

    return obsvec, dist