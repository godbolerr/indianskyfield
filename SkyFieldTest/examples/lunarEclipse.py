from skyfield.api import N, W, wgs84, load
from skyfield import eclipselib

ts = load.timescale()
eph = load('de421.bsp')

t0 = ts.utc(2022, 1, 1)
t1 = ts.utc(2025, 1, 1)
t, y, details = eclipselib.lunar_eclipses(t0, t1, eph)

for ti, yi in zip(t, y):
    print(ti.utc_strftime('%Y-%m-%d %H:%M'),
          'y={}'.format(yi),
          eclipselib.LUNAR_ECLIPSES[yi])