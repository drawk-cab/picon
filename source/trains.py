
#!/usr/bin/python3

import icons.trains as icons
import logging
import json
import pytz
import datetime
import dateutil.parser
from source.base_sources import FileDataSource, DataSource

class Trains(FileDataSource):
    '''Returns icons for a train service report in a JSON input file of the format

{ "scheduled": <ISO time>, "estimated": <ISO time> }
'''

    def __init__(self, **args):
        self.banner = None
        FileDataSource.__init__(self, **args)

    def read(self):
        obj = self._readJSON()

        if obj is None:
            return [icons.temperature(None)]

        now = datetime.datetime.now(pytz.utc)

        try:
            scheduled = dateutil.parser.parse(obj.get("scheduled",None))
        except (ValueError, TypeError):
            scheduled = None

        try:
            estimated = dateutil.parser.parse(obj.get("estimated",None))
        except (ValueError, TypeError):
            estimated = None

        delay = estimated - scheduled
        wait = estimated - now

        status = None
        if delay > datetime.timedelta(0,600):
            status = True
        elif delay <= datetime.timedelta(0):
            status = False

        return [icons.train_is_delayed(status), icons.delay(delay), icons.time_left(wait)]

DataSource.CHOICES["trains"] = Trains
