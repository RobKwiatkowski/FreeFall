"""
Main file
"""

from free_fall import Object, drop_calc

ball = Object(1, 1, 0.44)

v, d, t = drop_calc(ball)
