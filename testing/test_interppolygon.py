"""
Test Script for interppolygon Function

This script tests the `interppolygon` function by applying it to a sample polygon
representing a region defined by longitude and latitude points. The script visualizes
the original and interpolated polygons on a 2D map for visual validation.

Author: [Your Name]
Date: [Current Date]
"""

# Import external modules
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Geod

# Import local modules
from mosaic_algorithms.auxiliar_functions.polygon_functions.interppolygon_gpt import interppolygon
from mosaic_algorithms.auxiliar_functions.polygon_functions.interppolygon_gptmini import interppolygon as interppolygon2


def interpm(lat, lon, distance):
    """
    Helper function that interpolates between consecutive latitude and longitude
    points based on a specified geodesic distance. Returns new latitude and longitude arrays.

    Parameters:
        - lat, lon: Arrays of latitude and longitude points defining a polygon.
        - distance: Desired distance in meters between interpolated points.

    Returns:
        - inter_lat, inter_lon: Interpolated arrays of latitude and longitude points.
    """
    geod = Geod(ellps="WGS84")
    inter_lat, inter_lon = [lat[0]], [lon[0]]

    for i in range(1, len(lat)):
        # Skip NaNs
        if np.isnan(lat[i]) or np.isnan(lon[i]):
            inter_lat.append(np.nan)
            inter_lon.append(np.nan)
            continue

        _, _, segment_distance = geod.inv(lon[i - 1], lat[i - 1], lon[i], lat[i])
        num_points = max(int(segment_distance // distance), 1)

        for j in range(1, num_points + 1):
            fraction = j / num_points
            inter_lon.append(lon[i - 1] * (1 - fraction) + lon[i] * fraction)
            inter_lat.append(lat[i - 1] * (1 - fraction) + lat[i] * fraction)

        inter_lon.append(lon[i])
        inter_lat.append(lat[i])

    return np.array(inter_lat), np.array(inter_lon)


def main():
    """
    Main function to test and visualize the interppolygon function.

    - Defines a simple polygon based on longitude and latitude.
    - Calls interppolygon to interpolate points along the polygon's edges.
    - Visualizes the original and interpolated polygons.
    """

    # Define a sample polygon (e.g., rough rectangle in degrees)
    roi0 = np.array([
        [-10.0, 40.0],
        [-10.0, 41.0],
        [-9.0, 41.0],
        [-9.0, 40.5],
        [-8.5, 40.2],
        [-8.0, 40.0],
        [-10.0, 40.0]  # Close the loop
    ])

    # Call the interppolygon function
    roi = interppolygon(roi0)

    # Call the interppolygon function
    roi2 = interppolygon2(roi0)

    # Visualization of original and interpolated polygons
    visualize_polygons(roi0, roi, roi2)


def visualize_polygons(roi0, roi, roi2):
    """
    Visualizes the original and interpolated polygons on a 2D map.

    Parameters:
    - roi0: Original Nx2 array of latitude and longitude points.
    - roi: Interpolated Nx2 array of latitude and longitude points.
    """

    # Plot original and interpolated polygons
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot original polygon
    ax.plot(roi0[:, 0], roi0[:, 1], 'o-', color="blue", label="Original Polygon")

    # Plot interpolated polygon
    ax.plot(roi[:, 0], roi[:, 1], 'x-', color="red", label="Interpolated Polygon")

    # Plot interpolated polygon
    ax.plot(roi2[:, 0], roi2[:, 1], 'v--', color="green", label="Interpolated Polygon Mini")

    # Labels and styling
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Original vs. Interpolated Polygon")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    # Show plot
    plt.show()


if __name__ == "__main__":
    main()
