#!/usr/bin/python3

import random
import icons.base as icons
from . import *

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
        self.banner = icons.random_banner
        DataSource.__init__(self, **args)

    def read(self):
        return [icons.number( random.randrange(self.min, self.max+1) )]

DataSource.CHOICES["random"] = RandomNumber
