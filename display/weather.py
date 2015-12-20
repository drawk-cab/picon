#!/usr/bin/python3

import icon
TEMP_ICONS = icon.IconSet("icons/weather-temperatures.ppm")
TYPE_ICONS = icon.IconSet("icons/weather-types.ppm")

def get_temperature(c):
    if c is None:
        return TEMP_ICONS.get(7, 7, 8)
    if c > 40:
        return TEMP_ICONS.get(0, 7, 8)
    if c < -9:
        return TEMP_ICONS.get(1, 7, 8)

    c = 40 - c
    return TEMP_ICONS.get(c%8, c//8, 8)

def get_weather_type(c):
    if c is None or c < 0 or c > 30:
        return TYPE_ICONS.get(7, 7, 8)
    else:
        return TYPE_ICONS.get(c%8, c//8, 8)
