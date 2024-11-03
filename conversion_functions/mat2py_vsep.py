# This code implements a function that receives the users' inputs, calls the SPICE function "spice.vsep"
# and returns the adapted outputs.
import spiceypy as spice
import numpy as np


# The function cspice_vsep in MATLAB can receive:
# - v1:[3,n] = size(v1); double = class(v1)
# - v2:[3,n] = size(v2); double = class(v2)
# Since MATLAB can handle over more than one couple of vectors, while Python can handle over one couple of vectors
# per time, a "for" cycle is needed.

# The function spice.vsep in Python receives:
# - v1: ndarray
# - v2: ndarray

# The function cspice_vsep in MATLAB gives as output:
# - vsep:[1,n] = size(vsep); double = class(vsep)

# The function spice.vsep in Python gives as output:
# - vsep:float

def mat2py_vsep(v1, v2):
    if len(v1) == 3:
        v1 = np.array(v1).reshape(len(v1), )
        v2 = np.array(v2).reshape(len(v2), )
        vsep = spice.vsep(v1, v2)
    else:
        v1 = np.array(v1)
        v2 = np.array(v2)
        vsep = []
        for i in range(0, np.shape(v1)[1]):
            v1 = v1[:, i]
            v2 = v2[:, i]
            vsep.append(spice.vsep(v1, v2))
        vsep = np.array(vsep).reshape(len(vsep), )
    return vsep
