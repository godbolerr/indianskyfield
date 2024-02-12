import datetime as dt
from pytz import timezone
from skyfield import almanac
from skyfield.api import N, W, wgs84, load

zone = timezone('US/Eastern')
now = zone.localize(dt.datetime.now())
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = midnight + dt.timedelta(days=1)

ts = load.timescale()
t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)
eph = load('de421.bsp')
bluffton = wgs84.latlon(40.8939 * N, 83.8917 * W)

f = almanac.meridian_transits(eph, eph['Sun'], bluffton)
times, events = almanac.find_discrete(t0, t1, f)

# Select transits instead of antitransits.
times = times[events == 1]

t = times[0]
tstr = str(t.astimezone(zone))[:19]
print('Solar noon:', tstr)
