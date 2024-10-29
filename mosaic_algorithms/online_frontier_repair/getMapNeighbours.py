import numpy as np


def getMapNeighbours(indrow, indcol, map, search='all'):
    """
    Given a grid of points (2D list) and an element, this function outputs the neighboring points
    of the current point in the matrix.

    Programmers:  Paula Betriu (UPC/ESEIAAT)
    Date:         09/2022
    Last Rev.:    06/2023

    Usage:        n = getMapNeighbours(indrow, indcol, map)
                  n = getMapNeighbours(indrow, indcol, map, search)

    Inputs:
      > indrow:       int row index of the matrix element (grid point)
      > indcol:       int column index of the matrix element (grid point)
      > map:          2D list of grid points. In order to avoid
                      mapping boundaries, map is bounded by NaN rows and
                      columns (first and last)
      > search:       string that defines if the function shall differentiate
                      between 'cardinal' and 'diagonal' searches. Otherwise,
                      the 8 adjacent points are visited

    Returns:
      > n:            2D list with the non-NaN neighbouring points in
                      the map
    """

    # Previous checks...
    # Searching element is not in the boundaries
    if indrow == 0 or indrow == len(map) - 1 or indcol == 0 or indcol == len(map[0]) - 1:
       raise ValueError("Searching element cannot be in the map boundaries")
    # Future work: check if first and last rows and columns are NaN

    # Initialize the list to hold neighboring points
    aux_n = [None] * 8  # Preallocate for up to 8 neighbors

    # Search neighbors of the given element in the map
    if map[indrow][indcol] is not None and not any(np.isnan(map[indrow][indcol])):
        if search == 'all':
            aux_n[0] = map[indrow - 1][indcol + 1]  # northeast
            aux_n[1] = map[indrow][indcol + 1]      # east
            aux_n[2] = map[indrow + 1][indcol + 1]  # southeast
            aux_n[3] = map[indrow - 1][indcol]      # north
            aux_n[4] = map[indrow + 1][indcol]      # south
            aux_n[5] = map[indrow - 1][indcol - 1]  # northwest
            aux_n[6] = map[indrow][indcol - 1]      # west
            aux_n[7] = map[indrow + 1][indcol - 1]  # southwest

        elif search == 'cardinal':
            aux_n[0] = map[indrow - 1][indcol]  # north
            aux_n[1] = map[indrow][indcol + 1]  # east
            aux_n[2] = map[indrow + 1][indcol]  # south
            aux_n[3] = map[indrow][indcol - 1]  # west

        elif search == 'diagonal':
            aux_n[0] = map[indrow - 1][indcol - 1]  # northwest
            aux_n[1] = map[indrow - 1][indcol + 1]  # northeast
            aux_n[2] = map[indrow + 1][indcol + 1]  # southeast
            aux_n[3] = map[indrow + 1][indcol - 1]  # southwest

    # Output neighbours (not empy nor NaN)
    n = [neighbor for neighbor in aux_n if neighbor is not None and not any(np.isnan(neighbor))]

    return n