from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.toposlib import Topos
from skyfield import eclipselib
import datetime
from skyfield.framelib import ecliptic_frame
import numpy as np
from skyfield.positionlib import Astrometric






from_dms = lambda degs, mins, secs: degs + mins / 60 + secs / 3600

def convert(seconds):
    hour = int(seconds/3600) 
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def cleaupString(slon):
    return str(slon.dms()).replace('(', '').replace(')', '')

def getDms(slon):
    newStr=  str(slon.dms()).replace('(', '').replace(')', '')
    dmsarray =  newStr.split(',')

    return dmsarray[0],dmsarray[1],dmsarray[2]




#Find out date of full moon from Start 0AD


eph = load('../de431t.bsp')
np.set_printoptions(legacy='1.25')


istTz = timezone('Asia/Kolkata')

rahuNodeFile = open(f"rahuNode2000_2025.csv", "w") 

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon

ts = load.timescale();

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']


print("calculation of lunar nodes")

t0 = ts.utc(2000, 1, 1)

t1 = ts.utc(2025, 12, 31)

t, y = almanac.find_discrete(t0, t1, almanac.moon_nodes(eph))

for (nodeTime , nodeValue) in zip(t,y) :
    if ( nodeValue == 1 ):
        mlat, mlon, distance = earth.at(nodeTime).observe(moon).frame_latlon(ecliptic_frame)
        print(nodeTime.utc_iso(),nodeValue,mlon.degrees,sep=",",file=rahuNodeFile)

print("calculation of lunar nodes over")


