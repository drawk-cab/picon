#!/usr/bin/python3

import random
from icons import base, icons
from source import source

class Counter(source.DataSource):
    '''Increments whenever it is read'''

    @staticmethod
    def define_args(parser):
        parser.add_argument("max", type=int, help="Maximum")
        source.DataSource.define_args(parser)

    def __init__(self, **args):
        self.value = 0
        self.max = args["max"]
        source.DataSource.__init__(self, **args)

    def read(self):
        self.value = (self.value+1) % self.max
        return source.Report(base.number( self.value, colour=(self.value/self.max,0,0) ),
            banner=base.count_banner)

source.DataSource.CHOICES["counter"] = Counter
