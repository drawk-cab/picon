#!/usr/bin/python3

import logging
import json
import pytz
import datetime
import dateutil.parser
from icons import icons, planets, base
from source import source

class Sunrise(source.FileDataSource):
    '''Returns the time of sunrise if night time, or sunset if daytime.

{
    "daytime": <true if sun is up>
    "next": <next sunrise or sunset time>,
    "weekday": <weekday 0..7>
    "lastSunrise": <last sunrise time>,
    "sunriseWeekday": <weekday at last sunrise>,
    "hour": solar hour (12 between each sunrise/set)
    "minute": solar minute (60 in each solar hour)
}
'''

    def read(self):
        obj = self._readJSON()
        if obj is None:
            return []

        # FIXME: extract hour and minute in a better way
        return self.report(obj['daytime'], int(obj['next'][11:13]), int(obj['next'][14:16]))

    def report(self, is_daytime, hour, minute):
        if is_daytime:
          return [ source.Report(base.number(minute, colour=icons.RED), banner=base.number(hour, icons.RED)) ]
        else:
          return [ source.Report(base.number(minute, colour=icons.AMBER), banner=base.number(hour, icons.AMBER)) ]

class PlanetaryHour(source.FileDataSource):
    def read(self):
        obj = self._readJSON()
        if obj is None:
            return []

        return self.report(obj['sunriseWeekday'], obj['hour'], obj['minute'])

    def report(self, sunrise_weekday, hour, minute):
        return [ source.Report(planets.hour(hour, sunrise_weekday, colour=icons.RED), banner = planets.weekday(sunrise_weekday, colour=icons.GREEN)),
                 source.Report(base.number(minute), banner = base.number(hour))
               ]

source.DataSource.CHOICES["sunrise"] = Sunrise
source.DataSource.CHOICES["planetary-hour"] = PlanetaryHour

