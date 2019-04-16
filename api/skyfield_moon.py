from skyfield import api, almanac
import datetime
import json
import pytz

p = api.load('de421.bsp')
ts = api.load.timescale()
now = ts.now()

ill = almanac.fraction_illuminated(p, 'moon', now)
pha = almanac.phase_angle(p, 'moon', now).degrees

t = { 'illumination': ill*100 }

# Inconveniently, phase angle is defined between 0 and 180 since astronomers don't know which way is up.
# So we have to go get the dates of the moon phases to figure out whether waxing or waning.
window = datetime.timedelta(30)
guess = datetime.datetime.utcnow().replace(tzinfo=api.utc)
guess_start = ts.utc(guess-window)
guess_end = ts.utc(guess+window)

moon_times, moon_phases = almanac.find_discrete(guess_start, guess_end, almanac.moon_phases(p))

times = []
last = None

for i, p in enumerate(moon_phases):
    times.append((int(p), moon_times[i].utc_iso()))
    if now - moon_times[i] > 0:
        last = i # assume skyfield gave us the times in order

if i>=2: # last phase was full or 3rd quarter, i.e., waning
   pha = -pha

t["now"] = now.utc_iso()
t["phase"] = pha
t["times"] = times

print(json.dumps(t))
