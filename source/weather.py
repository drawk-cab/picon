#!/usr/bin/python3

import logging
import json
from icons import weather
from source import source

class Weather(source.FileDataSource):
    '''Returns icons for a weather report in a JSON input file of the format

{ "temperature": <number>, "conditions": <string> }
'''

    def __init__(self, **args):
        self.banner = None
        source.FileDataSource.__init__(self, **args)

    def read(self):
        obj = self._readJSON()

        if obj is None:
            return source.Report(weather.temperature(None))

        try:
            t = int(obj.get("temperature",None))
        except (ValueError, TypeError):
            t = None

        c = obj.get("conditions",None)

        return self.report(c, t)

    def report(self, c, t):
        return [ 
                source.Report(weather.conditions(c)),
                source.Report(weather.temperature(t), banner=weather.temp_banner)]

class ShortWeather(Weather):
    def report(self, c, t):
        return source.Report(weather.conditions(c),
                    weather.temperature(t))

source.DataSource.CHOICES["weather"] = Weather
source.DataSource.CHOICES["short-weather"] = ShortWeather
