from skyfield import api, almanac
import datetime
import json
import pytz

p = api.load('de421.bsp')
ts = api.load.timescale()
now = ts.now()

ill = almanac.fraction_illuminated(p, 'moon', now)
pha = almanac.phase_angle(p, 'moon', now).degrees

t = { 'illumination': ill*100,
      'phase': pha }

# guess when new moon was
month_angle = 360 / 29.53
window = datetime.timedelta(1)
guess = datetime.datetime.utcnow().replace(tzinfo=api.utc) - datetime.timedelta(((pha+180)%360) / month_angle)
guess_start = ts.utc(guess-window)
guess_end = ts.utc(guess+window)

moon_times, moon_phases = almanac.find_discrete(guess_start, guess_end, almanac.moon_phases(p))

for i, p in enumerate(moon_phases):
    if p==0: # full
        t['age'] = now - moon_times[i]

print(json.dumps(t))
