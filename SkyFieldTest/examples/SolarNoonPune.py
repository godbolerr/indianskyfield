import datetime as dt
from pytz import timezone
from skyfield import almanac
from skyfield.api import N, W, wgs84, load

zone = timezone('Asia/Kolkata')
now = zone.localize(dt.datetime.now())
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = midnight + dt.timedelta(days=1)

ts = load.timescale()
t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)
eph = load('de421.bsp')
pune = wgs84.latlon(18.5204 , 73.8567 )

f = almanac.meridian_transits(eph, eph['Sun'], pune)
times, events = almanac.find_discrete(t0, t1, f)

# Select transits instead of antitransits.
times = times[events == 1]

t = times[0]
tstr = str(t.astimezone(zone))[:19]
print('Pune Solar Solar noon:', tstr)
