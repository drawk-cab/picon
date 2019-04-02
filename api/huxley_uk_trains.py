import requests
import datetime
import json
import pytz
import os

accessToken = os.environ["HUXLEY_ACCESS_TOKEN"]

# CRS codes here: http://www.nationalrail.co.uk/static/documents/content/station_codes.csv
crs = os.environ["HUXLEY_START_CRS"]
filter = os.environ["HUXLEY_END_CRS"]
service_mode = "train"
service_name = os.environ["HUXLEY_SERVICE"]


url = "https://huxley.apphb.com/departures/{}/to/{}?accessToken={}".format(crs, filter, accessToken)
mode_props = { "train": "trainServices", "bus": "busServices", "ferry": "ferryServices" }


r = requests.get(url)
j = r.json()

def hhmm_to_datetime(hhmm):
    if ':' not in hhmm:
        raise ValueError
    hh, mm = hhmm.split(':')
    now = datetime.datetime.now(tz=pytz.timezone('Europe/London'))
    then = now.replace(hour=int(hh), minute=int(mm)) #datetime.datetime(now.year, now.month, now.day, int(hh), int(mm), tz=pytz.timezone('Europe/London'))
    if then<now:
        then += datetime.timedelta(1)
    return then


out = []

for mode, prop in mode_props.items():
    services = j.get(prop, None)
    if services:
        for service in services:
            try:
                std = hhmm_to_datetime(service['std'])
                if service['etd']=="On time":
                    etd = std
                else:
                    etd = hhmm_to_datetime(service['etd'])
                report = { 'service':service_name, 'mode':mode, 'scheduled': std.isoformat(), 'estimated': etd.isoformat() }
                if mode != service_mode:
                    report['replacement'] = True
                out.append(report)

            except ValueError:
                pass

print(json.dumps(out))
