import matplotlib.pyplot as plt
from shapely.geometry import Polygon as ShapelyPolygon
from mosaic_algorithms.auxiliar_functions.plot.groundtrack import groundtrack
from mosaic_algorithms.auxiliar_functions.plot.mapPlot import mapPlot

def plotTour(tour, fplist, roistruct, sc, target, *args):
    # Pre-allocate variables
    filename = f"{target.lower()}-map.jpg"
    c1 = (0.72, 0.27, 1.00)
    c2 = (0.35, 0.06, 0.41)
    if len(args) > 0:
        ax = args[0]
        if len(args) > 1:
            video = args[1]
        else:
            video = None
    else:
        ax = mapPlot(filename)
        video = None

    # Plot region(s) of interest
    if video is not None:
        for roi in roistruct:
            poly = ShapelyPolygon(roi['vertices'])
            x, y = poly.exterior.xy
            ax.plot(x, y, color='k', linewidth=1, linestyle='-', label=roi['name'])

    # Check
    if not tour:
        return

    # Plot footprint list
    for i in range(len(fplist)):
        # Plot footprint polygon
        poly = ShapelyPolygon(fplist[i]['bvertices'])
        x, y = poly.exterior.xy
        h1 = ax.fill(x, y, color=c1, alpha=0.2, edgecolor=c2, linewidth=1.5, label='Footprint')

        # Plot coverage path
        if i > 0:
            if abs(tour[i-1][0] - tour[i][0]) <= 180:  # no coverage path - a.m. intercept
                h2 = ax.plot([tour[i-1][0], tour[i][0]], [tour[i-1][1], tour[i][1]],
                        color='y', linewidth=1.5, label='Coverage path')
        else:
            h2 = None
            h3 = ax.scatter(tour[i][0], tour[i][1], s=100, color='b', marker='^', label='Start point')

        # Plot ground track
        t = fplist[i]['t']
        sclon, sclat = groundtrack(sc, t, target)
        if i > 0:
            h4 = ax.scatter(sclon, sclat, s=8, color='c', marker='o', label='Ground track')
        else:
            h4 = None
            h5 = ax.scatter(sclon, sclat, s=100, color='b', marker='^')

        # Save animation
        if video is not None:
            plt.draw()
            video.grab_frame()

    # Re-plot the ROI (for aesthetic purposes)
    for roi in roistruct:
        poly = ShapelyPolygon(roi['vertices'])
        x, y = poly.exterior.xy
        h5 = ax.plot(x, y, color='k', linewidth=1.5, linestyle='-', label=roi['name'])

    # Legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, loc='best', frameon=False)

    if video is not None:
        video.finish()
