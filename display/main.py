#!/usr/bin/python3

import device
import argparse
import api
import time
import json

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Display informative icons.')

    parser.add_argument('-d', '--display', default="stdout", choices=device.CHOICES.keys(),
                       help='Where to display')

    parser.add_argument('-c', '--config', type=str,
                       help='Display configuration JSON file')

    parser.add_argument('-l', '--loop', type=int, default=0,
                       help='Number of minutes to loop for (0 = display once only)')

    parser.add_argument('-p', '--priority', type=float, default=0,
                       help='Lowest priority to display (0..1)')

    subparsers = parser.add_subparsers(help='Which API to use', dest='cmd')

    for name, api_class in api.CHOICES.items():
        subparser = subparsers.add_parser(name, help=api_class.__doc__)
        api_class.define_args(subparser)

    args = parser.parse_args()

    if args.cmd:
        rotate = [api.CHOICES[args.cmd](**vars(args))]
    elif args.config:
        rotate = []
        config = json.load(open(args.config,'r'))
        for api_args in config:
            rotate.append( api.CHOICES[api_args["api"]](**api_args) )
    else:
        rotate = [ api.CHOICES["metoffice"](sample="samples/metoffice"),
                   api.CHOICES["nationalrail"](sample="samples/nationalrail", walk=10) ]

    loop = True
    start_time = time.time()

    with device.CHOICES[args.display]() as use_device:
        while loop:
            for each_api in rotate:
                priority, frames, wait = each_api.get()
                if priority >= args.priority:
                    for frame in frames:
                        use_device.display(frame)
                        time.sleep(wait)
            if (time.time() - start_time) > (args.loop*60):
                loop = False


