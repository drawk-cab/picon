#!/usr/bin/python3

from . import icons
import os
import datetime

_here = os.path.dirname(__file__)

_time_icons = icons.IconSet(os.path.join(_here,"time-left.ppm"))
_delay_icons = icons.IconSet(os.path.join(_here,"delay.ppm"))
_train_icons = icons.IconSet(os.path.join(_here,"trains.ppm"))

def train_is_delayed(status):
    if status is True:
        return _train_icons.get(2, 0, 8) # red
    elif status is False:
        return _train_icons.get(0, 0, 8) # green
    else:
        return _train_icons.get(1, 0, 8) # amber

def time_left(c):
    if c is None or not isinstance(c, datetime.timedelta):
        return _time_icons.get(7, 7, 8)
    c = c.seconds // 60
    if c > 40:
        return _time_icons.get(0, 7, 8)
    if c < -9:
        return _time_icons.get(1, 7, 8)

    c = 40 - c
    return _time_icons.get(c%8, c//8, 8)

def delay(c):
    if c is None or not isinstance(c, datetime.timedelta):
        return _delay_icons.get(7, 7, 8)
    c = c.seconds // 60
    if c > 40:
        return _delay_icons.get(0, 7, 8)
    if c < -9:
        return _delay_icons.get(1, 7, 8)

    c = 40 - c
    return _delay_icons.get(c%8, c//8, 8)

