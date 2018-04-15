#!/usr/bin/python3

import random
from icons import icons, base
from source.base_sources import DataSource

class RandomNumber(DataSource):
    '''Returns a random number whenever it is read'''

    @staticmethod
    def define_args(parser):
        parser.add_argument("min", type=int, help="Minimum")
        parser.add_argument("max", type=int, help="Maximum")
        DataSource.define_args(parser)

    def __init__(self, **args):
        self.min = args["min"]
        self.max = args["max"]
        DataSource.__init__(self, **args)

    def read(self):
        return icons.Report(base.number( random.randrange(self.min, self.max+1) ),
            banner=base.random_banner)

DataSource.CHOICES["random"] = RandomNumber
