import requests
import datetime
import json
import pytz
import os

accessToken = os.environ["HUXLEY_ACCESS_TOKEN"]

# CRS codes here: http://www.nationalrail.co.uk/static/documents/content/station_codes.csv
crs = os.environ["HUXLEY_START_CRS"]
filter = os.environ["HUXLEY_END_CRS"]

url = "https://huxley.apphb.com/departures/{}/to/{}?accessToken={}".format(crs, filter, accessToken)

r = requests.get(url)
j = r.json()

def hhmm_to_datetime(hhmm):
    if ':' not in hhmm:
        raise ValueError
    hh, mm = hhmm.split(':')
    now = datetime.datetime.now(pytz.utc)
    then = datetime.datetime(now.year, now.month, now.day, int(hh), int(mm), tzinfo=pytz.utc)
    if then<now:
        then += datetime.timedelta(1)
    return then


t = []
for train in j.get('trainServices',[]):
    try:
        std = hhmm_to_datetime(train['std'])
        if train['etd']=="On time":
            etd = std
        else:
            etd = hhmm_to_datetime(train['etd'])
        t.append({ 'mode':'train', 'scheduled': std.isoformat(), 'estimated': etd.isoformat() })
    except ValueError:
        pass

print(json.dumps(t))
