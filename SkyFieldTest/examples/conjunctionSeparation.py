from skyfield.api import load
from skyfield.framelib import ecliptic_frame

ts = load.timescale()
eph = load('de421.bsp')
sun, mars,earth = eph['sun'], eph['mars'], eph['earth']

t = ts.utc(2019, 9, 2, 10, 42, 26)
e = earth.at(t)
s = e.observe(sun).apparent()
m = e.observe(mars).apparent()
print('{:.5f}°'.format(m.separation_from(s).degrees))
print('     Latitude Longitude')

lat, lon, distance = s.frame_latlon(ecliptic_frame)
print('Sun  {:.5f}° {:.5f}°'.format(lat.degrees, lon.degrees))

lat, lon, distance = m.frame_latlon(ecliptic_frame)
print('Mars {:.5f}° {:.5f}°'.format(lat.degrees, lon.degrees))

t = ts.utc(2020, 10, 13, 23, 25, 55)

e = earth.at(t)
s = e.observe(sun).apparent()
m = e.observe(mars).apparent()

print('Separation: {:.5f}°'.format(m.separation_from(s).degrees))

print('')
print('     Latitude Longitude')

lat, lon, distance = s.frame_latlon(ecliptic_frame)
print('Sun  {:.5f}° {:.5f}°'.format(lat.degrees, lon.degrees))

lat, lon, distance = m.frame_latlon(ecliptic_frame)
print('Mars {:.5f}° {:.5f}°'.format(lat.degrees, lon.degrees))
