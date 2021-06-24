"""
A two dimensional lattice of infinitely long
cylindrical rods. Triangular with finite dimensions
Adapted from https://meep.readthedocs.io/en/latest/Python_Tutorials/Basics/
"""

import meep as mp
from meep import materials
import matplotlib.pyplot as plt
import numpy as np
import lattices

# Define the materials to use
block_material = mp.Medium(index=3.42)
cylinder_material = mp.air
waveguide_material = block_material

# Create the block of dielectric material
block_x_width = 2000
block_y_width = 500
# Create a "Cell", the region in space
cell = mp.Vector3(block_x_width + 200, block_y_width + 100, 0)
geometry = [mp.Block(mp.Vector3(block_x_width, block_y_width, mp.inf, ),
                     center=mp.Vector3(0, 0),
                     material=block_material)]

# Append cylinders objects to the "geometry variable"
cylinder_radius = 21.0
lattice_constant = 65.7
starting_corner = mp.Vector3(-(block_x_width / 2) + cylinder_radius, -(block_y_width / 2) + cylinder_radius)
number_of_cols = int(block_x_width / lattice_constant)
number_of_rows = int(block_y_width / lattice_constant)

# Create a triangular lattice
for point in lattices.square(lattice_constant, number_of_rows, number_of_cols, starting_corner):
    geometry.append(mp.Cylinder(radius=cylinder_radius, material=cylinder_material, center=point))

# Place a source
# use a gaussian source and get a transmission spectrum (https://meep.readthedocs.io/en/latest/Python_Tutorials/Resonant_Modes_and_Transmission_in_a_Waveguide_Cavity/)
fcen = 1/300  # Center frequency
df = 1/100    # pulse frequency width
sources = [mp.Source(mp.ContinuousSource(fcen),  # 1/wavelength in microns
                     component=mp.Ez,
                     size=mp.Vector3(0, 0),
                     center=mp.Vector3((block_x_width+100) / 2, 0, 0))]

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
resolution = 1

# Create meep simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

flux_plane = mp.Vector3(-(block_x_width/2 + 50))
freg = mp.FluxRegion(center=flux_plane,
                     size=mp.Vector3(0, 40))

# nfreq = 500  # number of frequencies at which to compute flux

# transmitted flux
# trans = sim.add_flux(fcen, df, nfreq, freg)

# Run the simulation
# sim.run(mp.at_beginning(mp.output_epsilon), mp.to_appended("ez", mp.at_every(1, mp.output_efield_z)),  until=5000)
# sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, flux_plane, 1e-3))
sim.run(until=5000)
# sim.display_fluxes(trans)
# transmitted_flux = mp.get_fluxes(trans)
# flux_freqs = mp.get_flux_freqs(trans)
# plt.plot(flux_freqs, transmitted_flux)
# plt.show()

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
