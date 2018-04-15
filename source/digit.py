#!/usr/bin/python3

from icons import icons, base
import logging
from source.base_sources import DataSource, FileDataSource

class SingleDigit(FileDataSource):
    '''Returns an icon corresponding to the first byte of the input file,
which must be a single ASCII digit.'''

    def __init__(self, **args):
        FileDataSource.__init__(self, **args)

    def read(self):
        try:
            char = self._readFile(1)
            n = int(char)
        except (ValueError, TypeError):
            logging.warn("First byte of file %s was %s, not a digit" % (self.filename, char))
            return icons.Report(base.number(None),
                banner=base.digit_banner)

        return icons.Report(base.number(n),
            banner=base.digit_banner)

DataSource.CHOICES["digit"] = SingleDigit
