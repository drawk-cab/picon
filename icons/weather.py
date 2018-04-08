#!/usr/bin/python3

from . import IconSet
import os
import logging
import math

_here = os.path.dirname(__file__)

_temp_icons = IconSet(os.path.join(_here,"weather-temperatures.ppm"))

_cond_icons = IconSet(os.path.join(_here,"weather-conditions.ppm"))
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

def temperature(c):
    if c is None:
        return _temp_icons.get(7, 7, 8)

    try:
        c = math.floor(c)
    except ValueError as e:
        logging.warn(e)
        return _temp_icons.get(7, 7, 8)

    if c > 40:
        return _temp_icons.get(0, 7, 8)
    if c < -9:
        return _temp_icons.get(1, 7, 8)

    c = 40 - c
    return _temp_icons.get(c%8, c//8, 8)

def conditions(c):
    if isinstance(c, str):
        if c in _cond_names:
            c = _cond_names[c]
        else:
            logging.warn("No icon for condition '%s'" % c)
            return _cond_icons.get(7, 7, 8)

    try:
        c = math.floor(c)
    except Exception as e:
        logging.warn(e)
        return _temp_icons.get(7, 7, 8)

    if c is None or c < 0 or c > 30:
        return _cond_icons.get(7, 7, 8)
    else:
        return _cond_icons.get(c%8, c//8, 8)
