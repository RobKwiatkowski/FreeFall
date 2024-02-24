"""
Main file
"""

from free_fall import Object

ball = Object(mass=1, diameter=1, drag_c=0.44)

v, d, t = ball.drop(1000)
