#!/usr/bin/python3

import logging
import argparse
import time
import json
import source
import device

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Display informative icons in a repeating loop.")

    parser.add_argument("-d", "--display", default="stdout", choices=device.choices.keys(),
                       help="Where to display")

    parser.add_argument("-r", "--rotate", type=int, default=0,
                       help="Display rotation (snapped to 90 degrees on most devices)")

    parser.add_argument("-c", "--config", type=str,
                       help="Configuration JSON file")

    parser.add_argument("-l", "--loop", type=int, default=0,
                       help="Number of minutes to loop for (0 = display once only)")

    subparsers = parser.add_subparsers(help="Which API to use", dest="cmd")

    for name, source_class in source.choices.items():
        subparser = subparsers.add_parser(name, help=source_class.__doc__)
        source_class.define_args(subparser)

    args = parser.parse_args()

    if args.cmd:
        carousel = [ source.choices[args.cmd](**vars(args)) ]
    else:
        carousel = []
        if args.config:
            config = json.load(open(args.config,"r"))
        else:
            config = json.load(open("config.json","r"))
            logging.warn("No config.file specified, using 'config.json'")
        for source_args in config:
            carousel.append( source.choices[source_args["source"]](**source_args) )

    looping = True
    start_time = time.time()

    with device.choices[args.display](rotate=args.rotate) as use_device:
        while looping:
            for each_source in carousel:
                use_device.display(each_source.read(), each_source["transition"])
            if (time.time() - start_time) > (args.loop*60):
                loop = False


