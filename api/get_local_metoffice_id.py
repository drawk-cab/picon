#!/usr/bin/python3

import metoffer
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Discover nearest Met. Office station to you and get its id.')

    parser.add_argument('key', type=str, help='Your DataPoint API key')
    parser.add_argument('lat', type=float, help='Your latitude')
    parser.add_argument('lon', type=float, help='Your longitude')

    args = parser.parse_args()

    M = metoffer.MetOffer(args.key)
    x = M.nearest_loc_obs(args.lat, args.lon)
    y = metoffer.parse_val(x)

    #print( y.data )
    print( '%s - %s, %s' % (y.ident, y.name, y.country))


