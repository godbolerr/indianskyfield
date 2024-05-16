from datetime import datetime 
from datetime import timedelta
import datetime
import datetime

from pytz import timezone
import pytz  
from skyfield import almanac
from skyfield import api
from skyfield import eclipselib
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.framelib import ecliptic_frame
from skyfield.toposlib import Topos
from skyfield.trigonometry import position_angle_of
from wx.lib.ogl.composit import _objectStartY

import datetime as dt
import numpy as np
import pandas as pd


# –13200 to 17191
# #################### Constants ########################
ts = api.load.timescale()
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
pune = wgs84.latlon(18.5204 * N, 73.8567 * E)
puneObserver = eph['Earth'] + pune

startDay = 10
startMonth = 12 
startYear = 2023
lunarMonths = 15

csvFile = open(f"RawTithi_{ startDay }_{startMonth}_{startYear}_{lunarMonths}.csv", "w") 

from_dms = lambda degs, mins, secs: degs + mins / 60 + secs / 3600

# Python Program to Convert seconds
# into hours, minutes and seconds

def convert(seconds):
    hour = int(seconds/3600) 
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)
    

def cleaupString(slon):
    return str(slon.dms()).replace('(', '').replace(')', '')

def findSunRise(refDate,observer):
    
    startday = refDate.utc_datetime()
    
    midnight = startday.replace(hour=0, minute=0, second=0, microsecond=0)
    next_midnight = midnight + datetime.timedelta(days=1)

    t0 = ts.from_datetime(midnight)
    t1 = ts.from_datetime(next_midnight)

    st, _ = almanac.find_risings(observer, sun, t0, t1)

    return st[0].astimezone(istZone)


def tithiDate(refDate, tithiNo):
    
    nextTithistartMarker = refDate + datetime.timedelta(hours=19)
    degreeDiff = 12 * tithiNo
    lonDiff = 0
    
    while(lonDiff < degreeDiff):
        nextTithistartMarker = nextTithistartMarker + datetime.timedelta(seconds=30)
        mlat, mlon, _ = earth.at(nextTithistartMarker).observe(moon).frame_latlon(ecliptic_frame)
        slat, slon, _ = earth.at(nextTithistartMarker).observe(sun).frame_latlon(ecliptic_frame)        
        lonDiff = mlon.degrees - slon.degrees 
        if (lonDiff < 0):
            lonDiff = lonDiff + 360
        
       # print(tithiNo,nextTithistartMarker.astimezone(istZone) , lonDiff)
        
        if (tithiNo == 30 and lonDiff > 359.99):
            break
 
    return nextTithistartMarker, slat, slon, mlat, mlon, lonDiff
    
# Find next amavasya at Pune from the start date


startDate = ts.utc(startYear, startMonth, startDay, hour=0, minute=0, second=0)
endDate = startDate + dt.timedelta(days=30)

t, y = almanac.find_discrete(startDate, endDate, almanac.moon_phases(eph))

firstNewMoonFlag = 0 
firstNewMoonDate = 0

for (newMoonTime , phases) in zip(t, y): 
    if (phases == 0):
        firstNewMoonFlag = 1
        firstNewMoonDate = newMoonTime
        break
        
if (firstNewMoonFlag == 1):
 
    tithiNumber = 0;
   
    curTithiDate = firstNewMoonDate
    
    seq = 0
    for lunarMonth in range(1, lunarMonths, 1):
    
        for tithiSeq in range(1, 31, 1):
            seq = seq + 1
            nextithiStartDate, slat, slon, mlat, mlon, lonDiff = tithiDate(curTithiDate, tithiSeq)    
            year, month, day, hour, minute, second = nextithiStartDate.tai_calendar()
            tithiDuration = nextithiStartDate.tt - curTithiDate.tt ; 
            paksha = "S"
            if ( tithiSeq > 15 ):
                paksha = "K"
                
            tithiNumber = tithiSeq
                
            if ( tithiSeq > 15 ):
                tithiNumber = tithiSeq - 15
                          
            tithiTotalSeconds = tithiDuration * 24 * 3600
      
            tithiDuration = convert(tithiTotalSeconds)
            
            istDate = nextithiStartDate.astimezone(istZone)
                                                                
            print(seq, istDate , tithiSeq, paksha, tithiNumber, year, month, day, hour, minute, second ,  tithiDuration,tithiTotalSeconds,  cleaupString(slat), cleaupString(slon), cleaupString(mlat), cleaupString(mlon), lonDiff , sep="," , file=csvFile)
            print(year, month, day)
            curTithiDate = nextithiStartDate
            
       
csvFile.close()     
