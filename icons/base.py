#!/usr/bin/python3

from . import icons
import os
import logging
import math

_here = os.path.dirname(__file__)

_number_icons = icons.IconSet(os.path.join(_here,"numbers-generic.ppm"))
_banner_icons = icons.IconSet(os.path.join(_here,"base.ppm"))

random_banner = _banner_icons.get(0, 0, 8)
digit_banner = _banner_icons.get(1, 0, 8)    

def number(c, colour=(0,-1,0)):
    if c is None:
        return _number_icons.get(0, 0, 8).colour(*colour)

    try:
        c = math.floor(c)
    except ValueError as e:
        logging.warn(e)
        return _number_icons.get(0, 0, 8).colour(*colour)

    if c > 99:
        return _number_icons.get(1, 0, 8).colour(*colour)
    if c < -9:
        return _number_icons.get(2, 0, 8).colour(*colour)

    c = 104 - c
    return _number_icons.get(c%8, c//8, 8).colour(*colour)
