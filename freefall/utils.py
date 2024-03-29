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


def atmosphere_model(altitude: float) -> dict:
    """
    Args:
        altitude: current altitude [m]

    Returns:
        data from appropriate atmospheric model
    """
    if altitude > 11000:
        model_data = stratospheric_model(altitude)
    else:
        model_data = tropospheric_model(altitude)

    return model_data


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


def check_flight_conditions(air: dict, velocity, diameter: float, flags: list) -> list:
    """

    Args:
        air: air parameters
        velocity: current flight velocity
        diameter: object diameter
        flags: flags list

    Returns:
        updated flags

    """
    mach = calculate_mach_number(velocity, air["sound"])
    reynolds = calculate_reynolds(air["density"], velocity, diameter, air["viscosity"])

    if mach > 0.6 and flags[0] == 0:
        flags[0] = 1
    if reynolds > 200000 and flags[1] == 0:
        flags[1] = 1
    return flags


def calculate_velocity(air, mass, cross_section, drag_c, current_time):
    """Calculates current velocity considering the terminal velocity

    Args:
        air: air parameters
        mass: mass of an object [kg]
        cross_section: cross_section of an object [m2]
        drag_c: coefficient of drag
        current_time: current time of flight

    Returns:
        Air viscosity
    """
    gravity = 9.81
    coefficient = air["density"] * cross_section * drag_c / 2
    terminal = math.sqrt(mass * gravity / coefficient)
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
