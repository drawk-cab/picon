#!/usr/bin/python3

import logging
import json
import pytz, tzlocal
import datetime
import dateutil.parser
from icons import icons, planets, base, weather
from source import source
import re

class Sunrise(source.FileDataSource):
    '''Returns the time of sunrise if night time, or sunset if daytime.

{
    "events": [{
        "event": <rise|set>,
        "time": <ISO time of event>
    }...]
}
'''
    @staticmethod
    def fromisoformat(s):
        m = re.match('(....)-(..)-(..).(..):(..):(..)(.*)$', s)
        if not m:
            raise ValueError(s)
        tz = m.group(7)
        tzname = None
        if tz=='Z':
            tzname='utc'
        if tzname is None:
            raise ValueError
        return datetime.datetime(*[int(m.group(x)) for x in range(1,7)], tzinfo=getattr(pytz, tzname))

    def read(self):
        obj = self._readJSON()
        if obj is None or not 'events' in obj:
            return []

        daytime = None
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        last = None
        next = None
        last_sunrise = None
        for e in obj['events']:
            t = Sunrise.fromisoformat(e['time'])
            if t < now:
                last = t
                if e['event']=='rise':
                    last_sunrise = t
                    daytime = True
                else:
                    daytime = False
            else:
                next = t
                break

        next = next.astimezone(tzlocal.get_localzone())
        return self.report(daytime, next.hour, next.minute)

    def report(self, is_daytime, hour, minute):
        if is_daytime:
          return source.Report(base.number(hour, icons.RED), base.number(minute, colour=icons.RED),
                      banner=weather.conditions('sun'),
                      label="Sunrise:set {}{}".format(minute, hour))
        else:
          return source.Report(base.number(hour, icons.AMBER), base.number(minute, colour=icons.AMBER),
                      banner=weather.conditions('sun'),
                      label="Sunrise:rise {}{}".format(minute, hour))

class PlanetaryHour(source.FileDataSource):
    def read(self):
        obj = self._readJSON()
        if obj is None:
            return []

        daytime = None
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        last = None
        next = None
        last_sunrise = None
        for e in obj['events']:
            t = Sunrise.fromisoformat(e['time'])
            if t < now:
                last = t
                if e['event']=='rise':
                    last_sunrise = t
                    daytime = True
                else:
                    daytime = False
            else:
                next = t
                break

        halfday_length = next - last
        halfday_elapsed = (now - last) / halfday_length

        hour = int(halfday_elapsed * 12)
        minute = int(halfday_elapsed * 12 * 60) % 60
        if not daytime:
            hour += 12

        if not last_sunrise:
            return None # couldn't figure out what day it was

        return self.report(last_sunrise.isoweekday(), hour, minute)

    def report(self, sunrise_weekday, hour, minute):
        return source.Report(planets.hour(hour, sunrise_weekday, colour=icons.RED),
                               base.number(hour),
                               base.number(minute),
                               banner=planets.weekday(sunrise_weekday, colour=icons.GREEN),
                               label="PlanetaryHour:{} {}{}".format(sunrise_weekday,hour,minute))

source.DataSource.CHOICES["sunrise"] = Sunrise
source.DataSource.CHOICES["planetary-hour"] = PlanetaryHour

