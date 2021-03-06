"""
Given a frequency in units of speed-of-light/lattice-spacing
and a lattice spacing calculates the energy in electronVolts
"""

speed_of_light = 3e8 # Speed of Light in meters per second
planck_constant = 6.626e-34 # Planck's Constant in SI units

lattice_constant = input("Enter lattice constant in microns: ")
frequency_c_over_a = input("Enter frequency in c/a: ")

frequency_hertz = frequency_c_over_a * (speed_of_light / (lattice_constant * (1e-6)))
wavelength_meters = speed_of_light / frequency_hertz

print("The frequency in hertz is: " + str(frequency_hertz))