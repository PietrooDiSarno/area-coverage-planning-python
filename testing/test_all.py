# ALL TESTING SCRIPTS AT ONCE
# RUN THIS FROM THE REPO ROOT FOLDER

# Import all the testing functions
from testing.test_boustrophedon import main as test_boustrophedon
from testing.test_closestSide import main as test_closestSide
from testing.test_closestSide2 import main as test_closestSide2
from testing.test_emissionang import main as test_emissionang
from testing.test_floodfill import main as test_floodfill
from testing.test_grid2D import main as test_grid2D
from testing.test_groundtrack import main as test_groundtrack
from testing.test_inst2topo import main as test_inst2topo
from testing.test_instpointing import main as test_instpointing
from testing.test_interppolygon import main as test_interppolygon
from testing.test_minimumWidthDirection import main as test_minimumWidthDirection
from testing.test_planSidewinderTour import main as test_planSidewinderTour
from testing.test_planSidewinderTour2 import main as test_planSidewinderTour2
from testing.test_trgobsvec import main as test_trgobsvec
from testing.test_visibleroi import main as test_visibleroi


# Main launch point
def main():

    # Launch all the functions
    test_boustrophedon()
    test_closestSide()
    test_closestSide2()
    test_emissionang()
    test_floodfill()
    test_grid2D()
    test_groundtrack()
    test_inst2topo()
    test_instpointing()
    test_interppolygon()
    test_minimumWidthDirection()
    # test_planSidewinderTour()
    # test_planSidewinderTour2()
    test_trgobsvec()
    test_visibleroi()


if __name__ == '__main__':
    main()
