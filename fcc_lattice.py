"""
The 3D Face Centered Cubic lattice is commonly used, as its
Brillouin Zone is close to spherical, and thus interactions
at similar wavelengths can be expected in all directions
"""
from typing import List

import numpy as np
import meep as mp
from meep import mpb, Vector3
import matplotlib.pyplot as plt

# Define the square root of 1/2:
sqrt_half = np.sqrt(1 / 2)

geometry_lattice = mp.Lattice(
    basis_size=mp.Vector3(sqrt_half, sqrt_half, sqrt_half),
    basis1=mp.Vector3(0, 1, 1),
    basis2=mp.Vector3(1, 0, 1),
    basis3=mp.Vector3(1, 1)
)

# Corners of the irreducible Brillouin zone for the fcc lattice,
# in a canonical order:
vlist = [
    mp.Vector3(0, 0.5, 0.5),  # X
    mp.Vector3(0, 0.625, 0.375),  # U
    mp.Vector3(0, 0.5, 0),  # L
    mp.Vector3(0, 0, 0),  # Gamma
    mp.Vector3(0, 0.5, 0.5),  # X
    mp.Vector3(0.25, 0.75, 0.5),  # W
    mp.Vector3(0.375, 0.75, 0.375)  # K
]

k_points = mp.interpolate(15, vlist)

# Define two dielectric materials, one for the background medium
# and one for the structure.
bulk_material = mp.Medium(epsilon=1)
atom_material = mp.Medium(epsilon=12)

# Place a sphere of dielectric material in the center of the unit cell
radius = 0.3  # relative to the lattice constant
geometry = [mp.Sphere(radius, material=atom_material)]

resolution = 16  # This will make the unit cell a 42x42x42 grid
# Reduce this number to increase computation speed

num_bands = 20

ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution,
                    mesh_size=5
)


def plot_bands(freqs):
    """
    Plot band structures
    :param freqs: value of ms.all_freqs after running
    """
    fig, ax = plt.subplots()
    x = range(len(freqs))
    # Plot bands
    # Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
    for xz, fz, in zip(x, freqs):
        ax.scatter([xz] * len(fz), fz, color='blue')
    ax.plot(freqs, color='blue')
    # ax.set_ylim([0, 1])
    # ax.set_xlim([x[0], x[-1]])

    plt.show()


def extract_epsilon():
    """
    Extracts dielectric function from global mode solver obj
    """
    eps = ms.get_epsilon()
    md = mpb.MPBData(rectify=True, periods=12, resolution=resolution)
    eps = md.convert(eps)
    for i in range(resolution):
        plt.imshow(eps[i], interpolation='spline36', cmap='binary')  # Plot a slice
        plt.show()


def do_calculations():
    """
    Run using global mode solver settings
    """
    ms.run()
    freqs = ms.all_freqs
    return freqs


if __name__ == "__main__":
    freqs = do_calculations()
    plot_bands(freqs)
    # ms.init_params()
    # extract_epsilon()
