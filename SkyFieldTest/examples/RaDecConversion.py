from skyfield import api

ts = api.load.timescale()
t = ts.utc(2019, 9, 13, 20)
geographic = api.wgs84.latlon(latitude_degrees=42, longitude_degrees=-87)
observer = geographic.at(t)
pos = observer.from_altaz(alt_degrees=90, az_degrees=0)

ra, dec, distance = pos.radec()
print(ra)
print(dec)