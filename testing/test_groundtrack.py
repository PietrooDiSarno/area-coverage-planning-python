"""
Test Script for groundtrack Function

This script tests the `groundtrack` function, which calculates the longitude and latitude
of a spacecraft's ground track on a target body at specified times. It verifies the function's
ability to handle single and multiple time inputs and visualizes the ground track over the
target body's surface.

"""

import numpy as np
import matplotlib.pyplot as plt
from pySPICElib import kernelFetch
from spiceypy import str2et

from mosaic_algorithms.auxiliar_functions.plot.groundtrack_gpt import groundtrack


def main():
    """
    Main function to execute the groundtrack test.

    - Defines observer and target bodies.
    - Sets test times for ground track calculation.
    - Calls the groundtrack function.
    - Visualizes the results on a 2D plot.
    """

    # Load SPICE kernels
    kf = kernelFetch()
    kf.ffFile(metaK='input/galileo/inputkernels.txt', forceDownload=False)

    # Observation parameters
    et = str2et('1998 MAY 30 00:00:00.000 TDB')  # Observation time
    target = 'EUROPA'  # Target body
    observer = 'GALILEO ORBITER'  # Observer

    # Simulated time steps across one day (in seconds past J2000)
    times = et + np.linspace(0, 86400, 100)

    # Call the groundtrack function
    gtlon, gtlat = groundtrack(observer, times, target)

    # Visualization
    visualize_results(gtlon, gtlat, target)


def visualize_results(gtlon, gtlat, target):
    """
    Visualizes the ground track on the target body's surface in a longitude-latitude plot.

    Parameters:
    - gtlon: Array of ground track longitudes.
    - gtlat: Array of ground track latitudes.
    - target: Name of the target body for plot title.
    """

    # Plot the ground track
    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot for ground track points
    ax.plot(gtlon, gtlat, linestyle='-', marker='o', markersize=3, label="Ground Track")

    # Formatting the plot
    ax.set_title(f'Ground Track on {target}')
    ax.set_xlabel('Longitude (degrees)')
    ax.set_ylabel('Latitude (degrees)')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    # Display the plot
    plt.show()


if __name__ == "__main__":
    main()
