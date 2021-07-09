"""
A two dimensional lattice of infinitely long
cylindrical rods. Triangular with finite dimensions
Adapted from https://meep.readthedocs.io/en/latest/Python_Tutorials/Basics/
"""
import sys

import meep as mp
from meep import materials
import matplotlib.pyplot as plt
import numpy as np
import lattices

# Define the materials to use, and other parameters
block_material = materials.Si
cylinder_material = mp.Medium(epsilon=3.61)
# waveguide_material = block_material
pml_thickness = 5
lattice_constant = 1
cylinder_radius = 0.3*lattice_constant
block_x_width = np.ceil(20*lattice_constant)
block_y_width = 10
resolution = 40  # Resolution in pixels per micron
polarization = "tm"  # "tm" or "te"

if polarization == "te":
    source_component = mp.Ez
    plot_component = mp.Ez
elif polarization == "tm":
    source_component = mp.Ey
    plot_component = mp.Bz
else:
    print("unknown or no polarisation")
    sys.exit(1)

# Current source information
fcen = 0.61 # (Center) frequency; 1/wavelength in microns
df = 0.6  # pulse frequency width (for Gaussian Sources)
source_x_loc = -(block_x_width/2 + 10)
source_y_loc = 0

# Create the block of dielectric material
# Create a "Cell", the region in space
cell = mp.Vector3(block_x_width+50, block_y_width+0.5*pml_thickness, 0)
geometry = [mp.Block(mp.Vector3(block_x_width, block_y_width, mp.inf),
                     center=mp.Vector3(0, 0),
                     material=block_material)]
# geometry = []

# Append cylinders objects to the "geometry variable"

starting_corner = mp.Vector3(-(block_x_width / 2) + cylinder_radius, -(block_y_width / 2) + cylinder_radius)
number_of_cols = int(block_x_width / lattice_constant)
number_of_rows = int(block_y_width / lattice_constant) + 3

# Create a square lattice
for point in lattices.triangular(lattice_constant, number_of_rows, number_of_cols, starting_corner):
    geometry.append(mp.Cylinder(radius=cylinder_radius, material=cylinder_material, center=point))

# Place a source use a gaussian source and get a transmission spectrum
# (https://meep.readthedocs.io/en/latest/Python_Tutorials/Resonant_Modes_and_Transmission_in_a_Waveguide_Cavity/)
# geometry.append(mp.Cylinder(material=mp.air, radius=300, center=mp.Vector3(0, 0)))
sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df),
                     component=source_component,
                     size=mp.Vector3(0, 2*lattice_constant),
                     center=mp.Vector3(source_x_loc, source_y_loc, 0))]

# Add a waveguide
# wg1 = mp.Block(mp.Vector3(block_y_width/2 - 1, 50, mp.inf),
#                center=mp.Vector3(block_x_width/4 + 200, 0),
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
pml_layers = [mp.PML(pml_thickness)]

# Create meep simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

flux_plane = mp.Vector3(-source_x_loc, source_y_loc)
freg = mp.FluxRegion(center=flux_plane,
                     size=mp.Vector3(0, 40))

nfreq = 1000  # number of frequencies at which to compute flux

# transmitted flux
trans = sim.add_flux(fcen, df, nfreq, freg)

# Run the simulation
sim.run(mp.at_beginning(mp.output_epsilon), mp.to_appended("ez", mp.at_every(0.1, mp.output_bfield_z)),  until=100)
# sim.run(until_after_sources=mp.stop_when_fields_decayed(50, plot_component, flux_plane, 1e-3))
# sim.run(until=100)
# sim.display_fluxes(trans)

# Get the frequencies and flux values
flux_freqs = mp.get_flux_freqs(trans)
fluxes = mp.get_fluxes(trans)
plt.plot(flux_freqs, fluxes)
plt.show()

with open("out.txt", "w") as file:
    file.write("Freqs\n")
    for freq in flux_freqs:
        file .write(str(freq)+"\n")
    file.write("Flux\n")
    for flux in fluxes:
        file.write(str(flux)+"\n")


# plot data using matplotlib
# First the dielectric
eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

# and then the field diagram
ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=plot_component)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()
