#!/usr/bin/python3

import datetime
from icons import base, icons
from source import source

class Time(source.DataSource):
    '''Shows the current time'''

    def read(self):
        t = datetime.datetime.now()
        return source.Report(base.number( t.minute, colour=icons.WHITE ),
            banner=base.number( t.hour, colour=icons.RED ))

source.DataSource.CHOICES["time"] = Time
