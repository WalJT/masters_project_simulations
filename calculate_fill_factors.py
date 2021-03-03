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
    return np.pi * (r ** 2)


def volume_sphere(r: [int, float]) -> float:
    """
    Calculates the volume of a sphere given the radius
    :param r: radius
    :return: volume
    """
    return (4/3) * np.pi * (r**3)


# Start with the square lattice of circles
def square_circs(r: [int, float], a: [int, float]) -> float:
    """
    Calculates the packing fraction of a square lattice of circles
    This is applicable to infinitely long cylinders
    :param r: radius of the circle
    :param a: length of a the lattice vector
    :return: Packing fraction (complete fill is 1)
    """

    if r > a/2:
        print("The packing fraction is greater than close packed")
        return None
        # TODO: handle this case

    square_area = a ** 2
    circle_area = area_circle(r)

    packing_fraction = circle_area/square_area
    return packing_fraction


if __name__ == "__main__":
    radii = np.linspace(0, 1, int(1e4))
    fill_facts = list()
    for r in radii:
        fill_facts.append(square_circs(r, 1))

    plt.plot(radii, fill_facts)
    plt.show()
