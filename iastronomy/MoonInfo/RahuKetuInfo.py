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

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon

ts = load.timescale();

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

for curYear in range(2000, 2002, 1):
    
    nextYear = curYear + 1
    
    t0 = ts.utc(curYear, 1, 1)
    
    t1 = ts.utc(nextYear, 12, 31)
    
    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
    
    # compute only for new moons
    
    for (eventTime , phases) in zip(t,y) :
            if (phases == 0 ) :
                year, month, day, hour, minute, second = eventTime.tt_calendar()
                dayOfWeek = datetime.datetime(year, month, day).weekday()
               
                mlat, mlon, distance = earth.at(eventTime).observe(moon).frame_latlon(ecliptic_frame)
                slat, slon, distance = earth.at(eventTime).observe(sun).frame_latlon(ecliptic_frame)                                                             
                print(eventTime.utc_iso(), mlon.degrees,  slon.degrees,sep=",")

    
    # Find Longitude of the Rahu from the lunar node data
    
    t, y = almanac.find_discrete(t0, t1, almanac.moon_nodes(eph))
    
    for (nodeTime , nodeValue) in zip(t,y) :
        if ( nodeValue == 1 ):
            mlat, mlon, distance = earth.at(nodeTime).observe(moon).frame_latlon(ecliptic_frame)
            #print(nodeTime.utc_iso(),nodeValue,mlon.degrees,sep=",")

