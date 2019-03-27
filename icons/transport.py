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

def time_left(td, warn_notice):
    if td is None or not isinstance(td, datetime.timedelta):
        return base.error("time_left: expected timedelta, got %s" % td)

    mins = td.total_seconds() // 60
    warn_notice_mins = warn_notice.total_seconds() // 60
    return base.number(mins, icons.RED, 0, icons.GREEN, warn_notice_mins)

def delay(td, warn_delay):
    if td is None or not isinstance(td, datetime.timedelta):
        return base.error("delay: expected timedelta, got %s" % td)

    mins = td.total_seconds() // 60
    warn_delay_mins = warn_delay.total_seconds() // 60

    if mins <= 0:
        return base.number(mins, icons.GREEN)
    elif mins > warn_delay_mins:
        return base.number(mins, icons.RED)
    else:
        return base.number(mins, icons.AMBER, 1, icons.RED, warn_delay_mins)

def mode(mode):
    return _mode_icons.get(mode, 0, 8).colour(icons.BLUE)

def is_delayed(status, mode=TRAIN):
    if status is True:
        return _mode_icons.get(mode, 0, 8).colour(icons.RED)
    elif status is False:
        return _mode_icons.get(mode, 0, 8).colour(icons.GREEN)
    else:
        return _mode_icons.get(mode, 0, 8).colour(icons.AMBER)

