"""
A two dimensional lattice of infinitely long
cylindrical rods. Triangular with finite dimensions
Adapted from https://meep.readthedocs.io/en/latest/Python_Tutorials/Basics/
"""

import meep as mp
from meep import materials
import matplotlib.pyplot as plt
import numpy as np

# Define the materials to use
block_material = mp.Medium(index=3.42)
cylinder_material = mp.air
waveguide_material = block_material

# Create the block of dielectric material
block_x_width = 490
block_y_width = 600
# Create a "Cell", the region in space
cell = mp.Vector3(block_x_width+100, block_y_width+100, 0)
geometry = [mp.Block(mp.Vector3(block_x_width, block_y_width, mp.inf, ),
                     center=mp.Vector3(0, 0),
                     material=block_material)]

# Append cylinders objects to the "geometry variable"
cylinder_radius = 21.0
lattice_constant = 65.7
starting_corner = mp.Vector3(-(block_x_width / 2) + cylinder_radius, -(block_y_width / 2) + cylinder_radius)
points = [starting_corner]
number_of_cols = int(block_x_width / lattice_constant) + 2
number_of_rows = int(block_y_width / lattice_constant) + 2

# Create a triangular lattice
lattice_vectors = (mp.Vector3(lattice_constant, 0),
                   mp.Vector3(lattice_constant / 2, np.sqrt(3)*lattice_constant / 2),
                   mp.Vector3(-lattice_constant / 2, np.sqrt(3)*lattice_constant / 2))
for col in range(number_of_cols):
    for row in range(number_of_rows):
        if row == 0:
            new_point = points[row] + col * (lattice_vectors[0])
        else:
            if (row % 2) == 0:
                new_point = points[row] + (lattice_vectors[1]) + col * (lattice_vectors[0])
            else:
                new_point = points[row] + (lattice_vectors[2]) + col * (lattice_vectors[0])
        points.append(new_point)

    new_point = points[col] + (col * lattice_vectors[0]) - (col * lattice_vectors[1])
    points.append(new_point)

# print(number_of_cols)
# print(square_lattice_vectors)
# print(points)


for point in points:
    geometry.append(mp.Cylinder(radius=cylinder_radius, material=cylinder_material, center=point))

# Hollow structure center to place a source
# geometry.append(mp.Cylinder(radius=1, material=mp.air, center=mp.Vector3(0, 0)))

# Place a source
sources = [mp.Source(mp.ContinuousSource(frequency=1 / 210),  # 1/wavelength in microns
                     component=mp.Ez,
                     center=mp.Vector3((block_x_width+50)/2, 0, 0))]

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
resolution = 2

# Create meep simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

# Run the simulation
# sim.run(mp.at_beginning(mp.output_epsilon), mp.to_appended("ez", mp.at_every(0.05, mp.output_efield_z)),  until=10)
sim.run(until=10)

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
