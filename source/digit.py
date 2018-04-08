#!/usr/bin/python3

import icons.base as icons
import logging
from source.base_sources import DataSource, FileDataSource

class SingleDigit(FileDataSource):
    '''Returns an icon corresponding to the first byte of the input file,
which must be a single ASCII digit.'''

    def __init__(self, **args):
        self.banner = icons.digit_banner
        FileDataSource.__init__(self, **args)

    def read(self):
        try:
            char = self._readFile(1)
            n = int(char)
        except (ValueError, TypeError):
            logging.warn("First byte of file %s was %s, not a digit" % (self.filename, char))
            return [icons.number(None)]

        return [icons.number(n)]

DataSource.CHOICES["digit"] = SingleDigit
