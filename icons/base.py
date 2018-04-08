#!/usr/bin/python3

from . import IconSet
import os
import logging
import math

_here = os.path.dirname(__file__)

_number_icons = IconSet(os.path.join(_here,"numbers-generic.ppm"))
_banner_icons = IconSet(os.path.join(_here,"base.ppm"))

random_banner = _banner_icons.get(0, 0, 8)
digit_banner = _banner_icons.get(1, 0, 8)    

def number(c):
    if c is None:
        return _number_icons.get(7, 7, 8)

    try:
        c = math.floor(c)
    except ValueError as e:
        logging.warn(e)
        return _number_icons.get(7, 7, 8)

    if c > 40:
        return _number_icons.get(0, 7, 8)
    if c < -9:
        return _number_icons.get(1, 7, 8)

    c = 40 - c
    return _number_icons.get(c%8, c//8, 8)
