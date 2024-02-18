"""Version 2.4
This program calculates free fall parameters of a sphere released from a given altitude.
It includes drag force change with the altitude and speed.

International Standard Atmosphere (ISA) air parameters are modelled by approximation functions from NASA webpage.
Viscosity is calculated based on Sutherland equation.
Only troposphere is modelled therefore the maximum allowable release height is 11000m.

Release notes:
* Includes lower stratosphere only (up to 25000m)
"""

import math


def drop_calc(mass, diameter, drag_c=0.44, drop_h=1000):
	"""

	@param mass: mass of a ball [kg]
	@param diameter: diameter of a ball [mm]
	@param drag_c: coefficient of drag
	@param drop_h: drop height [m]
	@return:
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

	gravity = 9.81
	time_step = 0.05
	s = 110.4		# used for viscosity
	b = 1.46E-6		# used for viscosity

	area = 3.14*diameter**2/4*0.000001

	print("\nSphere cross sectional area is: {} mm^2" .format(area))

	velocity = [0]					# stores the current velocity
	distance = [0] 					# stores the distance travelled
	time = [0]					    # stores the current time
	h = drop_h                      # stores the actual height
	max_mach = 0
	re_max = 0
	reynolds_tracking = []

	while h > 0:
		if h > 11000:
			temp_c = -56.46                						    # air temperature [deg C]
			press = 22.65*math.exp(1.73-.000157*h)       			# air pressure [kPa]
			density = press/(0.2869*(temp_c+273.1))             	# air density [kg/m3]
		else:
			temp_c = 15.04 - 0.00649*h                       		# air temperature [deg C]
			press = 101.29*((temp_c+273.1)/288.08)**5.256        	# air pressure [kPa]
			density = press/(0.2869*(temp_c+273.1))             	# air density [kg/m3]

		sound = math.sqrt(1.4*press*1000/density)						# speed of sound[m/s]
		mach = velocity[-1]/sound								    	# Mach number [-]
		viscosity = (b*(temp_c+273.1)**1.5)/(temp_c+s+273.1)			# viscosity [Pa s]
		reynolds = density*velocity[-1]*diameter*0.001/viscosity		# Reynold number [-]
		reynolds_tracking.append(reynolds)

		if mach > max_mach:
			max_mach = mach
		if reynolds > re_max:
			re_max = reynolds

		k = density*area*drag_c/2                   			# calculates shape drag coefficient
		terminal = math.sqrt(mass*gravity/k)        			# calculates terminal velocity [m/s]
		time.append(time[-1] + time_step)
		velocity.append(terminal*math.tanh(gravity*time[-1]/terminal))
		distance.append(distance[-1] + (velocity[-2] + velocity[-1])/2*time_step)	 # the total distance travelled [m]
		h = drop_h - distance[-1]                                           		 # the actual height [m]

	if max_mach > 0.6:
		print("WARNING: Mach number above 0.6!\n")

	if max(reynolds_tracking) > 200000:
		print("WARNING: reynolds number above 200000!\n")

	print("RESULTS:")
	print("Falling time is: {:.3f}s ".format(time[-1]))
	print("Impact velocity is {:.3f} m/s".format(velocity[-1]))

	return [velocity, distance, time]
