#!/usr/bin/python3

from . import icons
import os
import logging
import math

_here = os.path.dirname(__file__)

_number_icons = icons.IconSet(os.path.join(_here,"numbers.ppm"))
_banner_icons = icons.IconSet(os.path.join(_here,"banners.ppm"))

random_banner = _banner_icons.get(0, 0, 8)
digit_banner = _banner_icons.get(1, 0, 8)

def empty():
    return _number_icons.get(3, 0, 8)

def fill(colour=icons.WHITE):
    return _number_icons.get(4, 0, 8).colour(colour)

def error(e):
    logging.warn(e)
    return _number_icons.get(0, 0, 8)

def unknown(colour=icons.RED):
    return _number_icons.get(0, 0, 8).colour(colour)

def number(n, c_min=icons.WHITE, n_min=0, c_max=None, n_max=0):
    if n is None:
        return unknown()

    try:
        colour = icons.colour_between(n, c_min, n_min, c_max, n_max)
        n = math.floor(n)
    except ValueError as e:
        logging.warn(e)
        return _number_icons.get(0, 0, 8).colour(colour)

    if n > 99:
        return _number_icons.get(1, 0, 8).colour(colour)
    if n < -9:
        return _number_icons.get(2, 0, 8).colour(colour)

    n = 104 - n
    return _number_icons.get(n%8, n//8, 8).colour(colour)
