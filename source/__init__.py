#!/usr/bin/python3

import random
import json
import icons.weather as weather
import icons.base as icons
import logging

class DataSource:
    '''No help for this API.'''
    CHOICES = {}

    @staticmethod
    def define_args(parser):
        pass

    def __init__(self, **args):
        if not hasattr(self,"banner"):
            self.banner = weather.conditions("sun")


class FileDataSource(DataSource):
    @staticmethod
    def define_args(parser):
        parser.add_argument('filename', type=str, help="Sample file name")
        DataSource.define_args(parser)

    def __init__(self, filename, **args):
        self.filename = filename
        DataSource.__init__(self, **args)

class SingleDigit(FileDataSource):
    '''Returns an icon corresponding to the first byte of the input file,
which must be a single ASCII digit.'''

    def __init__(self, **args):
        self.banner = icons.digit_banner
        FileDataSource.__init__(self, **args)

    def read(self):
        try:
            char = open(self.filename,'r').read(1)
            n = int(char)
        except ValueError:
            logging.warn("First byte of file %s was %s, not a digit" % (self.filename, char))
            return [icons.number(None)]

        return [icons.number(n)]

DataSource.CHOICES['digit'] = SingleDigit

class RandomNumber(DataSource):
    '''Returns a random number whenever it is read'''

    @staticmethod
    def define_args(parser):
        parser.add_argument('min', type=int, help="Minimum")
        parser.add_argument('max', type=int, help="Maximum")
        DataSource.define_args(parser)

    def __init__(self, **args):
        self.min = args["min"]
        self.max = args["max"]
        self.banner = icons.random_banner
        DataSource.__init__(self, **args)

    def read(self):
        return [icons.number( random.randrange(self.min, self.max) )]

DataSource.CHOICES['random'] = RandomNumber

