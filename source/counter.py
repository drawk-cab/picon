#!/usr/bin/python3

import random
import icons.base as icons
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
        self.banner = icons.digit_banner
        DataSource.__init__(self, **args)

    def read(self):
        self.value = (self.value+1) % self.max
        return [icons.number( self.value, colour=(self.value/self.max,0,0) )]

DataSource.CHOICES["counter"] = Counter
