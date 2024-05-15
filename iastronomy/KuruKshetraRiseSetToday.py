from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime as dt

ts = api.load.timescale()


eph = load('de422.bsp')
sun = eph['sun']

ist = timezone('Asia/Kolkata')
kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)
kuruKshetraObserver = eph['Earth'] + kuruKshetra


now = ist.localize(dt.datetime.now())
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = midnight + dt.timedelta(days=1)

t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)

t, y = almanac.find_risings(kuruKshetraObserver, sun, t0, t1)

tstr = str(t.astimezone(ist))
print(tstr)


