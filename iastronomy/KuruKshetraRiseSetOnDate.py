from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
from skyfield.api import GREGORIAN_START



ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START



ist = timezone('Asia/Kolkata')

eph = load('de422.bsp')
sun = eph['sun']

# 29 degree 52 min, 76 degree , 76 min

kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)

kuruKshetraObserver = eph['Earth'] + kuruKshetra

t0 = ts.utc(-100, 1, 1)
t1 = ts.utc(-100, 1, 2)

t, y = almanac.find_risings(kuruKshetraObserver, sun, t0, t1)

bc_4714 = -4713
t = ts.tt(bc_4714, 11, 24, 12)
print(t.tt)


