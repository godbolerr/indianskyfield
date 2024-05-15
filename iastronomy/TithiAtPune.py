from datetime import datetime 
from datetime import timedelta
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
import csv




# –13200 to 17191
# #################### Constants ########################
ts = api.load.timescale()
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
pune = wgs84.latlon(18.5204 * N, 73.8567 * E)
puneObserver = eph['Earth'] + pune

startDay = 1
startMonth = 1 
startYear = 2024
lunarMonths = 13

from_dms = lambda degs, mins, secs: degs + mins / 60 + secs / 3600


def cleaupString(slon):
    return str(slon.dms()).replace('(', '').replace(')', '')

def findSunRise(refDate,observer,observerTimeZone):
    
    midnight = refDate.replace(tzinfo=observerTimeZone)
    next_midnight = midnight + datetime.timedelta(days=1)

    t0 = ts.from_datetime(midnight)
    t1 = ts.from_datetime(next_midnight)

    st, _ = almanac.find_risings(observer, sun, t0, t1)

    return st[0]

def tithiNow(refDate) :
    
    mlat, mlon, _ = earth.at(refDate).observe(moon).frame_latlon(ecliptic_frame)
    slat, slon, _ = earth.at(refDate).observe(sun).frame_latlon(ecliptic_frame)        
    lonDiff = mlon.degrees - slon.degrees 
    if (lonDiff < 0) :
        lonDiff = lonDiff + 360
        
    tithiSeq = int(lonDiff / 12 ) # Assume that tithin never finishes exactly at sunrise
    tithiSeq = tithiSeq + 1
      
    targetLon = 12 * tithiSeq  
    
    tithiEndDate = refDate
  
    paksha = "S"
    while(lonDiff < targetLon):
        tithiEndDate = tithiEndDate + datetime.timedelta(seconds=30)
        mlat, mlon, _ = earth.at(tithiEndDate).observe(moon).frame_latlon(ecliptic_frame)
        slat, slon, _ = earth.at(tithiEndDate).observe(sun).frame_latlon(ecliptic_frame)        
        lonDiff = mlon.degrees - slon.degrees 

        if (lonDiff < 0):
            lonDiff = lonDiff + 360
            
        if (lonDiff > 359.99):
            break         
        
        if ( tithiSeq > 15 ) :
            tithi = tithiSeq - 15
            paksha = "K"
        else :
            tithi = tithiSeq
        
#    print(lonDiff, tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon)
    
    return lonDiff, tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon
    
fields = ['seq','istDate', 'tithiSeq', 'paksha' , 'tithiNumber', 'tithiDuration','year','month','day','hour','minute','second','phaseAngle']

df = pd.read_csv('RawTithi_10_12_2023_15.csv' ,skipinitialspace=True, usecols=fields)

# Read the start date
# It is assumed to be Pratipada end time.

curIndex = 0 
curDate = 0

#Decide start gregorian date 

tithiDate = ts.utc(df.year[curIndex], df.month[curIndex], df.day[curIndex], df.hour[curIndex], df.minute[curIndex], df.second[curIndex])

curTithiDate = tithiDate.astimezone(istZone)

currentDate = datetime.datetime(2024,3,1,0,0,0)

sunrise = findSunRise(currentDate, puneObserver, istZone)

seq = 0
lonDiffFlag = 0 

for row in range(1,100,1) :
    seq = seq+1
    sunrise = findSunRise(currentDate, puneObserver, istZone)
    sunriseLocal = sunrise.astimezone(istZone)
    lonDiff, tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon = tithiNow(sunrise)
    
    if ( lonDiffFlag == 0 ) :
        lonDiffFlag = lonDiff

    if ( lonDiff - lonDiffFlag  > 12 ) :
        print("Kshay tithi detected : " , sunriseLocal )
    
    lonDiffFlag = lonDiff
            
    tithiEndLocal = tithiEndDate.astimezone(istZone)
    print(seq,tithiSeq,paksha,tithi,lonDiff,lonDiffFlag,sunriseLocal,tithiEndLocal)
        
    currentDate += datetime.timedelta(days=1)

