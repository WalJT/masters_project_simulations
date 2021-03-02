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
    R = np.linspace(0, 0.5, num=1e4)


square_circs()