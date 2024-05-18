from datetime import timedelta

from pytz import timezone
import pytz  
from skyfield import almanac
from skyfield import api
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.toposlib import Topos
from skyfield.framelib import ecliptic_frame
import datetime


# –13200 to 17191
ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('../de431t.bsp')
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START


sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)
kuruKshetraObserver = eph['Earth'] + kuruKshetra


startYear = -5000
endYear = 2000


csvFile = open("Kuru5000BC_2000AD_J.csv", "w") 

def cleaupString(slon):
    return str(slon.dms()).replace('(', '').replace(')', '')

def findSunRise(year,month,day,observer):
    
    
    midnight = ts.utc(year, month, day, 0, 0, 0)
    next_midnight = midnight + datetime.timedelta(days=1)

    st, _ = almanac.find_risings(observer, sun, midnight, next_midnight)

    return st[0]

def findSunset(year,month,day,observer):
    
   
    
    midnight = ts.utc(year, month, day, hour, minute, second)
    next_midnight = midnight + datetime.timedelta(days=1)


    st, _ = almanac.find_settings(observer, sun, midnight, next_midnight)

    return st[0]



seq = 0
for curYear in range(startYear, endYear, 1):
    
    t0 = ts.utc(curYear, 1, 1)
    t1 = ts.utc(curYear, 12, 31)


    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
       
    for (eventTime , phases ) in zip(t,y) :
        
            # 0 indicates Amavasya or new moon
        
            if (phases == 0 ) :
                
            
                year, month, day, hour, minute, second = eventTime.tt_calendar()
                
                newMoontime = ts.utc(year, month, day, hour, minute, second)
                
                #Move to IST only for reporting purpose as astimezone does not work on BC Dates
                
                kuruDateTime = newMoontime + datetime.timedelta(hours=5,minutes=30)
                
                #print(newMoontime.utc_jpl())
                e = kuruKshetraObserver.at(newMoontime)
                s = e.observe(sun)
                m = e.observe(moon)
                seperation = s.separation_from(m).degrees
                
                if ( seperation < 0.5 and ( hour > 2 and hour < 11) ) :
                    seq = seq + 1
                    print(seq,year)
                      
                    #Both dates are reported for vefirification with other data sources
                    
                    print(seq,newMoontime.utc_iso(), kuruDateTime.utc_iso(), newMoontime.tt , year, month, day, hour, minute, second, seperation, sep="," ,file=csvFile)
                 