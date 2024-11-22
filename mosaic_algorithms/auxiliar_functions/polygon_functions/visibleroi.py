import numpy as np
import copy
from shapely.geometry import MultiPolygon, Polygon, Point
from mosaic_algorithms.auxiliar_functions.observation_geometry.emissionang import emissionang
from mosaic_algorithms.auxiliar_functions.polygon_functions.amsplit import amsplit
from conversion_functions import *

def visibleroi(roi_, et, target, obs):
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
    roi = copy.deepcopy(roi_)
    # Previous anti-meridian intersection check...
    ind1 = np.where(np.diff(np.sort(roi[:, 0])) >= 180)[0]  # find the discontinuity index
    if ind1.size > 0:
        col1, col2 = amsplit(roi[:, 0], roi[:, 1])
        roi = np.hstack((col1.reshape(len(col1),1),col2.reshape(len(col2),1)))

    # Parameters for mat2py_limbpt function
    flag = False  # assume the target area is visible from the instrument
    method = 'TANGENT/ELLIPSOID'
    _, targetframe, _ = mat2py_cnmfrm(target)  # body-fixed frame
    abcorr = 'XLT+S'
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

    ind2 = np.where(np.diff(np.sort(lblon)) >= 180)[0]
    if ind2.size > 0:
        lblon, lblat = amsplit(lblon, lblat)

    # roi and limb intersection
    if (np.isnan(lblon)).any():
        nanindex = np.where(np.isnan(lblon))[0][0]
        poly1 = MultiPolygon([Polygon(list(zip(lblon[:nanindex], lblat[:nanindex]))),
                                Polygon(list(zip(lblon[nanindex + 1:], lblat[nanindex + 1:])))])
    else:
       poly1 = Polygon(list(zip(lblon, lblat)))
    poly1 = poly1.buffer(0)

    if (np.isnan(roi[:,0])).any():
        nanindex = np.where(np.isnan(roi[:,0]))[0]
        polygon_list = []
        for i in range(len(nanindex)):
            if i==0:
                polygon_list.append(Polygon(list(zip(roi[:nanindex[0],0], roi[:nanindex[0],1]))))
            else:
                polygon_list.append(Polygon(list(zip(roi[nanindex[i-1]+1:nanindex[i],0], roi[nanindex[i-1]+1:nanindex[i],1]))))
        if ~ np.isnan(roi[-1,0]):
            polygon_list.append(Polygon(list(zip(roi[nanindex[-1] + 1:, 0], roi[nanindex[-1] + 1:, 1]))))
        poly2 = MultiPolygon(polygon_list)
    else:
        poly2 = Polygon((list(zip(roi[:, 0], roi[:, 1]))))
    poly2 = poly2.buffer(0)

    inter = (poly1.intersection(poly2)).buffer(0)

    # output visible roi
    if isinstance(inter, Polygon):
        vroi = np.array(inter.exterior.coords)
    elif isinstance(inter, MultiPolygon):
        for i in range(len(inter.geoms)):
            if i == 0:
                vroi = np.vstack((np.array(inter.geoms[i].exterior.coords), [np.nan, np.nan]))
            else:
                vroi = np.vstack((vroi, np.array(inter.geoms[i].exterior.coords), [np.nan, np.nan]))
        vroi = vroi[:-1,:]

    # visibility flag
    if vroi.size == 0:
         flag = True

    return vroi, inter, flag

