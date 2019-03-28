#!/usr/bin/python3

import logging
import json
import pytz
import datetime
import dateutil.parser
from icons import icons, planets, base
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

        return self.report(daytime, next.hour, next.minute)

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

        return self.report(last_sunrise.isoweekday(), hour, minute)

    def report(self, sunrise_weekday, hour, minute):
        return [ source.Report(planets.hour(hour, sunrise_weekday, colour=icons.RED), banner = planets.weekday(sunrise_weekday, colour=icons.GREEN)),
                 source.Report(base.number(minute), banner = base.number(hour))
               ]

source.DataSource.CHOICES["sunrise"] = Sunrise
source.DataSource.CHOICES["planetary-hour"] = PlanetaryHour

