#!/usr/bin/python3

import icon
import datetime

TIME_ICONS = icon.IconSet("icons/time-left.ppm")
DELAY_ICONS = icon.IconSet("icons/delay.ppm")
TRAIN_ICONS = icon.IconSet("icons/trains.ppm")

def get_train(status):
    if status > 0:
        return TRAIN_ICONS.get(2, 0, 8) # red
    elif status < 0:
        return TRAIN_ICONS.get(0, 0, 8) # green
    else:
        return TRAIN_ICONS.get(1, 0, 8) # amber

def get_time_left(c):
    if c is None or not isinstance(c, datetime.timedelta):
        return TIME_ICONS.get(7, 7, 8)
    c = c.seconds // 60
    if c > 40:
        return TIME_ICONS.get(0, 7, 8)
    if c < -9:
        return TIME_ICONS.get(1, 7, 8)

    c = 40 - c
    return TIME_ICONS.get(c%8, c//8, 8)

def get_delay(c):
    if c is None or not isinstance(c, datetime.timedelta):
        return DELAY_ICONS.get(7, 7, 8)
    c = c.seconds // 60
    if c > 40:
        return DELAY_ICONS.get(0, 7, 8)
    if c < -9:
        return DELAY_ICONS.get(1, 7, 8)

    c = 40 - c
    return DELAY_ICONS.get(c%8, c//8, 8)

