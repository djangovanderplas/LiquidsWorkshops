from pycea import CEA, blends
import matplotlib.pyplot as plt
import numpy as np

# ADJUSTABLE PARAMETERS
chamber_pressure = 30e5  # Pa
nozzle_expansion_ratio = 10
ambient_pressure = 1e5  # Pa

# PROPELLANT SELECTOR
fuel = ['Ethanol', 'H2O']
fuel_mass_fraction = [0.8, 0.2]
oxidizer = ['LOX']
oxidizer_mass_fraction = [1]

def genCEAObj(fuel: list, fuel_mass_fraction: list, oxidizer: list, oxidizer_mass_fraction: list) -> object:
    """
    Generates a CEA object with the given fuel and oxidizer. You can find the propellants here:
    https://rocketcea.readthedocs.io/en/latest/propellants.html
    :param fuel: List of fuel names
    :param fuel_mass_fraction: List of fuel mass fractions
    :param oxidizer: List of oxidizer names
    :param oxidizer_mass_fraction: List of oxidizer mass fractions
    :return: CEA object
    """
    # Create new blends
    Fuel = blends.newFuelBlend(fuelL=fuel, fuelPcentL=fuel_mass_fraction)
    Oxidizer = blends.newOxBlend(oxL=oxidizer, oxPcentL=oxidizer_mass_fraction)

    # Create CEA object
    return CEA(propName='', fuelName=Fuel, oxName=Oxidizer, units="metric")


# Create CEA object
cea = genCEAObj(fuel, fuel_mass_fraction, oxidizer, oxidizer_mass_fraction)


# Plot Isp vs mixture ratio
mixture_ratios = np.arange(1, 2, 0.01)
isp_vacuums = []
isp_ambients = []
tcombs = []
for mr in mixture_ratios:
    isp_vacuum = cea.get_Isp(Pc=chamber_pressure, MR=mr, eps=nozzle_expansion_ratio)
    isp_ambient = cea.estimate_Ambient_Isp(Pc=chamber_pressure, MR=mr, eps=nozzle_expansion_ratio,
                                           Pamb=ambient_pressure)
    temperature = cea.get_Tcomb(Pc=chamber_pressure, MR=mr)
    isp_vacuums.append(isp_vacuum)
    isp_ambients.append(isp_ambient[0])
    tcombs.append(temperature)

# Figure out optima
print(f'Maximum Vacuum Isp: {max(isp_vacuums)}')
print(f'Mixture Ratio for Maximum Vacuum Isp: {mixture_ratios[np.argmax(isp_vacuums)]}')

print(f'Maximum Ambient Isp: {max(isp_ambients)}')
print(f'Mixture Ratio for Maximum Ambient Isp: {mixture_ratios[np.argmax(isp_ambients)]}')

print(f'Maximum Combustion Temperature: {max(tcombs)}')
print(f'Mixture Ratio for Maximum Combustion Temperature: {mixture_ratios[np.argmax(tcombs)]}')


# Plot the graph
fig, ax1 = plt.subplots()
plt.title('Isp vs Mixture Ratio')
color = 'tab:red'

# plt.plot(mixture_ratios, isp_ambients, label='Ambient Isp')
plt.plot(mixture_ratios, isp_vacuums, label='Vacuum Isp', color=color)
ax1.set_xlabel('Mixture Ratio [-]')
ax1.set_ylabel('Isp [s]', color=color)
ax1.tick_params(axis='y', labelcolor=color)


ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Temperature [K]', color=color)
ax2.plot(mixture_ratios, tcombs, label='Combustion Temperature', color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.show()
