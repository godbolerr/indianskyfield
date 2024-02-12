import numpy as np
from skyfield.api import Angle, load

ts = load.timescale()
time = ts.utc(2020, 12, 30)

eph = load('de421.bsp')
earth, neptune = eph['earth'], eph['neptune barycenter']
radius_km = 24764.0

astrometric = earth.at(time).observe(neptune)
ra, dec, distance = astrometric.apparent().radec()
apparent_diameter = Angle(radians=np.arcsin(radius_km / distance.km) * 2.0)
print('{:.6f} arcseconds'.format(apparent_diameter.arcseconds()))