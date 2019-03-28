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

class Date(source.DataSource):
    '''Shows the current date'''

    def read(self):
        t = datetime.datetime.now()
        return source.Report(base.number( t.day, colour=icons.WHITE ),
            banner=base.number( t.month, colour=icons.RED ))

class Year(source.DataSource):
    '''Shows the current year'''

    def read(self):
        t = datetime.datetime.now()
        return source.Report(base.number( t.year % 100, colour=icons.BLUE ),
            banner=base.number( t.year // 100, colour=icons.BLUE ))

source.DataSource.CHOICES["time"] = Time
source.DataSource.CHOICES["date"] = Date
source.DataSource.CHOICES["year"] = Year
