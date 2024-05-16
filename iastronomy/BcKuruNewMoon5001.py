from pytz import timezone
import pytz  
from skyfield import almanac
from skyfield import api
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.toposlib import Topos
from skyfield import eclipselib
from datetime import timedelta
from skyfield.framelib import ecliptic_frame
import datetime
from datetime import datetime 

# –13200 to 17191

ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

csvFile = open("NewMoon1600_1700.csv", "w") 
counter = 0

prevNewMoon = 0;
for curYear in range(1600, 2600, 1):
    
    nextYear = curYear + 1
     
    #print(" Processing from ", curYear , nextYear)
    t0 = ts.utc(curYear, 1, 1)
    t1 = ts.utc(nextYear, 12, 31)
    diff = 0
    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
    
    for (eventTime , phases ) in zip(t,y) :
            if (phases == 2 ) :
                year, month, day, hour, minute, second = eventTime.tt_calendar()
                
                if  ( prevNewMoon == 0 ):
                    prevNewMoon = eventTime.tt
                else :
                    curNewMoon = eventTime.tt
                    diff = curNewMoon - prevNewMoon
                    prevNewMoon = curNewMoon
                 
                mlat, mlon, distance = earth.at(eventTime).observe(moon).frame_latlon(ecliptic_frame)
                slat, slon, distance = earth.at(eventTime).observe(sun).frame_latlon(ecliptic_frame)
                print(year)
                counter = counter + 1
                print(counter,year, month, day, hour, minute, int(second), diff, eventTime.tt, slon.dms() , mlon.dms(),  slat.dms(),mlat.dms(),  sep=",", file=csvFile)
csvFile.close() 