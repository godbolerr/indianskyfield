from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.toposlib import Topos
from skyfield import eclipselib
import datetime as dt

# –13200 to 17191

ts = api.load.timescale()
eph = load('de431t.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

ist = timezone('Asia/Kolkata')
kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)
kuruKshetraObserver = eph['Earth'] + kuruKshetra

#now = ist.localize(dt.datetime.now())
#midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
#next_midnight = midnight + dt.timedelta(days=1)
#t0 = ts.from_datetime(midnight)
#t1 = ts.from_datetime(next_midnight)

t0 = ts.utc(-5000, 1, 1)
t1 = ts.utc(0, 1, 1)
t, y, details = eclipselib.lunar_eclipses(t0, t1, eph)

for ti, yi in zip(t, y):
    
    year, month, day, hour, minute, second = ti.tai_calendar()
    
    print(ti.tt, year, month, day, hour, minute, second,eclipselib.LUNAR_ECLIPSES[yi], sep=",")
    
    
    
    
    