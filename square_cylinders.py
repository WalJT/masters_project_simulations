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


def do_calculations(ms: mpb.ModeSolver, polarization: str):
    """
    Run MPB using the global modesolver
    :param ms: MPB Mode Solver Object
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

    return ms.all_freqs, ms.gap_list


def display_lattice():
    md = mpb.MPBData(periods=3, resolution=resolution, rectify=True)
    eps = md.convert(ms.get_epsilon())
    # Show low dielectric constant as white, and high as black
    plt.imshow(eps, interpolation='spline36', cmap='binary')
    plt.show()


def plot_bands(bands, gaps):
    fig, ax = plt.subplots()  # We need ax in order to modify the tick labels

    x = range(len(bands))

    # Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
    # Used to plot frequencies in all bands at each k-point
    for xz, bandz in zip(x, bands):
        ax.scatter([xz] * len(bandz), bandz, color="blue")

    ax.plot(bands, color="blue")  # Plot lines, so we have a continuous representation

    # Label axes:
    plt.ylabel("Frequency, c/a")
    points_in_between = (len(bands) - 4) / 3  # Number of points in between BZ corners
    tick_locations = [i * points_in_between + i for i in range(4)]
    ax.set_xticks(tick_locations)

    tick_labels = ["Gamma", "X", "M", "Gamma"]
    ax.set_xticklabels(tick_labels)

    # Plot any complete band gaps that were found
    for gap in gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1], gap[2], color="blue", alpha=0.1)

    plt.show()


def set_up_lattice():
    """
    Returns geometry_lattice; A Lattice object with specified lattice vectors, and
    geometry; objects that make up the basis of the crystal
    """
    geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1))
    geometry = [mp.Cylinder(radius, material=rods_material)]
    return geometry_lattice, geometry


def output_gap_list(gaps):
    pass  # TODO


if __name__ == "__main__":
    # Define points on the irreducible BZ
    k_points = [mp.Vector3(),  # Gamma
                mp.Vector3(0.5),  # X
                mp.Vector3(0.5, 0.5),  # M
                mp.Vector3()]  # Gamma

    # Important parameters to be passed to the mode solver

    num_bands = 8
    k_points = mp.interpolate(20, k_points)
    rods_material = mp.Medium(epsilon=12)
    bulk_material = mp.Medium(epsilon=1)
    resolution = 50  # Lattice constant is this many pixels
    radius = 0.2  # radius of the cylinders

    geometry_lattice, geometry = set_up_lattice()

    # Create the ModeSolver
    ms = mpb.ModeSolver(num_bands=num_bands,
                        k_points=k_points,
                        geometry=geometry,
                        geometry_lattice=geometry_lattice,
                        default_material=bulk_material,
                        resolution=resolution)

    band_frequencies, band_gaps = do_calculations(ms, "tm")
    plot_bands(band_frequencies, band_gaps)
    display_lattice()

"""
    with open("gap_list.out", "a") as gaps_output:
        gaps_output.write("TM Band Gaps for radius " + str(r) + "a:\n")
        gaps_output.write(str(tm_gaps))
        gaps_output.write("\nTE Band Gaps for radius " + str(r) + "a:\n")
        gaps_output.write(str(te_gaps))
        gaps_output.write("\n=======================================\n\n")
"""
