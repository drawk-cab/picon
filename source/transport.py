
#!/usr/bin/python3

import logging
import json
import pytz
import datetime
import dateutil.parser
from icons import icons, transport, base
from source import source

class Transport(source.FileDataSource):
    '''Returns icons for a train service report in a JSON input file of the format

{
  "mode": "train" (default) | "bus" | "tram",
  "scheduled": <ISO time>,
  "estimated": <ISO time>
}
'''

    @staticmethod
    def define_args(parser):
        parser.add_argument("delay", type=int, help="How much delay warrants a red warning (minutes)", default=15)
        parser.add_argument("notice", type=int, help="How much notice needed to get a red warning (minutes)", default=10)
        source.FileDataSource.define_args(parser)

    def __init__(self, **args):
        self.banner = None
        self.delay = datetime.timedelta(args["delay"] * 60)
        self.notice = datetime.timedelta(args["notice"] * 60)
        source.FileDataSource.__init__(self, **args)

    def read(self):
        obj = self._readJSON()

        if obj is None:
            return []

        now = datetime.datetime.now(pytz.utc)

        mode = obj.get("mode",None)
        if mode == "bus":
            mode = transport.BUS
        elif mode == "tram":
            mode = transport.TRAM
        else:
            mode = transport.TRAIN

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

        if delay > self.delay:
            is_delayed = True
        elif delay > datetime.timedelta(0):
            is_delayed = None
        else:
            is_delayed = False

        return self.report(mode, wait, is_delayed, delay)

    def report(self, mode, wait, is_delayed, delay):
        return [
                source.Report(transport.time_left(wait, self.notice), banner=transport.mode(mode)),
                source.Report(transport.delay(delay, self.delay), banner=base.plus_minus_banner)]

class ShortTransport(Transport):
    def report(self, mode, wait, is_delayed, delay):
        return source.Report(
            transport.is_delayed(is_delayed, mode),
            transport.time_left(wait, self.notice))

source.DataSource.CHOICES["short-transport"] = ShortTransport
source.DataSource.CHOICES["transport"] = Transport

