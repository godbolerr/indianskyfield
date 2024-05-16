from datetime import datetime 
from datetime import timedelta
import datetime


from pytz import timezone
import pytz  
from skyfield import api
from skyfield import almanac
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load



ts = api.load.timescale()
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
lat=18.5204
long=73.8567 
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
pune = wgs84.latlon(lat * N, long * E)
puneObserver = eph['Earth'] + pune
istZone = timezone('Asia/Kolkata')

refDate = datetime.datetime(1000,3,1,0,0,0)
midnight = refDate.replace(tzinfo=istZone)
next_midnight = midnight + datetime.timedelta(days=1)

t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)

st, _ = almanac.find_risings(puneObserver, sun, t0, t1)


sunriseLocal = st[0].astimezone(istZone)


print(sunriseLocal)