"""
Utility functions
"""

import math


def stratospheric_model(height: float) -> tuple:
    """
    Calculates air parameters in a stratosphere as a function of height above the sea level

    Args:
        height: current height above sea level

    Returns:
        parameters of the air: temperature, pressure, density

    """

    temperature = -56.46  # air temperature [deg C]
    pressure = 22.65 * math.exp(1.73 - 0.000157 * height)  # air pressure [kPa]
    density = pressure / (0.2869 * (temperature + 273.1))  # air density [kg/m3]

    return temperature, pressure, density


def tropospheric_model(height: float) -> tuple:
    """
    Calculates air parameters in a troposphere as a function of height above the sea level

    Args:
        height: current height above sea level

    Returns:
        parameters of the air: temperature, pressure, density

    """

    temperature = 15.04 - 0.00649 * height  # air temperature [deg C]
    pressure = 101.29 * ((temperature + 273.1) / 288.08) ** 5.256  # air pressure [kPa]
    density = pressure / (0.2869 * (temperature + 273.1))  # air density [kg/m3]

    return temperature, pressure, density


def calculate_speed_of_sound(pressure: float, density: float) -> float:
    """
    Calculates a speed of sound

    Args:
        pressure: air pressure
        density: air density

    Returns:
        speed of sound at given air conditions
    """
    return math.sqrt(1.4 * pressure * 1000 / density)


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


def calculate_sphere_cross_section(diameter: float) -> float:
    """

    Args:
        diameter: diameter of a sphere in millimeters

    Returns:
        calculated cross-section area

    """
    return 3.14 * diameter**2 / 4 * 0.000001


def calculate_mach_number(velocity, sound_speed):
    """
    Calculates Mach number
    Args:
        velocity: velocity in m/s
        sound_speed: speed of sound in m/s

    Returns:
        calculated Mach number
    """
    return velocity / sound_speed


def calculate_reynolds(
    density: float, velocity: float, diameter: float, viscosity: float
) -> list:
    """

    Args:
        density:
        velocity:
        diameter:
        viscosity:

    Returns:

    """
    return density * velocity * diameter * 0.001 / viscosity


def update_drag_coefficient(density, area, drag_c):
    """

    Args:
        density:
        area:
        drag_c:

    Returns:

    """
    return density * area * drag_c / 2


def calculate_terminal_velocity(mass, drag_coefficient):
    """

    Args:
        mass:
        drag_coefficient:

    Returns:

    """
    gravity = 9.81
    return math.sqrt(mass * gravity / drag_coefficient)


def calculate_velocity(terminal, current_time):
    """

    Args:
        terminal:
        current_time:

    Returns:

    """
    gravity = 9.81
    return terminal * math.tanh(gravity * current_time / terminal)


def calculate_total_distance(distance, curr_velocity, prev_velocity, time_step):
    """

    Args:
        distance:
        curr_velocity:
        prev_velocity:
        time_step:

    Returns:

    """
    return distance + (prev_velocity + curr_velocity) / 2 * time_step
