#!/usr/bin/python3

from icons import weather, icons
import logging
import json
from source.base_sources import FileDataSource, DataSource

class Weather(FileDataSource):
    '''Returns icons for a weather report in a JSON input file of the format

{ "temperature": <number>, "conditions": <string> }
'''

    def __init__(self, **args):
        self.banner = None
        FileDataSource.__init__(self, **args)

    def read(self):
        obj = self._readJSON()

        if obj is None:
            return icons.Report(weather.temperature(None))

        try:
            t = int(obj.get("temperature",None))
        except (ValueError, TypeError):
            t = None

        c = obj.get("conditions",None)

        return icons.Report(weather.conditions(c), weather.temperature(t))

DataSource.CHOICES["weather"] = Weather
