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
    return np.pi * (r^2)


# Start with the square lattice of circles
def square_circs():
    """

    :return:
    """
    radii = np.linspace(0, 1e4, 0.5)

    i = 0
    areas = np.array()
    for r in radii:
        areas[i] = area_circle(r)
        i += 1

    plt.plot(radii, areas)
    plt.show()


square_circs()