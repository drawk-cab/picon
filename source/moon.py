
#!/usr/bin/python3

import logging
import json
import pytz
import datetime
import dateutil.parser
from icons import icons, planets, base
from source import source

class Moon(source.FileDataSource):
    '''Returns icons for the current phase and % of the moon given a JSON of the form

{
  "phase": <phase in degrees>,
  "illumination": <percentage illuminated>
}
'''

    def read(self):
        obj = self._readJSON()
        if obj is None:
            return []

        return self.report(obj['phase'], obj['illumination'])

    def report(self, phase, illumination):
        if phase>180:
            colour = icons.GREEN # waxing
        else:
            colour = icons.RED # waning
        return source.Report(base.number(illumination, colour),
                             banner=planets.moon_phase_angle(phase),
                             label="Moon:{}deg {}%".format(phase, illumination))

source.DataSource.CHOICES["moon"] = Moon

