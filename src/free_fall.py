"""
This program calculates free fall parameters of a sphere released from a given altitude.
It includes drag force change with the altitude and speed.

International Standard Atmosphere (ISA) air parameters are modelled by approximation functions
from NASA webpage.
Viscosity is calculated based on Sutherland equation.
"""

import utils


def drop_calc(
    mass: float,
    diameter: float,
    drag_c: float = 0.44,
    drop_h: float = 1000,
    verbose: bool = True,
    time_step: float = 0.05,
) -> list:
    """

    Args:
            mass: mass of a ball [kg]
            diameter: diameter of an object [mm]
            drag_c: coefficient of drag at sea level[-]
            drop_h: drop height [m]
            verbose: verbosity level
            time_step: size of the time step [s]

    Returns:
            History of velocity, distance and time

    """

    if not isinstance(mass, (float, int)) or not isinstance(diameter, (float, int)):
        raise ValueError("Error! Only numerical values are allowed.")

    if mass <= 0:
        raise ValueError("Error! Mass has to be a positive value.")

    if diameter <= 0:
        raise ValueError("Error! Diameter has to be a positive value.")

    area = utils.calculate_sphere_cross_section(diameter)

    velocity = [0]  # stores the current velocity
    distance = [0]  # stores the distance travelled
    time = [0]  # stores the current time
    flags = [0, 0]  # flags about warnings

    h_actual = drop_h  # actual height

    while h_actual > 0:
        if h_actual > 11000:
            temp_c, density, sound = utils.stratospheric_model(h_actual)
        else:
            temp_c, density, sound = utils.tropospheric_model(h_actual)

        viscosity = utils.calculate_viscosity(temp_c)

        mach = utils.calculate_mach_number(velocity[-1], sound)
        reynolds = utils.calculate_reynolds(density, velocity[-1], diameter, viscosity)

        flags = utils.check_flight_conditions(mach, reynolds, flags)

        k = utils.update_drag_coefficient(density, area, drag_c)
        time.append(time[-1] + time_step)

        current_velocity = utils.calculate_velocity(mass, k, time[-1])
        velocity.append(current_velocity)

        step_distance = utils.calculate_step_distance(
            velocity[-1], velocity[-2], time_step
        )
        distance.append(distance[-1] + step_distance)

        h_actual = drop_h - distance[-1]  # the actual height [m]

    if verbose:
        if flags[0] == 1:
            print("WARNING: Mach number above 0.6! Compression effects may occur.\n")
        if flags[1] == 1:
            print("WARNING: reynolds number above 200000!\n")
        print("RESULTS:")
        print(f"Falling time is: {time[-1]:.3f}s ")
        print(f"Impact velocity is {velocity[-1]:.3f} m/s")

    return [velocity, distance, time]
