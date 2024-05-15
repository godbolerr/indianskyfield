from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime as dt

ts = api.load.timescale()
ist = timezone('Asia/Kolkata')

eph = load('de422.bsp')
sun = eph['sun']

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon

ist = timezone('Asia/Kolkata')
now = ist.localize(dt.datetime.now())
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = midnight + dt.timedelta(days=1)

t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)

t, y = almanac.find_risings(puneObserver, sun, t0, t1)

tstr = str(t.astimezone(ist))
print(tstr)


