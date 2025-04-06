from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime
from skyfield.api import Star, load
from skyfield.data import hipparcos



ts = api.load.timescale()
ist = timezone('Asia/Kolkata')

eph = load('de431t.bsp')
sun = eph['sun']

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon 

ist = timezone('Asia/Kolkata')

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

# HIP for Sirius 32349

siriusStar = Star.from_dataframe(df.loc[32349])

csvFile="SiriusSettingAzimuth.csv"

t0 = ts.utc(2000, 1, 1,0,0,0)

for curYear in range(1, 365, 1):
   
    t1 = t0 + datetime.timedelta(hours=24)
    
    t, y = almanac.find_settings(puneObserver, siriusStar, t0, t1)
    
    alt, az, dist = puneObserver.at(t).observe(siriusStar).apparent().altaz()
    
    punetime = t[0].astimezone(ist).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    azdegrees = '{:.4f}'.format( az.degrees[0])
    
    print(punetime,azdegrees,sep=",")

    t0=t1