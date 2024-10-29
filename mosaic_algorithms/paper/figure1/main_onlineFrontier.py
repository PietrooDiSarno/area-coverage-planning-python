import numpy as np
import matplotlib.pyplot as plt
from mosaic_algorithms.paper.figure1.input_data_fig1 import input_data_fig1
# Revision of grid discretization:
# Grid is going to be built in the camera frame, instead of the body-fixed
# frame. This is somewhat more complicated (it requires more calculations)
# but it could correct the spatial aberration that we presently see
# Re-implementation of sidewinder function with these new feature (and
# other code improvements)

# Load mission info (kernels, SPICE ids, etc.)
input_data_fig1()

# Online Frontier
A, fpList = frontierRepair(roistruct[0].inittime,
                            stoptime, tcadence, inst, sc, target, roi, olapx, olapy, 3 * 1e-3)

# Plot tour
plotTour(A, fpList, roistruct, sc, target)

# FOM post-process
post_process_fig1()

# Save figure [PDF]
figpath = '.'
plt.gcf().set_size_inches(9.2, 6)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
filename = f"{figpath}/fig1_onlinefrontier.pdf"
plt.savefig(filename, dpi=1200, bbox_inches='tight')
