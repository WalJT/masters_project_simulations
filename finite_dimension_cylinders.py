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
cell = mp.Vector3(500, 600, 0)

# Define the materials to use
block_material = mp.Medium(index=3.42)
cylinder_material = mp.air
waveguide_material = block_material

# Create the block of dielectric material
block_width = 490
geometry = [mp.Block(mp.Vector3(block_width, block_width, mp.inf,),
                     center=mp.Vector3(0, 0),
                     material=block_material)]

# Append cylinders objects to the "geometry variable"
cylinder_radius = 21.0
lattice_constant = 65.7
starting_corner = mp.Vector3(-(block_width/2)+cylinder_radius, -(block_width/2)+cylinder_radius)
points = [starting_corner]
number_of_cols = int(block_width / lattice_constant)
number_of_rows = int(block_width / lattice_constant)

square_lattice_vectors = (mp.Vector3(lattice_constant, 0), mp.Vector3(0, lattice_constant))

for col in range(number_of_cols):
    for row in range(number_of_rows):
        new_point = points[row] + (square_lattice_vectors[1]) + col*(square_lattice_vectors[0])
        points.append(new_point)
    new_point = points[col] + (col*square_lattice_vectors[0]) - (col*square_lattice_vectors[1])
    points.append(new_point)

print(number_of_cols)
print(square_lattice_vectors)
print(points)

for point in points:
    geometry.append(mp.Cylinder(radius=cylinder_radius, material=cylinder_material, center=point))

# Hollow structure center to place a source
# geometry.append(mp.Cylinder(radius=1, material=mp.air, center=mp.Vector3(0, 0)))

# Place a source
sources = [mp.Source(mp.ContinuousSource(frequency=1/210),  # 1/wavelength in microns
                     component=mp.Ez,
                     center=mp.Vector3(0, -250, 0))]

# Add a waveguide
# wg1 = mp.Block(mp.Vector3(block_width/2 - 1, 1.2, mp.inf),
#                center=mp.Vector3(block_width/4 + 0.5, 0),
#                material=waveguide_material)
# wg1 = mp.Block(mp.Vector3(block_width/4, 1.2, mp.inf),
#                center=mp.Vector3(block_width/8 + 1, 0),
#                material=waveguide_material)
# wg2 = mp.Block(mp.Vector3(1.2, block_width/2, mp.inf),
#                center=mp.Vector3(block_width/4 + 0.5, block_width/4),
#                material=waveguide_material)
#
# geometry.append(wg1)
# geometry.append(wg2)

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
# sim.run(mp.at_beginning(mp.output_epsilon), mp.to_appended("ez", mp.at_every(0.05, mp.output_efield_z)),  until=70)
sim.run(until=5)

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
