"""
A two dimensional lattice of infinitely long
cylindrical rods. Triangular with finite dimensions
"""

import meep as mp
from meep import materials

# Create the block of dielectric material
geometry = [mp.Block(mp.Vector3(10,10,mp.inf),
                     center=mp.Vector3(),
                     material=mp.Medium(epsilon=12))]
