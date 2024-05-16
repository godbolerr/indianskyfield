#https://stackoverflow.com/questions/76559899/calculate-the-crescent-moon-width-using-skyfield

from skyfield.api import wgs84, load
from math import degrees, cos, asin, floor

ts = load.timescale()
eph = load('de421.bsp')

sun, earth, moon = eph['sun'], eph['earth'], eph['moon']

time = ts.tt(2023, 6, 1, 21, 30)  # June 1st 2023 9:30pm

# the location of the observer i.e. Hyde Park, London
observer = earth + wgs84.latlon(
    51.51, -0.165, 30)  #latitude, longitude, elevation 

# calculate the topocentric position of the sun and the moon
sun_topocentric = observer.at(time).observe(sun).apparent()
moon_topocentric = observer.at(time).observe(moon).apparent()

# calculate elongation from topocentric position of the sun relative to the moon
elongation = sun_topocentric.separation_from(moon_topocentric)

# calculate the geocentric position of the moon from the earth
difference = moon.at(time) - earth.at(time)
# retrieve the distance is km
moon_to_earth_km = difference.distance().km


moon_radius_km = 1737.1
moon_radius_degrees = degrees(asin(moon_radius_km / moon_to_earth_km))

crescent_width_degrees = moon_radius_degrees * (1 - (cos(elongation.radians)))

print(crescent_width_degrees)