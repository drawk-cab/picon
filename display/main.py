#!/usr/bin/python3

import device
import argparse
import api
import time

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Display informative icons.')

    parser.add_argument('-d', '--display', default="stdout", choices=device.CHOICES.keys(),
                       help='Where to display')

    parser.add_argument('-l', '--loop', type=int, default=0,
                       help='Number of minutes to loop for (0 = display once only)')

    parser.add_argument('-w', '--wait', type=float, default=2,
                       help='Time to wait between frames')

    parser.add_argument('-p', '--priority', type=float, default=0,
                       help='Lowest priority to display (0..1)')

    subparsers = parser.add_subparsers(help='Which API to use', dest='cmd')

    for name, api_class in api.CHOICES.items():
        subparser = subparsers.add_parser(name, help=api_class.HELP)
        api_class.define_args(subparser)

    args = parser.parse_args()

    if args.cmd:
        rotate = [api.CHOICES[args.cmd](**vars(args))]
    else:
        rotate = [ api.CHOICES["metoffice"](),
                   api.CHOICES["nationalrail"](walk=10) ]

    loop = True
    start_time = time.time()

    with device.CHOICES[args.display]() as use_device:
        while loop:
            for each_api in rotate:
                priority, frames = each_api.get()
                if priority >= args.priority:
                    for frame in frames:
                        use_device.display(frame)
                        time.sleep(args.wait)
            if (time.time() - start_time) > (args.loop*60):
                loop = False


