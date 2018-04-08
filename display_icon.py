#!/usr/bin/python3

import argparse
import time
import icons.weather
import device

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Display a single icon until killed.")

    parser.add_argument("-d", "--display", default="stdout", choices=device.choices.keys(),
                       help="Where to display")

    parser.add_argument("-i", "--icon", type=str, default="sun",
                       help="What to display")

    args = parser.parse_args()

    i = icons.weather.conditions(args.icon)

    with device.choices[args.display]() as use_device:
        while True:
            use_device.display(i)
            time.sleep(999)


