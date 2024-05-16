from pytz import timezone
import pytz
from skyfield import api
from skyfield.api import N, E, wgs84, load
from skyfield.api import GREGORIAN_START
from datetime import timedelta

ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
ist = timezone('Asia/Kolkata')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

t = ts.utc(2000, 1, 1,14,30,0) #+  timedelta(hours=5,minutes=30)
dt = t.astimezone(pytz.timezone("Asia/Kolkata"))

print(t.tdb_calendar() )
print(dt)