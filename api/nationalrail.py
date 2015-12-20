#!/usr/bin/python3

import argparse
import json
import datetime
import urllib.request

def get_wait(when, now_today):
    # convert slightly unhelpful API responses into real times
    try:
        h, m = when.split(":")
    except:
        return None
    when_today = int(h)*60 + int(m)
    wait = when_today - now_today
    if wait < -12*60:
        # assume time refers to tomorrow
        wait += 24*60
    return wait*60

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

    now = datetime.datetime.now().replace(second=0, microsecond=0)
    now_today = now.hour*60 + now.minute

    for train in response["trainServices"]:
        std_wait = get_wait(train["std"], now_today)
        if std_wait:
            std = now+datetime.timedelta(0,std_wait)
        else:
            std = now

        etd_wait = get_wait(train["etd"], now_today)
        if etd_wait:
            etd = now+datetime.timedelta(0,etd_wait)
        else:
            etd = std

        status.append({"std": std.isoformat(),
                       "etd": etd.isoformat()})

    print(json.dumps(status))
