#!/usr/bin/python3

import argparse
import json
import datetime
import pytz
import urllib.request

UK_TZ = pytz.timezone('Europe/London')

def get_wait(when, now):
    # convert unhelpful API responses into relative times
    # (API gives HH:MM in UK time, and doesn't tell you what day it's talking about either)
    try:
        h, m = when.split(":")
    except:
        return None

    try:
        now_uk = now.astimezone(UK_TZ)
    except pytz.InvalidTimeError:
        # time is ambiguous or nonexistent, don't bother handling this
        return None

    if int(h)<now_uk.hour:
        try:
            tomorrow_uk = (now + datetime.timedelta(1)).astimezone(UK_TZ)
        except pytz.InvalidTimeError:
            # time is ambiguous or nonexistent, don't bother handling this
            return None

        then_uk = tomorrow_uk.replace(hour=int(h),minute=int(m),second=0,microsecond=0)
    else:
        then_uk = now_uk.replace(hour=int(h),minute=int(m),second=0,microsecond=0)

    try:
        then_uk = UK_TZ.normalize(then_uk)
    except pytz.InvalidTimeError:
        # train's time is ambiguous or nonexistent, don't bother handling this
        return None

    then = then_uk.astimezone(pytz.utc)

    return then-now

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Discover how trains are running.')

    parser.add_argument('key', type=str, help='Your OpenLDBWS API key')
    parser.add_argument('station', type=str, help='Station code')
    parser.add_argument('destination', type=str, help='Desstination station code')

    args = parser.parse_args()

    url = "https://huxley.apphb.com/departures/%s/to/%s/15/?accessToken=%s" % (args.station, args.destination, args.key)

    request = urllib.request.Request(url)
    response = json.loads(urllib.request.urlopen(request).read().decode())

    status = []

    now = datetime.datetime.now(datetime.timezone.utc)

    if "trainServices" in response and response["trainServices"]:
        for train in response["trainServices"]:
            std_wait = get_wait(train["std"], now)
            if std_wait:
                std = now+std_wait
            else:
                std = now

            etd_wait = get_wait(train["etd"], now)
            if etd_wait:
                etd = now+etd_wait
            else:
                etd = std

            status.append({"std": std.isoformat(),
                           "etd": etd.isoformat()})

    print(json.dumps(status))
