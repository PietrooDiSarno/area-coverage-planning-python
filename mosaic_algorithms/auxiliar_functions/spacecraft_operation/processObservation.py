import numpy as np
from shapely.geometry import Polygon
import copy

from conversion_functions import mat2py_et2utc
from mosaic_algorithms.auxiliar_functions.spacecraft_operation.footprint import footprint
from mosaic_algorithms.auxiliar_functions.spacecraft_operation.slewDur import slewDur
def processObservation(A, tour, fpList, poly1, t, slewRate, tobs, amIntercept, inst, sc, target, resolution):
    """
    This function handles the processing of an observation point by computing
    its footprint, updating the list of completed observations and adjusting
    the remaining area to be covered. It also accounts for anti-meridian
    interception and updates the time for the next observation based on slew
    rate and observation time.

    Programmers:  Paula Betriu (UPC/ESEIAAT)
    Date:         09/2023

    Usage:        A, tour, fpList, poly1,t = processObservation(A, tour,
                  fpList, poly1, t, slewRate, tobs, amIntercept, inst sc, target,
                  resolution)

    Inputs:
      > A:           list of lists of successive instrument observations,
                     sorted in chronological order.
                     Each observation is defined by the instrument boresight
                     projection onto the body surface, in latitudinal
                     coordinates [lon lat], in deg
     > tour:         array of remaining observation points in the tour, in
                     latitudinal coordinates [º]
     > fpList:       list of footprint structures detailing the observation
                     metadata and coverage
     > poly1:        current polygon shape of the uncovered area on the
                     target body
     > t:            current time in ephemeris seconds past J2000 epoch
     > slewRate:     rate at which the spacecraft (or instrument platform)
                     can slew between observations, in [º/s]
     > tobs:         observation time, i.e. the minimum time that the
                     instrument needs to perform an observation, in seconds
     > amIntercept:  boolean flag indicating if the anti-meridian is
                     intercepted by the observation path
     > inst:         string name of the instrument
     > sc:           string name of the spacecraft
     > target:       string name of the target body
     > resolution:   string defining the resolution setting, affecting the
                     footprint calculation. It could be either 'lowres' or
                     'highres'. See footprint function for further
                     information

    Returns:
      > A, tour, fpList, poly1, t: updated variables

    """

    # Previous check...
    if not tour:
        return A, tour, fpList, poly1, t, True

    # Compute the footprint of each point in the tour successively and
    # subtract the corresponding area from the target polygon
    a = copy.deepcopy(tour[0]) # observation
    tour[0] = [] #delete this observation from the planned tour
    empty = False

    # Check an.m. intercept...
    if a[0] > 180:
        a[0] -= 360

    # Compute the observation's footprint
    print(f"Computing {inst} FOV projection on {target} at {mat2py_et2utc(t, 'C', 0)}...")
    fprinti = footprint(t, inst, sc, target, resolution, a[0], a[1], 0)

    # Body-fixed to inertial frame
    if fprinti['bvertices']:  # assuming 'fprinti' is a dictionary with 'bvertices' key
        print("\n")

        # Check a.m. intercept
        if amIntercept:
            aux = copy.deepcopy(fprinti)
            ind = aux['bvertices'][:,1] < 0
            aux['bvertices'][ind,0] += 360
            poly2 = Polygon(aux['bvertices'])
        else:
            poly2 = Polygon(fprinti['bvertices']) #create footprint polygon

        # Check footprint-ROI intersect
        targetpshape = copy.deepcopy(poly1)
        areaT = targetpshape.area
        inter = targetpshape.difference(poly2)
        areaI = inter.area
        areaInter = areaT - areaI
        fpArea = poly2.area

        if areaInter / fpArea == 0:
            empty = True
        else:
            A.append(a)  # add it in the list of planned observations
            poly1 = poly1.difference(poly2)  # update uncovered area

            # Save footprint struct
            fpList.append(fprinti)

            # New time iteration
            if tour:
                p1 = [fprinti['olon'], fprinti['olat']]
                p2 = [tour[0][0], tour[0][1]]
                t += tobs + slewDur(p1, p2, t, tobs, inst, target, sc, slewRate)
    else:
        empty = True

    if empty:
        print(" Surface not reachable\n")

    return A, tour, fpList, poly1, t, empty