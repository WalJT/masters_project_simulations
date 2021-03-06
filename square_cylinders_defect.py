"""
A two dimensional square lattice of infinitely long
cylindrical rods. Created following the MPB tutorial at
https://mpb.readthedocs.io/en/latest/Python_Tutorial/

modified to contain a point defect
"""

# import math
import meep as mp
from meep import mpb
# import numpy as np

import matplotlib.pyplot as plt

num_bands = 50

k_points = [mp.Vector3(),  # Gamma
            mp.Vector3(0.5),  # X
            mp.Vector3(0.5, 0.5),  # M
            mp.Vector3()]  # Gamma
# print k_points
# Add points inbetween the above points on the BZ
k_points = mp.interpolate(15, k_points)
# print k_points

dielectric_constant = 12  # of the rods

# Create an array of cylinders with different radii

resolution = 16  # Lattice constant is this many pixels

radii = (0.38, 0.4, 0.1, 0.2, 0.3, 0.5)  # Radii as a in units of a

for r in radii:

    ms = mpb.ModeSolver(num_bands=num_bands,
                        k_points=k_points,
                        # default_material=mp.Medium(epsilon=12), # Silicon-like material to contain air rods
                        resolution=resolution)

    # Set up the lattice with a pont defect
    ms.geometry_lattice = mp.Lattice(size=mp.Vector3(5, 5))
    ms.geometry = [mp.Cylinder(r, material=mp.Medium(epsilon=dielectric_constant))]
    ms.geometry = mp.geometric_objects_lattice_duplicates(ms.geometry_lattice, ms.geometry)
    ms.geometry.append(mp.Cylinder(r, material=mp.air))

    print("Square lattice of rods: TM bands")
    ms.run_tm()
    tm_freqs = ms.all_freqs
    tm_gaps = ms.gap_list

    print("Square lattice of rods: TE bands")
    ms.run_te()
    te_freqs = ms.all_freqs
    te_gaps = ms.gap_list

    md = mpb.MPBData(rectify=True, periods=3, resolution=resolution)
    eps = md.convert(ms.get_epsilon())
    plt.imshow(eps, interpolation='spline36', cmap='binary')
    plt.title("Radius = " + str(r) + "a")
    plt.show()
    # Plot both tm and te bands

    fig, ax = plt.subplots()
    x = range(len(tm_freqs))
    # Plot bands
    # Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
    for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
        ax.scatter([xz] * len(tmz), tmz, color='blue')
        # ax.scatter([xz] * len(tez), tez, color='red', facecolors='none')
    ax.plot(tm_freqs, color='blue')
    # ax.plot(te_freqs, color='red')
    ax.set_ylim([0, 1])
    ax.set_xlim([x[0], x[-1]])

    # Plot gaps
    for gap in tm_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1], gap[2], color='blue', alpha=0.2)

    for gap in te_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1], gap[2], color='red', alpha=0.2)

    # Plot labels
    ax.text(12, 0.04, 'TM bands', color='blue', size=15)
    # ax.text(13.05, 0.235, 'TE bands', color='red', size=15)

    points_in_between = (len(tm_freqs) - 4) / 3
    tick_locs = [i * points_in_between + i for i in range(4)]
    tick_labs = ['$\Gamma$', 'X', 'M', '$\Gamma$']
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labs, size=16)
    ax.set_ylabel('frequency (c/a)', size=16)
    ax.grid(True)
    plt.title("Radius = " + str(r) + "a")
    plt.show()

    with open("gap_list.out", "a") as gaps_output:
        gaps_output.write("TM Band Gaps for radius " + str(r) + "a:\n")
        gaps_output.write(str(tm_gaps))
        gaps_output.write("\nTE Band Gaps for radius " + str(r) + "a:\n")
        gaps_output.write(str(te_gaps))
        gaps_output.write("\n=======================================\n\n")
