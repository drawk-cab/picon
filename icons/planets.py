#!/usr/bin/python3

from . import icons, base
import logging
import os
import datetime

_here = os.path.dirname(__file__)
_planet_icons = icons.IconSet(os.path.join(_here,"planets.ppm"))

SUN = 0
MOON = 1
MERCURY = 2
VENUS = 3
MARS = 4
JUPITER = 5
SATURN = 6


def planet(planet, colour=icons.WHITE):
    return _planet_icons.get(planet, 0, 8).colour(colour)

HOURS = [0, 3, 2, 1, 6, 5, 4]
def hour(hour, weekday=0, colour=icons.WHITE):
    hour = int( (hour+24*weekday) % 7 )
    return planet(HOURS[hour], colour )

def weekday(weekday, colour=icons.WHITE):
    return hour(0, weekday, colour)

MONTH = datetime.timedelta(29.53)
def moon_phase(age, phase=0, colour=icons.WHITE):
    '''Return an icon for the phase of the moon after a certain time.
phase: 0 = new moon, 1 = first quarter, 2 = full moon, 3 = third quarter.
age: timedelta after the given phase.
You can supply age only, it will use the configured approximate average month of 29.53 days.'''
    age = ( 16 - int( age.total_seconds() * 32 / MONTH.total_seconds() ) ) % 32
    return _planet_icons.get(age % 8, 4-(age // 8)).colour(colour)

def moon_phase_angle(angle, colour=icons.WHITE):
    age = ( 16 - int(angle * 32/360) ) % 32
    return _planet_icons.get(age % 8, 1+(age // 8)).colour(colour)
