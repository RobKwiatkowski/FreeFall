"""
Main file
"""

from free_fall import Object

ball = Object(1, 1, 0.44)

v, d, t = ball.drop(1000)
