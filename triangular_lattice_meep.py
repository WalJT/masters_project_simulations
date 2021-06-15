"""
A two dimensional lattice of infinitely long
cylindrical rods. Triangular with finite dimensions
Adapted from https://meep.readthedocs.io/en/latest/Python_Tutorials/Basics/
"""

import meep as mp
from meep import materials
import matplotlib.pyplot as plt

# Create a "Cell", the region in space
cell = mp.Vector3(12, 12, 0)

# Create the block of dielectric material
geometry = [mp.Block(mp.Vector3(10, 10, mp.inf),
                     center=mp.Vector3(),
                     material=mp.Medium(index=3.42))]

# Place a source
sources = [mp.Source(mp.ContinuousSource(frequency=1/0.4),
                     component=mp.Ez,
                     center=mp.Vector3(0, 0))]

# "Perfectly Matched Layers" (cell boundaries)
pml_layers = [mp.PML(1.0)]

# Resolution in pixels per micron
resolution = 10

# Create meep simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

# Run the simulation
sim.run(until=20)

# plot data using matplotlib
# First the dielectric
eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

# and then the field diagram
ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()
