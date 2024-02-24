"""
Utility functions
"""

import math


def stratospheric_model(height: float) -> dict:
    """
    Calculates air parameters in a stratosphere as a function of height above the sea level

    Args:
        height: current height above sea level

    Returns:
        parameters of the air: temperature, pressure, density, speed of sound

    """

    temperature = -56.46  # air temperature [deg C]
    pressure = 22.65 * math.exp(1.73 - 0.000157 * height)  # air pressure [kPa]
    density = pressure / (0.2869 * (temperature + 273.1))  # air density [kg/m3]
    sound = _calculate_speed_of_sound(pressure, density)
    viscosity = calculate_viscosity(temperature)

    air = {
        "temp_c": temperature,
        "density": density,
        "sound": sound,
        "viscosity": viscosity,
    }

    return air


def tropospheric_model(height: float) -> dict:
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
    sound = _calculate_speed_of_sound(pressure, density)
    viscosity = calculate_viscosity(temperature)

    air = {
        "temp_c": temperature,
        "density": density,
        "sound": sound,
        "viscosity": viscosity,
    }

    return air


def _calculate_speed_of_sound(pressure: float, density: float) -> float:
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
) -> float:
    """

    Args:
        density: air density
        velocity: current velocity
        diameter: diameter of the ball
        viscosity: viscosity

    Returns:
        Reynolds number

    """
    return density * velocity * diameter * 0.001 / viscosity


def update_drag_coefficient(density, area, drag_c):
    """

    Args:
        density: air density
        area: cross-section area
        drag_c: coefficient of drag

    Returns:
        updated drag coefficient
    """
    return density * area * drag_c / 2


def _calculate_terminal_velocity(mass, drag_coefficient):
    """

    Args:
        mass: mass of an object
        drag_coefficient: drag coefficient

    Returns:
        calculated terminal velocity
    """

    gravity = 9.81
    return math.sqrt(mass * gravity / drag_coefficient)


def calculate_velocity(mass, drag_co, current_time):
    """

    Args:
        mass: mass of an object
        drag_co: drag coefficient
        current_time: current drop time

    Returns:

    """
    gravity = 9.81
    terminal = _calculate_terminal_velocity(mass, drag_co)
    return terminal * math.tanh(gravity * current_time / terminal)


def calculate_total_distance(distance, curr_velocity, prev_velocity, time_step):
    """

    Args:
        distance: distance travelled so far
        curr_velocity: current velocity
        prev_velocity: previous velocity
        time_step: time step size

    Returns:
        total distance travelled

    """
    return distance + (prev_velocity + curr_velocity) / 2 * time_step


def calculate_step_distance(curr_velocity, prev_velocity, time_step):
    """

    Args:
        curr_velocity: current velocity
        prev_velocity: previous velocity
        time_step: time step size

    Returns:
        total distance travelled

    """
    return (prev_velocity + curr_velocity) / 2 * time_step


def check_flight_conditions(mach: float, reynolds: float, flags: list) -> list:
    """

    Args:
        mach: current Mach number
        reynolds: current Reynolds number

    Returns:

    """

    if mach > 0.6 and flags[0] == 0:
        flags[0] = 1
    if reynolds > 200000 and flags[1] == 0:
        flags[1] = 1
    return flags
