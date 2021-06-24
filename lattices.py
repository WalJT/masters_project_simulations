#!/usr/bin/env python3
import meep as mp
import numpy as np


def triangular(lattice_constant: float, number_of_rows: int, number_of_cols: int, starting_point: mp.Vector3) -> list:
    """
    Returns a triangular (hexagonal lattice) repeated over a finite region in space
    :param lattice_constant:
    :param number_of_rows:
    :param number_of_cols:
    :param starting_point:
    :return: List containing all lattice sites (list of mp.Vector3)
    """
    lattice_sites = [starting_point]
    lattice_vectors = (mp.Vector3(lattice_constant, 0),
                       mp.Vector3(lattice_constant / 2, np.sqrt(3) * lattice_constant / 2),
                       mp.Vector3(-lattice_constant / 2, np.sqrt(3) * lattice_constant / 2))

    for col in range(number_of_cols):
        for row in range(number_of_rows):
            if row == 0:
                new_point = lattice_sites[row] + col * (lattice_vectors[0])
            else:
                if (row % 2) == 0:
                    new_point = lattice_sites[row] + (lattice_vectors[1]) + col * (lattice_vectors[0])
                else:
                    new_point = lattice_sites[row] + (lattice_vectors[2]) + col * (lattice_vectors[0])
            lattice_sites.append(new_point)

        new_point = lattice_sites[col] + (col * lattice_vectors[0]) - (col * lattice_vectors[1])
        lattice_sites.append(new_point)

    return lattice_sites


def square(lattice_constant: float, number_of_rows: int, number_of_cols: int, starting_point: mp.Vector3) -> list:
    lattice_sites = [starting_point]
    lattice_vectors = (mp.Vector3(lattice_constant, 0),
                       mp.Vector3(0, lattice_constant))

    for col in range(number_of_cols):
        for row in range(number_of_rows):
            if row == 0:
                new_point = lattice_sites[row] + col * (lattice_vectors[0])
            else:
                new_point = lattice_sites[row] + (lattice_vectors[1]) + col * (lattice_vectors[0])
            lattice_sites.append(new_point)

    new_point = lattice_sites[col] + (col * lattice_vectors[0]) - (col * lattice_vectors[1])
    lattice_sites.append(new_point)

    return lattice_sites
