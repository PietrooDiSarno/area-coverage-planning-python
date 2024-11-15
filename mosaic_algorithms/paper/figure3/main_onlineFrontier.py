import copy

from mosaic_algorithms.online_frontier_repair.frontierRepair import frontierRepair
from mosaic_algorithms.auxiliar_functions.plot.plotTour import plotTour
from mosaic_algorithms.paper.figure3.input_data_fig3 import *  # Load mission info (kernels, SPICE ids, etc.)
import matplotlib.pyplot as plt
import importlib

# Revision of grid discretization:
# Grid is going to be built in the camera frame, instead of the body-fixed
# frame. This is somewhat more complicated (it requires more calculations)
# but it could correct the spatial aberration that we presently see
# Re-implementation of sidewinder function with these new feature (and
# other code improvements)

mosaic = 'onlinefrontier'
roiname = roistruct[0]['name'].lower().replace(" ", "")
name = f'post_process_{roiname}'
module_name = f"mosaic_algorithms.paper.figure3.{name}"
module = importlib.import_module(module_name)


# Online Frontier
A, fpList = frontierRepair(roistruct[0]['inittime'], stoptime, tcadence, inst, sc, target, roi, olapx, olapy, 3 * 1e-3)

# Plot tour
ax = plotTour(A, fpList, roistruct, sc, target)
ax.set_title(roistruct[0]['name'], fontweight = 'bold', fontsize = 20)
ax.legend(loc='upper center', ncol=2)
handles, labels = ax.get_legend_handles_labels()
vals_label = [labels[0]]
inds = [0]
for ind_label,val_label in enumerate(labels):
    if not val_label in vals_label:
        vals_label.append(val_label)
        inds.append(ind_label)
labels = copy.deepcopy(vals_label)
handles = [handles[i] for i in inds]
handles = handles[:-1]
labels = labels[:-1]
legend = ax.legend(handles=handles, labels=labels, loc='upper center', ncol=2)
legend.get_frame().set_alpha(1)

# FOM post-process
exec(open(f"{name}.py").read())

post_process_fig3(roistruct,mosaic)