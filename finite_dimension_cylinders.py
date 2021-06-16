"""
A two dimensional lattice of infinitely long
cylindrical rods. Triangular with finite dimensions
Adapted from https://meep.readthedocs.io/en/latest/Python_Tutorials/Basics/
"""

import meep as mp
from meep import materials
import matplotlib.pyplot as plt
import numpy as np

# Create a "Cell", the region in space
cell = mp.Vector3(20, 20, 0)

# Create the block of dielectric material
block_width = 10
geometry = [mp.Block(mp.Vector3(block_width, block_width, mp.inf,),
                     center=mp.Vector3(0, 0),
                     material=mp.Medium(index=3.42))]

# Append air cylinders objects to the "geometry variable"
cylinder_material = mp.air
cylinder_radius = 0.2
lattice_constant = 0.5
starting_corner = mp.Vector3(-(block_width/2)+cylinder_radius, -(block_width/2)+cylinder_radius)
points = [starting_corner]

number_of_points = int(block_width / lattice_constant)
y_loc = starting_corner.y
for i in range(number_of_points):
    new_y = y_loc + lattice_constant
    for n in range(number_of_points):
        new_x = points[n].x + lattice_constant
        points.append(mp.Vector3(new_x, new_y))
    y_loc += lattice_constant

for point in points:
    geometry.append(mp.Cylinder(radius=cylinder_radius, material=cylinder_material, center=point))

# Place a source
sources = [mp.Source(mp.ContinuousSource(frequency=1/0.4),
                     component=mp.Ez,
                     center=mp.Vector3(7, 0, 0))]

# "Perfectly Matched Layers" (cell boundaries)
pml_layers = [mp.PML(1.0)]

# Resolution in pixels per micron
resolution = 75

# Create meep simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

# Run the simulation
sim.run(mp.at_beginning(mp.output_epsilon), mp.to_appended("ez", mp.at_every(0.05, mp.output_efield_z)),  until=120)
# sim.run(until=70)

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
