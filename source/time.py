#!/usr/bin/python3

import datetime
from icons import base, icons
from source import source

class Time(source.DataSource):
    '''Shows the current time'''

    def read(self):
        t = datetime.datetime.now()
        return source.Report(base.number( t.minute, colour=icons.WHITE ),
            banner=base.number( t.hour, colour=icons.ORANGE ),
            label="Time:{}{}".format(t.hour,t.minute))

class Date(source.DataSource):
    '''Shows the current date'''

    def read(self):
        t = datetime.datetime.now()
        return source.Report(base.number( t.year % 100, colour=icons.BLUE ),
            base.number( t.month, colour=icons.ORANGE ),
            base.number( t.day, colour=icons.WHITE ),
            banner=base.number( t.year // 100, colour=icons.BLUE ),
            label="Date:{}-{}-{}".format(t.year,t.month,t.day))

source.DataSource.CHOICES["time"] = Time
source.DataSource.CHOICES["date"] = Date
