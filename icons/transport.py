#!/usr/bin/python3

from . import icons, base
import logging
import os
import datetime

_here = os.path.dirname(__file__)
_mode_icons = icons.IconSet(os.path.join(_here,"transport-modes.ppm"))

TRAIN = 0
BUS = 1
TRAM = 2

def time_left(td, min_warn, max_warn, colour=icons.WHITE, warn_colour=icons.RED):
    if td is None or not isinstance(td, datetime.timedelta):
        return base.error("time_left: expected timedelta, got %s" % td)

    mins = (td.seconds + td.days*86400) // 60
    min_warn_mins = (min_warn.seconds + min_warn.days*86400) // 60
    max_warn_mins = (max_warn.seconds + max_warn.days*86400) // 60
    return base.number(mins, warn_colour, min_warn_mins, colour, max_warn_mins)

def delay(td, warn_delay, colour=icons.GREEN, delay_colour=icons.AMBER, warn_colour=icons.RED):
    if td is None or not isinstance(td, datetime.timedelta):
        return base.error("delay: expected timedelta, got %s" % td)

    mins = (td.seconds + td.days*86400) // 60
    warn_delay_mins = (warn_delay.seconds + warn_delay.days*86400) // 60

    if mins <= 0:
        return base.number(mins, colour)
    elif mins > warn_delay_mins:
        return base.number(mins, delay_colour)
    else:
        return base.number(mins, warn_colour, 1, icons.RED, warn_delay_mins)

def mode(mode, colour=icons.BLUE):
    return _mode_icons.get(mode, 0, 8).colour(colour)

def is_delayed(status, mode=TRAIN):
    if status is True:
        return _mode_icons.get(mode, 0, 8).colour(icons.RED)
    elif status is False:
        return _mode_icons.get(mode, 0, 8).colour(icons.GREEN)
    else:
        return _mode_icons.get(mode, 0, 8).colour(icons.AMBER)

