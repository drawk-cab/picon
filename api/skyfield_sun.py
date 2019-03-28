from skyfield import api, almanac
import datetime
import json
import pytz
import os

# FIXME: this whole thing only works in utc.
home = api.Topos(os.environ['HOME_LON'], os.environ['HOME_LAT'])

p = api.load('de421.bsp')
ts = api.load.timescale()
now = ts.now()
dtnow = datetime.datetime.utcnow().replace(tzinfo=api.utc)

window = datetime.timedelta(1)
guess_start = ts.utc(dtnow-window)
guess_end = ts.utc(dtnow+window)

sun_times, sun_events = almanac.find_discrete(guess_start, guess_end, almanac.sunrise_sunset(p, home))

daytime = True
last = None
last_sunrise = None
next = None
for i, is_sunrise in enumerate(sun_events):
    if sun_times[i].utc_datetime() < dtnow:
        last = sun_times[i]
        daytime = bool(is_sunrise)
        if is_sunrise:
            last_sunrise = last
    else:
        next = sun_times[i]
        break

hd_since = now - last
hd_length = next - last

minute = (hd_since / hd_length) * 12 * 60

if daytime:
    hour = 0
else:
    hour = 12

t = {
    "daytime": daytime,
    "next": next.utc_iso(),
    "weekday": dtnow.isoweekday(),
    "lastSunrise": last_sunrise.utc_iso(),
    "sunriseWeekday": last_sunrise.utc_datetime().isoweekday(),
    "hour": (minute // 60) + hour,
    "minute": minute % 60
}

print(json.dumps(t))
