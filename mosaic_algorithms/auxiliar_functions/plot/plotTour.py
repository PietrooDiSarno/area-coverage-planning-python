import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon, Polygon
import numpy as np
from mosaic_algorithms.auxiliar_functions.plot.groundtrack import groundtrack
from mosaic_algorithms.auxiliar_functions.plot.mapPlot import mapPlot
from mosaic_algorithms.auxiliar_functions.polygon_functions.amsplit import amsplit


def plotTour(tour, fplist, roistruct, sc, target, *args):
    # Pre-allocate variables
    filename = f"../../auxiliar_functions/plot/global-maps/{target.lower()}-map.jpg"
    c1 = (0.72, 0.27, 1.00)
    c2 = (0.35, 0.06, 0.41)
    if len(args) > 0:
        ax = args[0]
        if len(args) > 1:
            video = args[1]
        else:
            video = None
    else:
        fig, ax = mapPlot(filename)
        video = None

    # Plot region(s) of interest
    if video is not None:
        for roi in roistruct:
            x, y = np.array(roi['vertices'])[:,0],np.array(roi['vertices'])[:,1]
            ax.plot(x,y,color='k', linewidth=1, linestyle='-', label=roi['name'])
            #plt.draw()
            plt.pause(0.5)
        #plt.ioff()
        #plt.show(block = False)
        plt.pause(0.5)
        #plt.ion()
    # Check
    if not tour:
        return

    # Plot footprint list
    for i in range(len(fplist)):
        # Plot footprint polygon
        if (np.isnan(fplist[i]['bvertices'][:, 0])).any():
            nanindex = np.where(np.isnan(fplist[i]['bvertices'][:, 0]))[0]
            for i in range(len(nanindex)):
                if i == 0:
                    h1 = ax.fill(fplist[i]['bvertices'][:nanindex[0], 0], fplist[i]['bvertices'][:nanindex[0],1],
                                 color=c1, alpha=0.2, edgecolor=c2, linewidth=1.5, label='Footprint')
                    plt.pause(0.5)
                else:
                    h1 = ax.fill(fplist[i]['bvertices'][nanindex[i - 1] + 1:nanindex[i], 0],
                                 fplist[i]['bvertices'][nanindex[i - 1] + 1:nanindex[i], 1],
                                 color=c1, alpha=0.2, edgecolor=c2, linewidth=1.5, label='Footprint')
                    plt.pause(0.5)
            if ~ np.isnan(fplist[i]['bvertices'][-1, 0]):
                h1 = ax.fill(fplist[i]['bvertices'][nanindex[-1] + 1:, 0],
                             fplist[i]['bvertices'][nanindex[-1] + 1:, 1],
                             color=c1, alpha=0.2, edgecolor=c2, linewidth=1.5, label='Footprint')
                plt.pause(0.5)
        else:
            h1 = ax.fill(fplist[i]['bvertices'][:, 0], fplist[i]['bvertices'][:, 1], color=c1, alpha=0.2, edgecolor=c2,
                         linewidth=1.5, label='Footprint')
            plt.pause(0.5)

        # Plot coverage path
        if i > 0:
            if abs(tour[i-1][0] - tour[i][0]) <= 180:  # no coverage path - a.m. intercept
                h2 = ax.plot([tour[i-1][0], tour[i][0]], [tour[i-1][1], tour[i][1]],
                        color='y', linewidth=1.5, label='Coverage path')
                plt.pause(0.5)
        else:
            h2 = None
            h3 = ax.scatter(tour[i][0], tour[i][1], s=100, color='b', marker='^', label='Start point')
            plt.pause(0.5)

        # Plot ground track
        t = fplist[i]['t']
        sclon, sclat = groundtrack(sc, t, target)
        if i > 0:
            h4 = ax.scatter(sclon, sclat, s=8, color='c', marker='o', label='Ground track')
            plt.pause(0.5)
        else:
            h4 = None
            h5 = ax.scatter(sclon, sclat, s=100, color='b', marker='^')
            plt.pause(0.5)
        # Save animation
        if video is not None:
            plt.draw()
            video.grab_frame()

    # Re-plot the ROI (for aesthetic purposes)
    for i in range(len(roistruct)):
        roi = np.array(roistruct[i]['vertices'])
        x, y = amsplit(roi[:,0], roi[:,1])

        if (np.isnan(x)).any():
            nanindex = np.where(np.isnan(x))[0]
            polygon_list = []
            for i in range(len(nanindex)):
                if i == 0:
                    h5 = ax.plot(x[:nanindex[0]], y[:nanindex[0]], color='k', linewidth=1.5, linestyle='-',
                                 label=roistruct[i]['name'])
                    plt.pause(0.5)
                else:
                    h5 = ax.plot(x[nanindex[i - 1] + 1:nanindex[i]], y[nanindex[i - 1] + 1:nanindex[i]],
                                 color='k', linewidth=1.5, linestyle='-', label=roistruct[i]['name'])
                    plt.pause(0.5)
            if ~ np.isnan(x[-1]):
                h5 = ax.plot(x[nanindex[-1] + 1:], y[nanindex[-1] + 1:],
                             color='k', linewidth=1.5, linestyle='-', label=roistruct[i]['name'])
                plt.pause(0.5)
        else:
            h5 = ax.plot(x, y, color='k', linewidth=1.5, linestyle='-', label=roistruct[i]['name'])
            plt.pause(0.5)

    # Legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, loc='best', frameon=False)

    if video is not None:
        video.finish()
