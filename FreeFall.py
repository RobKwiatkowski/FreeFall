"""Version 2.4
This program calculates free fall parameters of a sphere released from a given altitude.
It includes drag force change with the altitude and speed.

International Standard Atmosphere (ISA) air parameters are modelled by approximation functions from NASA webpage.
Viscosity is calculated based on Sutherland equation.
Only troposphere is modelled therefore the maximum allowable release height is 11000m.

Release notes:
* Includes lower stratosphere (up to 25000m)
"""

import math

# constants
GRAVITY = 9.81
TIME_STEP = 0.05
S = 110.4
B = 1.46E-6

def user_input(text, default):
	"""
	Asks user for the input and checks its correctness
	"""
	while True:
		try:
			value = float(raw_input(text) or default)
			if value>0:		
				break
			else:
				print "Give a positive value!"
		except:
			print "Give a number!"
	return value

mass = user_input("Mass (def: 0.04)[kg]: ","0.04")
diameter = user_input("Diameter (def: 10)[mm]: ","10")
drag_c = user_input("Coefficient of drag (def: 0.44): ","0.44")
drop_h = user_input("Drop height (def: 10000)[m]: ","10000")

area = 3.14*diameter**2/4*0.000001

print "\nSphere cross sectional area is: " + str(area) + " m2\n"

velocity = [0]					# stores the current velocity
distance = [0] 					# stores the distance travelled
time     = [0]					# stores the current time
h = drop_h                      # stores the actual height
max_mach = 0
Re_max = 0


while h>0:
	if h>11000:
		T = -56.46                       					# air temperature [deg C]
		P = 22.65*math.exp(1.73-.000157*h)       			# calculates air pressure [kPa]
		density = P/(0.2869*(T+273.1))             			# calculates air density [kg/m3]
	else:
		T = 15.04 - 0.00649*h                       		# calculates air temperature [deg C]
		P = 101.29*((T+273.1)/288.08)**5.256        		# calculates air pressure [kPa]
		density = P/(0.2869*(T+273.1))             			# calculates air density [kg/m3]
		
	sound = math.sqrt(1.4*P*1000/density)					# calculates speed of sound[m/s]
	mach = velocity[-1]/sound								# calculates Mach number [-]
	viscosity = (B*(T+273.1)**1.5)/(T+S+273.1)				# calculates viscosity [Pa s]
	Re = density*velocity[-1]*diameter*0.001/viscosity		# calculates Reynold number [-]
	
	if mach>max_mach:
		max_mach = mach
	if Re>Re_max:
		Re_max = Re

	k = density*area*drag_c/2                   			# calculates shape drag coefficient  
	terminal = math.sqrt(mass*GRAVITY/k)        			# calculates terminal velocity [m/s]
	time.append(time[-1] + TIME_STEP)
	velocity.append(terminal*math.tanh(GRAVITY*time[-1]/terminal)) 
	distance.append(distance[-1] + (velocity[-2] + velocity[-1])/2*TIME_STEP)	# calculates the total distance travelled [m]
	h = drop_h - distance[-1]                                           		# calculates the actual height [m]

if max_mach>0.6:
	print "WARNING: Mach number above 0.6!\n"

if Re>200000:
	print "WARNING: Re number above 200000!\n"

print "RESULTS:"
print "Falling time is: " + str(time[-1]) + " s"
print "Impact velocity is: " + str(velocity[-1]) + " m/s"

input("Press ENTER to exit")
