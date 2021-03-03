"""
Script to calculate fill factors of various lattices
"""

import numpy as np
import matplotlib.pyplot as plt

def area_circle(r: [int, float]) -> float:
    """
    Calculates the area of a circle
    :param r: Radius of the Circle
    :return: Area of the circle
    """
    return np.pi * (r**2)


# Start with the square lattice of circles
def square_circs():
    """

    :return:
    """
    lattice_vector_length = 1
    square_area = lattice_vector_length**2

    radii = np.linspace(0, 0.5, int(1e4)) # end of range is close packed

    circle_areas, fill_factors = list(), list()
    i = 0
    for r in radii:
        circle_areas.append(area_circle(r))
        fill_factors.append(circle_areas[i])
        i += 1

    plt.plot(radii, fill_factors)
    plt.show()


square_circs()