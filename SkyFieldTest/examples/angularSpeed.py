from numpy import cos, sqrt
from skyfield.api import load, wgs84, N,S,E,W

ts = load.timescale()
t = ts.utc(2021, 2, 3, 0, 0)
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']
topos = wgs84.latlon(35.1844 * N, 111.6535 * W, elevation_m=2099.5)

a = (earth + topos).at(t).observe(mars).apparent()

(alt, az, distance,
 alt_rate, az_rate, range_rate) = a.frame_latlon_and_rates(topos)


ralt = alt_rate.degrees.per_minute
raz = az_rate.degrees.per_minute * cos(alt.radians)

degrees_per_minute = sqrt(ralt*ralt + raz*raz)
print('{:.4f}° per minute'.format(degrees_per_minute))