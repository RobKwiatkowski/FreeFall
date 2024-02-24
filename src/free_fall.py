"""
This program calculates free fall parameters of a sphere released from a given altitude.
It includes drag force change with the altitude and speed.

International Standard Atmosphere (ISA) air parameters are modelled by approximation functions
from NASA webpage.
Viscosity is calculated based on Sutherland equation.
"""

from dataclasses import dataclass
import utils


@dataclass(kw_only=True)
class Object:
    """
    Object to be dropped.
    """

    mass: float | int
    diameter: float | int
    drag_c: float | int

    def __post_init__(self):
        for name, field_type in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(
                    f"The field `{name}` was assigned by "
                    f"`{current_type}` instead of `{field_type}`"
                )

        if self.mass <= 0:
            raise ValueError("Error! Mass has to be a positive value.")

        if self.diameter <= 0:
            raise ValueError("Error! Diameter has to be a positive value.")

        self.cross_section = utils.calculate_sphere_cross_section(self.diameter)

    def drop(
        self, drop_altitude: float, verbose: bool = True, time_step: int | float = 0.5
    ) -> dict:
        """
        Args:
                drop_altitude: drop altitude [m]
                verbose: verbosity level
                time_step: size of the time step [s]

        Returns:
                History of velocity, distance and time
        """
        velocity = [0]  # stores the current velocity
        altitude = [drop_altitude]  # stores the distance travelled
        time = [0]  # stores the current time
        flags = [0, 0]  # flags about warnings

        while altitude[-1] > 0:
            air = utils.atmosphere_model(altitude[-1])
            flags = utils.check_flight_conditions(
                air, velocity[-1], self.diameter, flags
            )

            time.append(time[-1] + time_step)

            current_velocity = utils.calculate_velocity(
                air, self.mass, self.cross_section, self.drag_c, time[-1]
            )
            velocity.append(current_velocity)

            step_distance = utils.calculate_step_distance(
                velocity[-1], velocity[-2], time_step
            )
            altitude.append(altitude[-1] - step_distance)  # the actual height [m]

        if verbose:
            if flags[0] == 1:
                print(
                    "WARNING: Mach number above 0.6! Compression effects may occur.\n"
                )
            if flags[1] == 1:
                print("WARNING: reynolds number above 200000!\n")
            print("RESULTS:")
            print(f"Falling time is: {time[-1]:.3f}s ")
            print(f"Impact velocity is {velocity[-1]:.3f} m/s")

        return {"time": time, "altitude": altitude, "velocity": velocity}
