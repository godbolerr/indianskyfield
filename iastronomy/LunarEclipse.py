from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.toposlib import Topos
from skyfield import eclipselib



eph = load('de422.bsp')
babylon = Topos("29 N", "76 E")
istTz = timezone('Asia/Kolkata')
kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)
kuruKshetraObserver = eph['Earth'] + kuruKshetra

ts = load.timescale();
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

start_year = -2999

r = ts.tt(start_year,1,range(1,365))

t0 = ts.utc(-2999, 1, 1)
t1 = ts.utc(-3000, 1, 1)
t, y, details = eclipselib.lunar_eclipses(t0, t1, eph)

#for name, values in sorted(details.items()):
#    print(f'{name:24}  {values}')

for ti, yi in zip(t, y):
    #print(ti.utc_strftime('%Y-%m-%d %H:%M'),          'y={}'.format(yi),          eclipselib.LUNAR_ECLIPSES[yi])
    #print(ti,  ti.utc_jpl(),  ti.tai_calendar(),      eclipselib.LUNAR_ECLIPSES[yi])
    print(ti.tt,ti.tai_calendar(),      eclipselib.LUNAR_ECLIPSES[yi])
    
    
    
    
    