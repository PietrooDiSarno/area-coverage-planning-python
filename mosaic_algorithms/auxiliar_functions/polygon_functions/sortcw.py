import numpy as np
from shapely.geometry import Polygon


def sortcw(*args):
    """
    Given a set of polygon vertices, this function sorts them in clockwise order.

    Programmers: Paula Betriu (UPC/ESEIAAT)
    Date: 10/2022

    Usage:
        x, y = sortcw(x, y)
        x, y, z = sortcw(x, y, z)

    Inputs:
    - x:    x rectangular coordinate (for 3 inputs) or longitude values (for 2 inputs).
            Units are irrelevant as long as the 2 or 3 arrays are consistent
    - y:    y rectangular coordinate (for 3 inputs) or latitude values (for 2 inputs).
            Units are irrelevant as long as the 2 or 3 arrays are consistent
    - z:    z rectangular coordinate (for 3 inputs)

    Returns:
    - Sorted inputs in clockwise order

    Note: 2D sorting algorithm does not work with concave algorithms. In such
    case, 3D rectangular coordinates are recommended.
    """
    if len(args) < 3:
        #  This algorithm consists of dividing the space in 4 quadrants,
        #  centered at the polygon centroid (any other inner point would be also
        #  valid). We calculate iteratively the angle with respect to that point
        #  and sort the vertices according to their respective angle value.
        #  This algorithm does not work with non-convex polygons
        x, y = args[0], args[1]

        points = list(zip(x, y))
        polygon = Polygon(points)
        centroid = polygon.centroid
        cx, cy = centroid.x, centroid.y # polygon centroid

        angle = np.arctan2(y - cy, x - cx)  # obtain angle
        ind = np.argsort(angle)[::-1]  # sort angles and get the indices
        x_sorted = np.array(x)[ind] # sort the longitude values according to the angle order
        y_sorted = np.array(y)[ind] # sort the latitude values according to the angle order
        return x_sorted, y_sorted # save output

    elif len(args) == 3:
        # Algorithm extracted from
        # https://stackoverflow.com/questions/47949485/
        # sorting-a-list-of-3d-points-in-clockwise-order
        x, y, z = args[0], args[1], args[2]
        innerpoint = np.array([np.mean(x), np.mean(y), np.mean(z)])  # find an inner point (this
        # is not the centroid but still works)

        i, j, k = np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])

        # Compute the cross products (perpendicular to the surface normal)
        pn = [np.cross(i, innerpoint), np.cross(j, innerpoint), np.cross(k, innerpoint)]

        # Choose the largest cross product to get vector p
        p = max(pn, key=np.linalg.norm)

        # Compute a second perpendicular vector q in the plane
        q = np.cross(innerpoint, p)

        # Now we have two perpendicular reference vectors in the plane given by
        # the normal. Take triple products of those, and these will be the sine
        # and the cosine of an angle that can be used for sorting
        angles = []
        for xi, yi, zi in zip(x, y, z):
            rmc = np.array([xi, yi, zi]) - innerpoint
            t = np.dot(innerpoint, np.cross(rmc, p))
            u = np.dot(innerpoint, np.cross(rmc, q))
            angle = np.arctan2(u, t)
            angles.append(angle)
            
        angles=np.array(angles)
        # Sort vertices by angles
        ind = np.argsort(angles)
        x_sorted = np.array(x)[ind]
        y_sorted = np.array(y)[ind]
        z_sorted = np.array(z)[ind]
        return x_sorted, y_sorted, z_sorted
    else:
        raise ValueError("Too many input arguments")