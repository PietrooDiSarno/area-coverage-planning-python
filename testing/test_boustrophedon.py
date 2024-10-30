# This test will help verify that the function traverses the grid in the expected boustrophedon pattern
# and collects the non-empty coordinates accordingly.

# Import packages
from mosaic_algorithms.auxiliar_functions.grid_functions.boustrophedon_gpt import boustrophedon

# Sample grid with coordinates and None values
sample_grid = [
    [None, [1, 2], None],
    [[3, 4], None, [5, 6]],
    [None, [7, 8], None]
]

# Define directions
primary_direction = 'north'
secondary_direction = 'east'

# Call the function
coverage_tour = boustrophedon(sample_grid, primary_direction, secondary_direction)

# Output the result
print("Coverage Tour:", coverage_tour)
