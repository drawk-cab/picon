#!/usr/bin/python3

import device
import argparse
from source import DataSource
import time
import json

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Display informative icons.")

    parser.add_argument("-d", "--display", default="stdout", choices=device.CHOICES.keys(),
                       help="Where to display")

    parser.add_argument("-c", "--config", type=str,
                       help="Configuration JSON file")

    parser.add_argument("-l", "--loop", type=int, default=0,
                       help="Number of minutes to loop for (0 = display once only)")

    subparsers = parser.add_subparsers(help="Which API to use", dest="cmd")

    for name, source_class in DataSource.CHOICES.items():
        subparser = subparsers.add_parser(name, help=source_class.__doc__)
        source_class.define_args(subparser)

    args = parser.parse_args()

    if args.cmd:
        rotate = [ DataSource.CHOICES[args.cmd](**vars(args)) ]
    elif args.config:
        rotate = []
        config = json.load(open(args.config,"r"))
        for source_args in config:
            rotate.append( DataSource.CHOICES[source_args["source"]](**source_args) )
    else:
        rotate = [ DataSource.CHOICES["random"](min=-10,max=40) ]

    loop = True
    start_time = time.time()

    with device.CHOICES[args.display]() as use_device:
        while loop:
            for each_source in rotate:
                use_device.display(each_source.banner)
                time.sleep(1)
                frames = each_source.read()
                for frame in frames:
                    use_device.display(frame)
                    time.sleep(2)
            if (time.time() - start_time) > (args.loop*60):
                loop = False


