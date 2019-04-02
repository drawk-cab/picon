
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

[{
  "mode": "train" (default) | "bus" | "tram",
  "scheduled": <ISO time>,
  "estimated": <ISO time>
}]
'''

    @staticmethod
    def define_args(parser):
        parser.add_argument("delay", type=int, help="How much delay warrants a red warning (minutes)", default=15)
        parser.add_argument("warn", type=int, help="Final warning length (minutes)", default=10)
        parser.add_argument("walk", type=int, help="How much time needed to get to the train (minutes)", default=10)
        source.FileDataSource.define_args(parser)

    def __init__(self, **args):
        self.banner = None
        self.lookahead = datetime.timedelta(0, args["lookahead"] * 60)
        self.delay = datetime.timedelta(0, args["delay"] * 60)
        self.warn = datetime.timedelta(0, args["warn"] * 60)
        self.walk = datetime.timedelta(0, args["walk"] * 60)
        source.FileDataSource.__init__(self, **args)

    def read(self):
        all = self._readJSON()
        if not all:
            return source.Report(banner=transport.mode(transport.TRAIN),
                             label="Transport:No services")

        out = []
        prev_mode = None
        prev_service = None

        for obj in all:
            now = datetime.datetime.now(pytz.utc)

            mode = obj.get("mode",None)
            if mode == "bus":
                mode = transport.BUS
            elif mode == "tram":
                mode = transport.TRAM
            else:
                mode = transport.TRAIN

            service = obj.get("service",None)

            replacement = obj.get("replacement",False)

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

            if wait < self.walk:
                continue # missed it
            if wait > self.lookahead:
                continue # too far away
            if delay > self.delay:
                is_delayed = True
            elif delay > datetime.timedelta(0):
                is_delayed = None
            else:
                is_delayed = False

            if mode == prev_mode and service == prev_service:
                out.append(self.report(None, False, wait, is_delayed, delay, replacement))
            else:
                out.append(self.report(mode, service, wait, is_delayed, delay, replacement))
                prev_mode = mode
                prev_service = service
        return out

    def report(self, mode, service, wait, is_delayed, delay, is_replacement=False):
        if mode is not None:
            if is_replacement:
                mode = transport.mode(mode, colour=icons.RED)
            else:
                mode = transport.mode(mode)

        if service is False: # Means this was the same as before, as opposed to None (no value)
            return source.Report(
                             transport.time_left(wait, self.walk, self.warn), 
                             transport.delay(delay, self.delay),
                             banner=mode,
                             label="Transport:{}-{} {} {} {}".format(repr(mode), repr(service), wait, is_delayed, delay))
        elif service is not None:
            try:
                n = int(service)
                if n<0 or n>99:
                    raise ValueError
                service = base.number(n)
            except ValueError:
                service = None

        return source.Report(service,
                             transport.time_left(wait, self.walk, self.warn), 
                             transport.delay(delay, self.delay),
                             banner=mode,
                             label="Transport:{}-{} {} {} {}".format(repr(mode), repr(service), wait, is_delayed, delay))

class ShortTransport(Transport):
    def report(self, mode, wait, is_delayed, delay):
        return source.Report(
            transport.is_delayed(is_delayed, mode),
            transport.time_left(wait, self.warn, self.warn),
            label="ShortTransport:{} {} {} {}".format(mode, wait, is_delayed, delay))

source.DataSource.CHOICES["short-transport"] = ShortTransport
source.DataSource.CHOICES["transport"] = Transport

