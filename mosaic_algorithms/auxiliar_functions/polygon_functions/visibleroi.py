import numpy as np
import copy
from shapely.geometry import Polygon, Point
from mosaic_algorithms.auxiliar_functions.observation_geometry.emissionang import emissionang
from mosaic_algorithms.auxiliar_functions.polygon_functions.amsplit import amsplit
from conversion_functions import *

def visibleroi(roi, et, target, obs):
    """
        Given a target area (region-of-interest) on a planetary body surface and
        an observer, this function calculates the portion of the former that is
        visible.
        Note: if roi intercepts the anti-meridian line, this function returns
        the visible roi polygon divided by this line (see amsplit function).

        Programmers:  Paula Betriu (UPC/ESEIAAT)
                      Diego Andía  (UPC/ESEIAAT)
        Date:         06/2023

        Usage:        vroi = visibleroi(roi, et, target, obs)

        Inputs:
          > roi:     matrix containing the vertices of the ROI polygon. The
                     vertex points are expressed in 2D, in latitudinal
                     coordinates [º]
              # roi[:,1] correspond to the x values of the vertices
              # roi[:,2] correspond to the y values of the vertices
          > et:      limb projection time, in seconds past J2000 epoch
          > target:  string name of the target body (SPICE ID)
          > obs:     string name of the observer (SPICE ID)

        Output:
          > vroi:    matrix containing the vertices of the intersection between
                     the input ROI polygon and the limb projection, i.e., the
                     visible portion of the ROI on the body surface as seen from
                     the observer
        """

    # Previous anti-meridian intersection check...
    ind1 = np.where(np.diff(np.sort(roi[:, 0])) >= 180)[0]  # find the discontinuity index
    if ind1.size > 0:
        aux = amsplit(roi[:, 0], roi[:, 1])
        roi = copy.deepcopy(aux)

    # Parameters for mat2py_limbpt function
    flag = False  # assume the target area is visible from the instrument
    method = 'TANGENT/ELLIPSOID'
    _, targetframe, _ = mat2py_cnmfrm(target)  # body-fixed frame
    abcorr = 'LT+S'
    corloc = 'CENTER'
    refvec = np.array([0, 0, 1])  # first of the sequence of cutting half-planes
    ncuts = int(1e3)  # number of cutting half-planes
    delrol = mat2py_twopi() / ncuts  # angular step by which to roll the
    # cutting half-planes about the observer-target vector
    schstp = 1.0e-4  # search angular step size
    soltol = 1.0e-7  # solution convergence tolerance

    # Limb calculation with mat2py_limbpt function
    _, limb, _, _ = mat2py_limbpt(method, target, et, targetframe, abcorr,
                                   corloc, obs, refvec, delrol, ncuts, schstp, soltol, ncuts)  # limb points expressed in targetframe ref frame
    _, lblon, lblat = mat2py_reclat(limb)  # conversion from rectangular to latitudinal coordinates
    lblon = lblon * mat2py_dpr()
    lblat = lblat * mat2py_dpr()

    # Check for north/south pole
    northpole = False
    southpole = False
    # Check north-pole:
    srfpoint = np.array([0, 90])
    angle = emissionang(srfpoint, et, target, obs)
    if angle < 90:
        northpole = True
    # Check south-pole:
    srfpoint = np.array([0, -90])
    angle = emissionang(srfpoint, et, target, obs)
    if angle < 90:
        southpole = True

    # Case 1.
    if not northpole and not southpole:
        # Check a.m. split
        ind2 = np.where(np.diff(np.sort(lblon)) >= 180)[0]  # find the discontinuity
        if ind2.size > 0:
            lblon, lblat = amsplit(lblon, lblat)
        # Check if we are keeping the correct polygon (full disk polygons may be
        # misleading, we can only guarantee through emission angle check)
        exit = 0
        while exit == 0:
            randPoint = np.array([np.random.randint(-180, 181), np.random.randint(-90, 91)])
            if Polygon(list(zip(lblon, lblat))).contains(Point(randPoint[0],randPoint[1])):
                angle = emissionang(randPoint, et, target, obs)
                if angle < 85:
                    exit = 1
                    poly1 = Polygon((list(zip(lblon, lblat))))
            else:
                angle = emissionang(randPoint, et, target, obs)
                if angle < 85:
                    exit = 1
                    # This calculation is approximated, we should find a better way to find the complementary
                    # [Future work]
                    lonmap = np.array([-180, -180, 180, 180])
                    latmap = np.array([-90, 90, 90, -90])
                    polymap = Polygon(list(zip(lonmap, latmap)))
                    poly1 = Polygon(list(zip(lblon, lblat)))
                    poly1 = poly1.difference(polymap)
    else:
        # Case 2.
        lblon, indsort = np.sort(lblon), np.argsort(lblon)
        lblat = [lblat[i] for i in indsort]
        if northpole or southpole:
            # Include northpole to close polygon
            auxlon = lblon
            auxlat = lblat
            lblon = np.zeros(len(auxlon) + 2)
            lblat = np.zeros(len(auxlat) + 2)
            if northpole:
                lblon[0] = -180
                lblat[0] = 90
                lblon[-1] = 180
                lblat[-1] = 90
            else:
                lblon[0] = -180
                lblat[0] = -90
                lblon[-1] = 180
                lblat[-1] = -90
            lblon[1:-1] = auxlon
            lblat[1:-1] = auxlat
        poly1 = Polygon((list(zip(lblon, lblat))))

    # roi and limb intersection
    poly2 = Polygon((list(zip(roi[:, 0], roi[:, 1]))))
    inter = poly1.intersection(poly2)

    # output visible roi
    vroi = np.array(inter.exterior.coords)

    # visibility flag
    if len(vroi) == 0:
        flag = True

    return vroi, inter, flag
