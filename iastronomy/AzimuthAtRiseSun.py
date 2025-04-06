from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime as dt

ts = api.load.timescale()
ist = timezone('Asia/Kolkata')

eph = load('de431t.bsp')
sun = eph['sun']

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon

csvFile="PuneSunriseAzimuthOneYear.csv"

ist = timezone('Asia/Kolkata')
now = ist.localize(dt.datetime.now())
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = midnight + dt.timedelta(days=365)

t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)

t, y = almanac.find_risings(puneObserver, sun, t0, t1)

alt, az, dist = puneObserver.at(t).observe(sun).apparent().altaz()

for ti, yi, alti in zip(t, y, az.degrees):
    punetime = ti.astimezone(ist)
    print('{} ,{:.4f}'.format( punetime, alti))