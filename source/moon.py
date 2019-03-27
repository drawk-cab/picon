
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
        return self.report(obj['phase'], obj['illumination'])

    def report(self, phase, illumination):
        return [
                source.Report(base.number(illumination), banner=planets.moon_phase_angle(phase))
               ]

source.DataSource.CHOICES["moon"] = Moon

