import numpy as np
from shapely.geometry import Polygon
from mosaic_algorithms.auxiliar_functions.polygon_functions.sortcw import  sortcw


def amsplit(x, y):
    """
    Provided the vertices of a polygon in latitudinal coordinates, this
    function analyzes if the polygon intercepts the anti-meridian line and,
    in that case, divides the polygon by this line.

    Programmers:  Paula Betriu (UPC/ESEIAAT)
    Date:         10/2022

    Usage:        [xf, yf] = amsplit(x, y)

    Inputs:
      > x:        array of longitude values in [deg]. x ∈ [-180, 180]
      > y:        array of latitude values in [deg]. y ∈ [-90, 90]

    Outputs:
      > x:        array of longitude values in [deg]. In case the polygon
                  intercepts the a.m. line, then the longitude values of the
                  polygon are separated by a NaN value. x ∈ [-180, 180]
      > y:        array of latitude values in [deg]. In case the polygon
                  intercepts the a.m. line, then the latitude values of the
                  polygon are separated by a NaN value. y ∈ [-90, 90]
    """
    # [To be resolved]: If polygon longitude size is 180º, the function does
    # nothing.
    if (np.max(x) - np.min(x)) == 180:
        print("Full longitude. This function does nothing, in this case." +
              "The user must check if the polygon is well defined!")

    # Previous check...
    if (np.max(x) - np.min(x)) <= 180:
        xf = x
        yf = y
        return xf, yf

    # In case the polygon indeed intercepts this line, then we're going to
    # calculate the intercept points by computing the intersection between two
    # polygons: the input polygon and another one which corresponds to the
    # anti-meridian line (actually, it's a small polygon because the 'intersect'
    # function does not operate well with lines)
    x[x < 0] = x[x < 0] + 360  # continuous polygon
    poly1 = Polygon(zip(x, y))
    vpoly2 = np.vstack((np.column_stack((180 * np.ones(20), np.linspace(-90, 90, 20))),
                        np.column_stack((181 * np.ones(20), np.linspace(90, -90, 20)))))
    poly2 = Polygon(vpoly2)

    # Compute the intersection points
    polyinter = poly1.intersection(poly2)
    xinter, yinter = polyinter.exterior.xy

    # Only keep the anti-meridian intercepts
    yi = yinter[np.abs(xinter - 180) < 1e-2]
    xi = 180 * np.ones(len(yi))

    # Define the new polygon
    P = np.column_stack((x, y))

    # Add the intersection points to the polygon vertices
    P = np.vstack((P, np.column_stack((xi, yi))))

    # Split the polygon in two, cleaved by the anti-meridian line
    x = np.sort(P[:, 0])
    P = P[np.argsort(P[:, 0])]
    poly1 = P[x >= 180, :]  # this is the polygon that falls in negative lon.
    poly2 = P[x <= 180, :]  # this is the polygon that falls in positive lon.

    # Sort the polygon vertices in clockwise order...
    poly1[:, 0], poly1[:, 1] = sortcw(poly1[:, 0], poly1[:, 1])
    poly2[:, 0], poly2[:, 1] = sortcw(poly2[:, 0], poly2[:, 1])

    # Retrieve the original values (longitude values cannot be >180º in our system) and output the final vertices
    xf = poly1[:, 0] - 360
    xf = np.append(xf, [np.nan])
    xf = np.append(xf, poly2[:, 0])

    yf = poly1[:, 1]
    yf = np.append(yf, [np.nan])
    yf = np.append(yf, poly2[:, 1])

    # [Future work]: Consider polygons that are split by the a.m. but also are
    # discontinuous in latitude (i.e., more than two polygons)
    # yi = sorted(yi, reverse=True)
    # if len(xi) / 2 > 1:
    #     for j in range(len(yi)):
    #         # Get inner intersections
    #         if yi[j] > min(yi) and yi[j] < max(yi):
    #             # To determine whether the intersection should be included in the left or
    #             # right sides of the a.m. we need to check the immediately upper and
    #             # lower points
    #             poly3 = Polygon()
    #             if Polygon(poly2).contains(Point(180, yi[j] + 1)):
    #                 # Split poly1
    #                 ind = (x >= 180) & (y >= yi[j])  # poly1[:, 1] >= yi[j]
    #                 spoly1 = sortcw(poly1[ind, 0], poly1[ind, 1])
    #                 poly3 = addboundary(poly3, spoly2)
    #             else:
    #                 # Split poly2
    #                 pass

    return xf, yf