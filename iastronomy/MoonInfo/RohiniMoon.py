from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime
from skyfield.api import Star, load
from skyfield.data import hipparcos


ts = api.load.timescale()
ist = timezone('Asia/Kolkata')

eph = load('../de431t.bsp')
sun = eph['sun']

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

equatorLocation = wgs84.latlon(0 * N, 73.8567 * E)

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

puneObserver = earth + puneLatLon 

equatorObserver = eph['Earth'] + equatorLocation

observer = puneObserver

ist = timezone('Asia/Kolkata')

def checkDec(value):
    if 0.20 <= value <= 0.3 :
        return True
    return False

def checkRaRohini(value):
    if 68.5 <= value <= 69.5 :
        return True
    return False

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

# HIP for Aldebaran  21421

aldebarnHip = 21421

aldebaranStar = Star.from_dataframe(df.loc[aldebarnHip])

t0 = ts.utc(2000, 1, 1,0,0,0)

ra,dec,distance = observer.at(t0).observe(aldebaranStar).apparent().radec()

rohiniRa = ra.degrees
rohiniDec = dec.degrees

print(ra.degrees,dec.degrees,sep=",")

totalIterations = 1000000
counter=0


for row in range(1,totalIterations,1) :
    
    t1 = t0 + datetime.timedelta(seconds=600)
    
    raMoon,decMoon,distance = observer.at(t1).observe(moon).apparent().radec()
    
    if ( checkDec( rohiniDec - decMoon.degrees ) and checkRaRohini(raMoon.degrees)) :
    
        print(raMoon.degrees,decMoon.degrees,sep=",")
    
    t0 = t1







