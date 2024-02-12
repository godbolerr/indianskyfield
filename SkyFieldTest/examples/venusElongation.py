from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from skyfield.searchlib import find_maxima

ts = load.timescale()
t0 = ts.utc(2030)
t1 = ts.utc(2050)

eph = load('de421.bsp')
sun, earth, venus = eph['sun'], eph['earth'], eph['venus']

def elongation_at(t):
    e = earth.at(t)
    s = e.observe(sun).apparent()
    v = e.observe(venus).apparent()
    return s.separation_from(v).degrees

elongation_at.step_days = 15.0

times, elongations = find_maxima(t0, t1, elongation_at)

for t, elongation_degrees in zip(times, elongations):
    e = earth.at(t)
    _, slon, _ = e.observe(sun).apparent().frame_latlon(ecliptic_frame)
    _, vlon, _ = e.observe(venus).apparent().frame_latlon(ecliptic_frame)
    is_east = (vlon.degrees - slon.degrees) % 360.0 < 180.0
    direction = 'east' if is_east else 'west'
    print('{}  {:4.1f}° {} elongation'.format(
        t.utc_strftime(), elongation_degrees, direction))
        