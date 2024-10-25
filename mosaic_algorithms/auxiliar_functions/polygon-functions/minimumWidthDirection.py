import numpy as np
from scipy.spatial import ConvexHull

def minimumWidthDirection(x, y):
    """
    This function computes the orientation (angle) at which the width of the
    polygon is minimized. It also calculates the minimum width, the height
    (assuming the minimum width as the base), and the direction vector (axes)
    of the minimum width

    Programmers:  Paula Betriu (UPC/ESEIAAT)
    Date:         09/2022

    Usage:        [thetamin, minwidth, height, axes] = minimumWidthDirection(x, y)

    Inputs:
      > x:            array of x-coordinates of the polygon vertices
      > y:            array of y-coordinates of the polygon vertices

    Outputs:
      > thetamin:     angle at which polygon's width is minimized, in [deg]
      > minwidth:     minimum width of the polygon
      > height:       height of the polygon, at the orientation specified by
                      thetamin and assuming minwidth as the base
      > axes:         unit vector representing the direction of the polygon
                      axes (width, height)
   """

    # Check if the polygon is divided in two (a.m. intersection)...
    ind = np.where(np.isnan(x))[0]
    if ind.size > 0:
        x[:ind[0]] += 360
        x = np.delete(x, ind)
        y = np.delete(y, ind)

    # Find centroid
    hull = ConvexHull(np.array([x, y]).T)
    cx, cy = np.mean(hull.points[hull.vertices], axis=0)

    # Sort the vertices in clockwise direction
    vertices = np.array([x, y]).T
    angles = np.arctan2(vertices[:, 1] - cy, vertices[:, 0] - cx)
    sorted_indices = np.argsort(angles)
    vertices = vertices[sorted_indices]

    # Minimum width direction
    npoints = 361
    angle = np.linspace(0, 360, npoints)
    cosa = np.cos(np.deg2rad(angle))
    sina = np.sin(np.deg2rad(angle))
    rotMats = np.zeros((2, 2, npoints))
    for i in range(npoints):
        rotMats[:, :, i] = np.array([[cosa[i], sina[i]], [-sina[i], cosa[i]]])

    minwidth = np.inf
    mini = np.nan
    for i in range(npoints):
        # Compute rotation matrix to orient the convex hull with the main x-y
        # axis (this way it is easier to find the bounding box with the min and
        # max values of x/y)
        rotVertices = (rotMats[:, :, i] @ (vertices - [cx, cy]).T).T
        # Obtain width length of the rotated polygon
        maxx = np.max(rotVertices[:, 0])
        minx = np.min(rotVertices[:, 0])
        l = maxx - minx
        if l < minwidth:
            minwidth = l
            mini = i

    # Return minimum width direction
    thetamin = angle[mini]
    height = np.polyarea(x, y) / minwidth

    # Constrain angle between 0º and 180º
    if thetamin >= 180:
        thetamin -= 180

    axes = np.array([np.cos(np.deg2rad(thetamin)), np.sin(np.deg2rad(thetamin))])

    return thetamin, minwidth, height, axes