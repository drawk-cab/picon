from skyfield import api, almanac
import datetime
import json
import pytz
import os

# FIXME: this whole thing only works in utc.
home = api.Topos(os.environ['HOME_LAT'], os.environ['HOME_LON'])

p = api.load('de421.bsp')
ts = api.load.timescale()
now = ts.now()
dtnow = datetime.datetime.utcnow().replace(tzinfo=api.utc)

window = datetime.timedelta(1)
guess_start = ts.utc(dtnow-window)
guess_end = ts.utc(dtnow+window)

sun_times, sun_events = almanac.find_discrete(guess_start, guess_end, almanac.sunrise_sunset(p, home))

t = { 'events': [] }

for i, is_sunrise in enumerate(sun_events):
    sun_time = sun_times[i]
    event_name = 'set'
    if is_sunrise:
        event_name = 'rise'
    t['events'].append( {
        'event': event_name,
        'time': sun_time.utc_iso()
    })

print(json.dumps(t))
