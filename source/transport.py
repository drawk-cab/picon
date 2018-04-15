
#!/usr/bin/python3

import icons.transport as icons
import logging
import json
import pytz
import datetime
import dateutil.parser
from source.base_sources import FileDataSource, DataSource

class Transport(FileDataSource):
    '''Returns icons for a train service report in a JSON input file of the format

{
  "mode": "train" (default) | "bus" | "tram",
  "scheduled": <ISO time>,
  "estimated": <ISO time>
}
'''

    def __init__(self, **args):
        self.banner = None
        FileDataSource.__init__(self, **args)

    def read(self):
        obj = self._readJSON()

        if obj is None:
            return []

        now = datetime.datetime.now(pytz.utc)

        mode = obj.get("mode",None)
        if mode == "bus":
            mode = icons.BUS
        elif mode == "tram":
            mode = icons.TRAM
        else:
            mode = icons.TRAIN

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

        return [icons.is_delayed(status, mode),
                icons.delay(delay),
                icons.time_left(wait)]

DataSource.CHOICES["transport"] = Transport
