#!/usr/bin/python3

from . import icons, base
import os
import logging
import math

_here = os.path.dirname(__file__)

_cond_icons = icons.IconSet(os.path.join(_here,"weather-conditions.ppm"))
_cond_names = {
	"moon_night":0,
	"sun":1,
	"partial_cloud_night":2,
	"partial_cloud":3,
	"dark_night":4,
	"mist":5,
	"fog":6,
	"cloud":7,
	"dark_cloud":8,
	"rain_1":9,
	"showers":10,
	"drizzle":11,
	"rain":12,
	"heavy_rain":13,
	"heavy_showers":14,
	"heavy_rain_1":15,
	"sleet":16,
	"sleet_showers":17,
	"sleet_1":18,
	"hail":19,
	"hail_1":20,
	"hail_2":21,
	"snow":22,
	"snow_showers":23,
	"snow_1":24,
	"heavy_snow":25,
	"heavy_snow_showers":26,
	"heavy_snow_1":27,
	"lightning":28,
	"lightning_1":29,
	"lightning_2":30,
	"unknown":31
}

def temperature(t, cold=0, warm=15, hot=35):
    # "warm" means what will get a green number.
    # There's more perceptual distance between red and green
    # than green and blue, so "warm" should be on the cold side

    if t is None:
        return base.error("temperature: expected number, got None")

    try:
        if t > warm:
            return base.number(t, icons.GREEN, warm, icons.RED, hot)
        else:
            return base.number(t, icons.BLUE, cold, icons.GREEN, warm)
    except ValueError as e: # not a number?
        return base.error("weather.temperature: %s" % e)


def conditions(c):
    if isinstance(c, str):
        if c in _cond_names:
            c = _cond_names[c]
        else:
            return base.error("weather.conditions: no icon for '%s'" % c)

    try:
        c = math.floor(c)
    except Exception as e:
        return base.error("weather.conditions: %s" % e)

    if c is None or c < 0 or c > 30:
        return base.error("weather.conditions: %d out of range" % c)
    else:
        return _cond_icons.get(c%8, c//8, 8)
