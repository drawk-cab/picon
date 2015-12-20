#!/usr/bin/python3

import collections
import metoffer
import argparse
import json
import datetime

def make_jsonable(obj):
    if isinstance(obj, collections.Mapping):
        obj = {key: make_jsonable(value) for key, value in obj.items()}
    elif isinstance(obj, collections.MutableSequence):
        obj = [make_jsonable(value) for value in obj]
    elif isinstance(obj, tuple):
        obj = [make_jsonable(value) for value in obj]
    elif isinstance(obj, datetime.datetime):
        obj = obj.isoformat()
    else:
        pass
    return obj

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Discover nearest Met. Office station to you and get its id.')

    parser.add_argument('key', type=str, help='Your DataPoint API key')
    parser.add_argument('station', type=str, help='Station number')

    args = parser.parse_args()

    M = metoffer.MetOffer(args.key)
    x = M.loc_forecast(args.station, metoffer.THREE_HOURLY)
    y = metoffer.parse_val(x)

    print(json.dumps(make_jsonable({ "name":y.name,
                    "country":y.country,
                    "continent":y.continent,
                    "lat":y.lat,
                    "lon":y.lon,
                    "elevation":y.elevation,
                    "ident":y.ident,
                    "data_date":y.data_date,
                    "dtype":y.dtype,
                    "data":y.data })))
