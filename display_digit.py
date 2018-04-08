#!/usr/bin/python3

import argparse
import time
from source.digit import SingleDigit
from device import Device

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Display a single digit from a file.")

    parser.add_argument("-d", "--display", default="stdout", choices=Device.CHOICES.keys(),
                       help="Where to display")

    parser.add_argument("-f", "--filename", type=str, default="samples/digit",
                       help="Name of a file containing a single digit to read")

    args = parser.parse_args()

    source = SingleDigit(filename=args.filename)

    with Device.CHOICES[args.display]() as use_device:
        while True:
            use_device.display(source.read()[0])
            time.sleep(1)


