#!/usr/bin/python3

import random
from icons import base, icons
from source.base_sources import DataSource

class Counter(DataSource):
    '''Increments whenever it is read'''

    @staticmethod
    def define_args(parser):
        parser.add_argument("max", type=int, help="Maximum")
        DataSource.define_args(parser)

    def __init__(self, **args):
        self.value = 0
        self.max = args["max"]
        DataSource.__init__(self, **args)

    def read(self):
        self.value = (self.value+1) % self.max
        return icons.Report(base.number( self.value, colour=(self.value/self.max,0,0) ),
            banner=base.digit_banner)

DataSource.CHOICES["counter"] = Counter
