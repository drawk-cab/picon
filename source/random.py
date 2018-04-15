#!/usr/bin/python3

import random
from icons import base
from source import source

class RandomNumber(source.DataSource):
    '''Returns a random number whenever it is read'''

    @staticmethod
    def define_args(parser):
        parser.add_argument("min", type=int, help="Minimum")
        parser.add_argument("max", type=int, help="Maximum")
        source.DataSource.define_args(parser)

    def __init__(self, **args):
        self.min = args["min"]
        self.max = args["max"]
        source.DataSource.__init__(self, **args)

    def read(self):
        return source.Report(base.number( random.randrange(self.min, self.max+1) ),
            banner=base.random_banner)

source.DataSource.CHOICES["random"] = RandomNumber
