from skyfield.api import N, W, wgs84, load
from skyfield import almanac
from skyfield.functions import length_of

ts = load.timescale()
t = ts.utc(2019, 1, 1)

bierstadt = wgs84.latlon(39.5828 * N, 105.6686 * W, elevation_m=4287.012)
m1 = length_of(bierstadt.at(t).position.m)
print(int(m1))

accra = wgs84.latlon(5.6037 * N, 0.1870 * W, elevation_m=61)
m2 = length_of(accra.at(t).position.m)
print(int(m2))

assert m2 > m1
print("I was", int(m2 - m1), "meters farther from the Earth's center\n"
      "when I visited Accra, at nearly sea level, than atop\n"
      "Mt. Bierstadt in Colorado.")