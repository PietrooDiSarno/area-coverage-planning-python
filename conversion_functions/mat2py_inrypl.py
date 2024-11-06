# This code implements a function that receives the users' inputs, calls the SPICE function "spice.inrypl"
# and returns the adapted outputs.
import numpy as np
import spiceypy as spice


# The function cspice_inrypl in MATLAB can receive:
# - vertex: DOUBLE = Array[3]
# - direction: DOUBLE = Array[3]
# - plane:STRUCT = CSPICE_PLANE

# The function spice.inrypl in Python receives:
# - vertex: iterable[floats]
# - direction: iterable[floats]
# - plane: plane

# The function cspice_inrypl in MATLAB gives as output:
# - nxpts: LONG = Scalar
# - xpt:DOUBLE = Array[3]

# The function spice.inrypl in Python gives as output:
# - Tuple of [nxpts,xpt] whose shape is Tuple[int,ndarray]

def mat2py_inrypl(vertex, direction, plane):
    vertex = np.array(vertex, dtype=float).reshape(3, )
    direction = np.array(direction, dtype=float).reshape(3, )
    nxpts, xpt = spice.inrypl(vertex, direction, plane)
    nxpts = int(nxpts)
    xpt = np.array(xpt, dtype=float).reshape(3, )

    return nxpts, xpt
