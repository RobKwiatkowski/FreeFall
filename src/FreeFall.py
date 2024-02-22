"""Version 2.4
This program calculates free fall parameters of a sphere released from a given altitude.
It includes drag force change with the altitude and speed.

International Standard Atmosphere (ISA) air parameters are modelled by approximation functions from NASA webpage.
Viscosity is calculated based on Sutherland equation.
Only troposphere is modelled therefore the maximum allowable release height is 11000m.
"""

import math


def stratospheric_model(height):
    temperature = -56.46  # air temperature [deg C]
    pressure = 22.65 * math.exp(1.73 - 0.000157 * height)  # air pressure [kPa]
    density = pressure / (0.2869 * (temperature + 273.1))  # air density [kg/m3]

    return temperature, pressure, density


def tropospheric_model(height):
    temperature = 15.04 - 0.00649 * height  # air temperature [deg C]
    pressure = 101.29 * ((temperature + 273.1) / 288.08) ** 5.256  # air pressure [kPa]
    density = pressure / (0.2869 * (temperature + 273.1))  # air density [kg/m3]

    return temperature, pressure, density


def calculate_speed_of_sound(press, density):
    return math.sqrt(1.4 * press * 1000 / density)


def calculate_viscosity(temperature):
    """
    Calculates dynamic viscosity of air
    Args:
        temperature: temperature in Celsius

    Returns:
        calculated viscosity

    """
    s = 110.4  # Sutherland Constant
    b = 1.46e-6  # air viscosity at 15 deg C
    temp_kelvin = temperature + 273.1
    viscosity = (b * temp_kelvin**1.5) / (temp_kelvin + s)
    return viscosity


def calculate_sphere_cross_section(diameter):
    return 3.14 * diameter**2 / 4 * 0.000001


def calculate_mach_number(velocity, sound_speed):
    return velocity / sound_speed


def calculate_reynolds(density, velocity, diameter, viscosity):
    return density * velocity * diameter * 0.001 / viscosity


def update_drag_coefficient(density, area, drag_c):
    return density * area * drag_c / 2


def calculate_terminal_velocity(mass, drag_coefficient):
    gravity = 9.81
    return math.sqrt(mass * gravity / drag_coefficient)


def calculate_velocity(terminal, current_time):
    gravity = 9.81
    return terminal * math.tanh(gravity * current_time / terminal)


def calculate_total_distance(distance, curr_velocity, prev_velocity, time_step):
    return distance + (prev_velocity + curr_velocity) / 2 * time_step


def drop_calc(mass, diameter, drag_c=0.44, drop_h=1000):
    """

    Args:
            mass: mass of a ball [kg]
            diameter: diameter of an object [mm]
            drag_c: coefficient of drag at sea level[-]
            drop_h: drop height [m]

    Returns:
            History of velocity, distance and time

    """

    if not isinstance(mass, (float, int)) or not isinstance(diameter, (float, int)):
        print("Error! Only numerical values are allowed.")
        return False

    if mass <= 0:
        print("Error! Mass has to be a positive value.")
        return False

    if diameter <= 0:
        print("Error! Diameter has to be a positive value.")
        return False

    time_step = 0.05

    area = calculate_sphere_cross_section(diameter)

    velocity = [0]  # stores the current velocity
    distance = [0]  # stores the distance travelled
    time = [0]  # stores the current time
    reynolds_tracking = []  # stores history of Reynolds number

    h_actual = drop_h  # actual height
    max_mach = 0  # actual Mach number
    re_max = 0  # actual Reynolds number

    while h_actual > 0:
        if h_actual > 11000:
            temp_c, press, density = stratospheric_model(h_actual)
        else:
            temp_c, press, density = tropospheric_model(h_actual)

        sound = calculate_speed_of_sound(press, density)
        mach = calculate_mach_number(velocity[-1], sound)
        viscosity = calculate_viscosity(temp_c)
        reynolds = calculate_reynolds(density, velocity[-1], diameter, viscosity)

        reynolds_tracking.append(reynolds)

        if mach > max_mach:
            max_mach = mach
        if reynolds > re_max:
            re_max = reynolds

        k = update_drag_coefficient(density, area, drag_c)
        terminal = calculate_terminal_velocity(mass, k)

        time.append(time[-1] + time_step)

        current_velocity = calculate_velocity(terminal, time[-1])
        velocity.append(current_velocity)

        total_distance = calculate_total_distance(
            distance[-1], velocity[-1], velocity[-2], time_step
        )
        distance.append(total_distance)

        h_actual = drop_h - distance[-1]  # the actual height [m]

    if max_mach > 0.6:
        print("WARNING: Mach number above 0.6! Compression effects may occur.\n")

    if max(reynolds_tracking) > 200000:
        print("WARNING: reynolds number above 200000!\n")

    print("\nSphere cross sectional area is: {} mm^2".format(area))
    print("RESULTS:")
    print("Falling time is: {:.3f}s ".format(time[-1]))
    print("Impact velocity is {:.3f} m/s".format(velocity[-1]))

    return [velocity, distance, time]
