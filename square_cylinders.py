"""
A two dimensional square lattice of infinitely long
cylindrical rods. Created following the MPB tutorial at
https://mpb.readthedocs.io/en/latest/Python_Tutorial/
"""

# import math
import meep as mp
from meep import mpb
import numpy as np
import matplotlib.pyplot as plt

# Define points on the irreducible BZ
k_points = [mp.Vector3(),  # Gamma
            mp.Vector3(0.5),  # X
            mp.Vector3(0.5, 0.5),  # M
            mp.Vector3()]  # Gamma

# Important parameters to be passed to the mode solver
geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1))
num_bands = 8
k_points = mp.interpolate(20, k_points)
rods_material = mp.Medium(epsilon=1)
bulk_material = mp.Medium(epsilon=3.6)
resolution = 50  # Lattice constant is this many pixels
radius = 0.2  # radius of the cylinders
geometry = [mp.Cylinder(radius, material=rods_material)]

# Create the ModeSolver
ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    default_material=bulk_material,
                    resolution=resolution)


def do_calculations(polarization: str):
    """
    Run MPB using the global modesolver
    :param polarization: tm or te
    :return: bands (array)
    """
    if polarization == "tm":
        print("Running for Transverse Magnetic Polarisation:")
        ms.run_tm()
    elif polarization == "te":
        print("Running for Transverse Electric Polarisation:")
        ms.run_te()
    else:
        print("Unrecognised Polarisation")
        return None

    return ms.all_freqs


def display_lattice():
    md = mpb.MPBData(periods=3, resolution=resolution, rectify=True)
    eps = md.convert(ms.get_epsilon())
    plt.imshow(eps)
    plt.show()


def plot_bands(bands):
    x = range(len(bands))

    # Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
    # Used to plot frequencies in all bands at each k-point
    for xz, bandz in zip(x, bands):
        plt.scatter([xz] * len(bandz), bandz, color="blue")

    plt.plot(bands, color="blue")  # Plot lines, so we have a continuous representation

    # Label axes:
    plt.ylabel("Frequency, c/a")
    points_in_between = (len(bands) - 4) / 3  # Number of points in between BZ corners
    tick_locations = [i * points_in_between + i for i in range(4)]


    plt.show()


if __name__ == "__main__":
    frequencies = do_calculations("te")
    plot_bands(frequencies)
    display_lattice()

"""
for r in radii:
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
"""
