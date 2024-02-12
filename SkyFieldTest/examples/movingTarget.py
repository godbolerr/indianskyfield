from skyfield.api import load, wgs84, N,S,E,W

ts = load.timescale()
t = ts.utc(2021, 2, 3, 0, 0)
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']
topos = wgs84.latlon(35.1844 * N, 111.6535 * W, elevation_m=2099.5)

a = (earth + topos).at(t).observe(mars).apparent()

(alt, az, distance,
 alt_rate, az_rate, range_rate) = a.frame_latlon_and_rates(topos)

print('Alt: {:+.1f} asec/min'.format(alt_rate.arcseconds.per_minute))
print('Az:  {:+.1f} asec/min'.format(az_rate.arcseconds.per_minute))

print('Range rate: {:+.1f} km/s'.format(range_rate.km_per_s))

