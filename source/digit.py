#!/usr/bin/python3

import logging
from icons import icons, base
from source import source

class SingleDigit(source.FileDataSource):
    '''Returns an icon corresponding to the first byte of the input file,
which must be a single ASCII digit.'''

    def __init__(self, **args):
        source.FileDataSource.__init__(self, **args)

    def read(self):
        try:
            char = self._readFile(1)
            n = int(char)
        except (ValueError, TypeError):
            logging.warn("First byte of file %s was %s, not a digit" % (self.filename, char))
            return source.Report(base.number(None),
                banner=base.digit_banner)

        return source.Report(base.number(n),
            banner=base.digit_banner)

source.DataSource.CHOICES["digit"] = SingleDigit
