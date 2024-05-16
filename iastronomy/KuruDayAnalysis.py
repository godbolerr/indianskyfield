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
from wx.lib.ogl.composit import _objectStartY
import pandas as pd
import numpy as np

# –13200 to 17191
# #################### Constants ########################

ts = api.load.timescale()
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)
kuruKshetraObserver = eph['Earth'] + kuruKshetra

result = np.datetime64('now')

print(result)

# create a datetime64 object
dt64 = np.datetime64('-6-09-23T23:49:08')

print(dt64)



# ################## Change start year ##################

startYear = 2000
endYear = 2020
moonPhase = 0
#csvFile = open(f"NewMoon{ startYear }_{endYear}_{moonPhase}.csv", "w") 
counter = 0
#print(f"Processing {csvFile.name}")
prevNewMoon = 0;


def kuruTimeValue(skyfieldTime):

    year, month, day, hour, minute, second = skyfieldTime.tai_calendar() 

    second = int(second)
    
    monthstr = month
    dayString = day
    hourString = hour
    minuteString  = minute
    secString = second

    if ( month < 10 ):
        monthstr = f"0{month}"   
    
    if ( day < 10 ):
        dayString = f"0{day}"
    
    if ( hour < 10):
        hourString = f"0{hour}"   
        
       
    if ( minute < 10):
        minuteString = f"0{minute}"   
        
    if ( second < 10):
        secString = f"0{second}"                         
            
    dateString = f"{year}-{monthstr}-{dayString}T{hourString}:{minuteString}:{secString}"
    
    dateString = dateString.replace("[","").replace("]", "")

    # create a datetime64 object
    dt64 = np.datetime64(dateString)
    
    dt64 = dt64 + np.timedelta64(5,'h') + np.timedelta64(30,'m')
 
    kyear = np.datetime64(dt64,'Y')
    kmonth = np.datetime64(dt64,'M')
    kday = np.datetime64(dt64,'D')
    khour = np.datetime64(dt64,'h')
    kminute = np.datetime64(dt64,'m')
    ksecond = np.datetime64(dt64,'s')
    
    kmonth = str(kmonth)[-2:]
    kday = str(kday)[-2:]
    khour = str(khour)[-2:]
    kminute = str(kminute)[-2:]
    ksecond = str(ksecond)[-2:]
    
    #print(kyear,kmonth,kday,khour,kminute,ksecond)
    
    return (dt64 , kyear,kmonth,kday,khour,kminute,ksecond)


for curYear in range(startYear, endYear, 1):
    
    print(" Processing  ", curYear)
    t0 = ts.utc(curYear, 1, 1)
    t1 = ts.utc(curYear, 12, 31)
    diff = 0
    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
    
    for (newMoonTime , phases ) in zip(t,y) :
           if (phases == moonPhase) :
                year, month, day, hour, minute, second = newMoonTime.tai_calendar() 
              
               
                
             
                tt1 = api.load.timescale().utc(year, month, day)
                tt2 = tt1 + timedelta(days=1)
                
                tr, yr = almanac.find_risings(kuruKshetraObserver, sun, tt1, tt2)
                tss, ys = almanac.find_settings(kuruKshetraObserver, sun, tt1, tt2)
                
                if  ( prevNewMoon == 0 ):
                    prevNewMoon = newMoonTime.tt
                else :
                    curNewMoon = newMoonTime.tt
                    diff = curNewMoon - prevNewMoon
                    prevNewMoon = curNewMoon
                 
                mlat, mlon, distance = earth.at(newMoonTime).observe(moon).frame_latlon(ecliptic_frame)
                slat, slon, distance = earth.at(newMoonTime).observe(sun).frame_latlon(ecliptic_frame)
                 
                slonstr = str(slon.dms()).replace('(','').replace(')','')
                mlonstr = str(mlon.dms()).replace('(','').replace(')','')
                slatstr = str(slat.dms()).replace('(','').replace(')','')
                mlatstr = str(mlat.dms()).replace('(','').replace(')','')  
                
                mdeg,mmin,msec = mlatstr.split(",")
                
                dt64newMoon,kyear,kmonth,kday,khour,kminute,ksecond = kuruTimeValue(newMoonTime)
                
 #               dt = newMoonTime.astimezone(pytz.timezone("Asia/Kolkata"))
                #surniseTimeDt = tr.astimezone(pytz.timezone("Asia/Kolkata"))
#                sunsetTimeDt = tss.astimezone(pytz.timezone("Asia/Kolkata"))
                
               # print(dt , surniseTimeDt , sunsetTimeDt )
                counter = counter + 1
                
                # Check the possibility of eclipse on that day visible from Kurukshetra
                # Ideally it should be after sunset and before sunrise.
                eclipseFlag = "E_N"
                
                #if ( phases == 2 and (dt.hour > 18 or dt.hour < 6 )  ):
                #    eclipseFlag = "LE_Y"
                    #print(counter,dt,surniseTimeDt[0].hour, surniseTimeDt[0].minute,sunsetTimeDt[0].hour, sunsetTimeDt[0].minute, eclipseFlag, dt.year, dt.month, dt.day, dt.hour, dt.minute, int(dt.second), diff, newMoonTime.tt, slonstr , mlonstr,  slatstr,mlatstr,  sep="," , file=csvFile)
   
                if ( mdeg == '0.0' or  mdeg == '-0.0' ):        
                    if ( phases == 0 and int(khour) > 6 and int(khour) < 18 ) :
                        eclipseFlag = "SE_Y"            
               
               
                print(counter,eclipseFlag,year,month, day, khour,kminute, int(second), diff, newMoonTime.tt, slonstr , mlonstr,  slatstr,mlatstr,  sep="," )#, file=csvFile)
#csvFile.close()                               
                
                
                
                
                
                
                
                
                                 
  