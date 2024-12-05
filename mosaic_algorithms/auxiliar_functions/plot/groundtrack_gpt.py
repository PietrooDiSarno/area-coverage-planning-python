import numpy as np

from conversion_functions import *


def groundtrack(obs, t, target):
    """
    Returns the spacecraft ground track across the target surface at time t.

    Usage:
        gtlon, gtlat = groundtrack(obs, t, target)

    Inputs:
        obs (str):      SPICE name of the observer body.
        t (float or array-like): Time epoch(s) in TDB seconds past J2000 epoch.
                                 Can be a single value or an array of values.
        target (str):   SPICE name of the target body.

    Outputs:
        gtlon (float or ndarray): Longitude coordinate(s) of the observer ground track, in degrees.
        gtlat (float or ndarray): Latitude coordinate(s) of the observer ground track, in degrees.
    """

    # Initialize method and aberration correction parameters
    method = 'INTERCEPT/ELLIPSOID'  # Target modeling
    abcorr = 'NONE'                 # Aberration correction

    # Get the body-fixed frame associated with the target body
    # Original MATLAB: [~, tframe, ~] = cspice_cnmfrm(target);
    # Using mat2py_cnmfrm wrapper function to get frame name (tframe)
    # The mat2py_cnmfrm function returns (frcode, frname, found)
    _, tframe, _ = mat2py_cnmfrm(target)  # tframe is the body-fixed frame name

    # Ensure t is a numpy array for consistent handling
    t = np.atleast_1d(t)

    # Initialize lists to store results
    gtlon_list = []
    gtlat_list = []

    # Degrees per radian constant
    dpr = mat2py_dpr()

    # Loop over each time value in t
    for et in t:
        # Compute the sub-spacecraft point on the target body
        # Original MATLAB: sctrack = cspice_subpnt(method, target, t, tframe, abcorr, obs);
        # Using mat2py_subpnt wrapper function
        # mat2py_subpnt returns (spoint, trgepc, srfvec)
        sctrack = mat2py_subpnt(method, target, et, tframe, abcorr, obs)[0]  # Extracting spoint

        # Convert the rectangular coordinates of the sub-spacecraft point to latitudinal coordinates
        # Original MATLAB: [~, gtlon, gtlat] = cspice_reclat(sctrack);
        # Using mat2py_reclat wrapper function
        # mat2py_reclat returns (radius, lon, lat)
        _, lon, lat = mat2py_reclat(sctrack)

        # Convert longitude and latitude from radians to degrees
        # Original MATLAB: gtlon = gtlon * cspice_dpr; gtlat = gtlat * cspice_dpr;
        lon_deg = lon * dpr
        lat_deg = lat * dpr

        # Append to lists
        gtlon_list.append(lon_deg)
        gtlat_list.append(lat_deg)

    # Convert lists to numpy arrays (or scalars if only one element)
    gtlon_array = np.array(gtlon_list) if len(gtlon_list) > 1 else gtlon_list[0]
    gtlat_array = np.array(gtlat_list) if len(gtlat_list) > 1 else gtlat_list[0]

    return gtlon_array, gtlat_array

# Conversion Notes:
# - The MATLAB function `cspice_cnmfrm` returns [frcode, frname, found], where frname is the body-fixed frame.
#   We used `mat2py_cnmfrm` to obtain `tframe`, the target frame.
# - The function `cspice_subpnt` computes the sub-spacecraft point. We used `mat2py_subpnt` and extracted the first
#   output, `spoint`, which corresponds to `sctrack` in the MATLAB code.
# - The MATLAB function `cspice_reclat` converts rectangular coordinates to latitudinal coordinates, returning
#   [radius, lon, lat]. We used `mat2py_reclat` and extracted `lon` and `lat`.
# - The degrees per radian conversion uses `cspice_dpr` in MATLAB, which returns a constant. We used `mat2py_dpr`
#   to obtain this constant in Python.
# - The original MATLAB code may handle vectorized inputs implicitly. In Python, we explicitly loop over each time
#   value if `t` is an array to compute the ground track coordinates.
# - We ensured that the function returns scalar values if input `t` is a scalar, and numpy arrays if `t` is an array.
# - Comments have been added to explain each step and any differences from the MATLAB code.
