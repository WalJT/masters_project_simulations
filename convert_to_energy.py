"""
Given a frequency in units of speed-of-light/lattice-spacing
and a lattice spacing calculates the energy in electronVolts
"""

speed_of_light = 3e8  # Speed of Light in meters per second
planck_constant = 6.626e-34  # Planck's Constant in SI units
electron_charge = 1.6e-19

lattice_constant = float(input("Enter lattice constant in microns: "))
frequency_c_over_a = float(input("Enter frequency in c/a: "))

frequency_hertz = frequency_c_over_a * (speed_of_light / (lattice_constant * 1e-6))
wavelength_meters = speed_of_light / frequency_hertz

scientific_notation = "{:e}".format(frequency_hertz)

print("The frequency in hertz is: " + str(scientific_notation))
print("The wavelength in meters is: "+str(wavelength_meters))

energy_joules = planck_constant*frequency_hertz
energy_electron_volts = energy_joules/electron_charge

print("The energy is: "+str(energy_joules)+"J")

print("The energy is: "+str(energy_electron_volts)+"eV")
