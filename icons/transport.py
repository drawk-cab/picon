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

def is_delayed(status, mode=TRAIN):
    if status is True:
        return _mode_icons.get(mode, 0, 8).colour(icons.RED)
    elif status is False:
        return _mode_icons.get(mode, 0, 8).colour(icons.GREEN)
    else:
        return _mode_icons.get(mode, 0, 8).colour(icons.AMBER)

def time_left(td, min_notice=15):
    if td is None or not isinstance(td, datetime.timedelta):
        return base.error("time_left: expected timedelta, got %s" % td)

    mins = (td.seconds + td.days*86400) // 60
    return base.number(mins, icons.RED, 0, icons.GREEN, min_notice)

def delay(td, max_delay=15):
    if td is None or not isinstance(td, datetime.timedelta):
        return base.error("delay: expected timedelta, got %s" % td)

    mins = (td.seconds + td.days*86400) // 60

    if mins <= 0:
        return icons.Report(base.number(mins, icons.GREEN),
            banner=is_delayed(False))
    elif mins > max_delay:
        return icons.Report(base.number(mins, icons.RED),
            banner=is_delayed(True))
    else:
        return icons.Report(base.number(mins, icons.AMBER, 1, icons.RED, max_delay),
            banner=is_delayed(None))
