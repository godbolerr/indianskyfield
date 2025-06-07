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

eph = load('../de431t.bsp')
np.set_printoptions(legacy='1.25')
istTz = timezone('Asia/Kolkata')
oneMonthMoon = open(f"Jan2000_moon.csv", "w") 

def rahuNodes(starYear,endYear):

    print("calculation of lunar nodes")
    rahuNodeFile = open(f"rahuNodeSunMoon01_2000_01_2025.csv", "w") 
    t0 = ts.utc(starYear, 1, 1)
    t1 = ts.utc(endYear, 1, 1)
    
    t, y = almanac.find_discrete(t0, t1, almanac.moon_nodes(eph))
    count = 0
    for (nodeTime , nodeValue) in zip(t,y) :
        if ( nodeValue == 1 ):
            count = count +1 
            year, month, day, hour, minute, second = nodeTime.tt_calendar()
            mlat, mlon, distance = earth.at(nodeTime).observe(moon).frame_latlon(ecliptic_frame)
            slat, slon, distance = earth.at(nodeTime).observe(sun).frame_latlon(ecliptic_frame)    
            print("{0}-{1}-{2}".format(year,month,day),nodeTime.utc_iso(),nodeValue,slon.degrees,mlon.degrees,sep=",",file=rahuNodeFile)
    
    print("calculation of lunar nodes over : " , count )

def moonOneMonth():
    for dayCount in range(1, 32, 1):
        
        t0 = ts.utc(2000, 1, dayCount)
        year, month, day, hour, minute, second = t0.tt_calendar()
        mlat, mlon, distance = earth.at(t0).observe(moon).frame_latlon(ecliptic_frame)
        slat, slon, distance = earth.at(t0).observe(sun).frame_latlon(ecliptic_frame)     
        print(year, month, day, hour, minute, int(second),slon.degrees , mlon.degrees,  mlat.degrees,sep=",", file=oneMonthMoon)
   
#Find out date of full moon from Start 0AD


puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon

ts = load.timescale();

sun,earth,moon, jupiter  = eph['sun'] ,  eph['earth'], eph['moon'],eph['JUPITER BARYCENTER']

t0 = ts.utc(2001, 1, 1)

curLong = 0

for curYear in range(1, 1000 , 1):
    
    t1 = t0 + datetime.timedelta(days=30)

    year, month, day, hour, minute, second = t1.tt_calendar()
    jlat, jlon, distance = earth.at(t1).observe(jupiter).frame_latlon(ecliptic_frame)
    slat, slon, distance = earth.at(t1).observe(sun).frame_latlon(ecliptic_frame)     
    
    if ( curLong == 0 ):
        curLong = jlon.degrees
        prevLong = jlon.degrees
    
    diffLong =  jlon.degrees - prevLong
    print(year, month, day, hour, minute, int(second),slon.degrees , jlon.degrees, diffLong, jlat.degrees,sep=",")
    t0 = t1
    prevLong = jlon.degrees
    