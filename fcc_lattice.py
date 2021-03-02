"""
The 3D Face Centered Cubic lattice is commonly used, as its
Brillouin Zone is close to spherical, and thus interactions
at similar wavelengths can be expected in all directions
"""

from math import sqrt
import meep as mp
from meep import mpb

import matplotlib.pyplot as plt

# Define the square root of 1/2:
sqrt_half = sqrt(1 / 2)

sqrt_half = math.sqrt(0.5)
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

k_points = mp.interpolate(20, vlist)

# Define two dielectric materials, one for the background medium
# and one for the structure.
bulk_material = mp.Medium(epsilon=1) # air
atom_material = mp.Medium(epsilon=12) # A silicon-like material

# Place a sphere of dielectric material in the center of the unit cell
radius = 0.1 # 0.1 times the lattice constant
geometry = [mp.Sphere(radius, material=atom_material)]

resolution = 42 # This will make the unit cell a 42x42x42 grid
# Reduce this number to increase computation speed
