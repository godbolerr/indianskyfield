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

ist = timezone('Asia/Kolkata')


for curYear in range(2000, 2100, 1):
    
    t0 = ts.utc(curYear, 1, 1,0,0,0)
    t1 = ts.utc(curYear, 1, 2,0,0,0)
    t, y = almanac.find_settings(puneObserver, sun, t0, t1)
    alt, az, dist = puneObserver.at(t).observe(sun).apparent().altaz()
    punetime = t.astimezone(ist)
    
    print('{} ,{:.4f}'.format( punetime, az.degrees[0]))







