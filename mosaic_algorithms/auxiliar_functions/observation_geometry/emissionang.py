import numpy as np
from conversion_functions import *


def emissionang(srfpoint, t, target, obs):
    """
    This function returns the phase angle between the target normal to
    surface and the distance vector to the observer, from the target surface
    point srfpoint, at time t.

    Programmers: Paula Betriu (UPC/ESEIAAT)
    Date: 10/2022

    Usage: angle = emissionang(srfpoint, t, target, obs)

    Inputs:
      srfpoint: target surface point. It can be input either in latitudinal
                coordinates (in [deg]) or Cartesian coordinates (in [km]).
      t:        time epoch in TDB seconds past J2000 epoch. It can be
                either a single point in time or a discretized vector of
                different time values.
      target:   string SPICE name of the target body.
      obs:      string SPICE name of the observer body.

    Outputs:
      angle:    angle between the normal surface and the distance vector to
                the observer, in [deg].
    """

    # Parameters
    method = 'ELLIPSOID'  # assumption: tri-axial ellipsoid modeling of the target body
    _, targetframe, _ = mat2py_cnmfrm(target)  # target frame ID in SPICE

    # If srfpoint has been input with the latitudinal coordinates, change to rectangular
    if len(srfpoint) == 2:
        srfpoint = np.radians(srfpoint)  # [deg] to [rad]
        srfpoint = mat2py_srfrec(mat2py_bodn2c(target), srfpoint[0],
                                 srfpoint[1])  # surface point in rectangular coordinates

    else:
        # if srfpoint is input as a 1x3 instead of a 3x1, transpose array
        if srfpoint.ndim == 1:
            srfpoint = srfpoint.reshape(3, 1)

    # Compute the observer position as seen from the srfpoint
    obsvec = trgobsvec(srfpoint, t, target, obs)

    # Obtain the outwards surface normal vector
    nrmvec = np.zeros((3, len(t)))
    for i in range(len(t)):
        nrmvec[:, i] = mat2py_srfnrm(method, target, t[i], targetframe, srfpoint)  # normal to surface

    # Angle between the two vectors
    angle = mat2py_vsep(obsvec, nrmvec)  # angle in radians
    angle = np.degrees(angle)  # [rad] to [deg]

    return angle