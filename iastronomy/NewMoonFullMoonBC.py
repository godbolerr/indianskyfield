from datetime import timedelta

from pytz import timezone
import pytz  
from skyfield import almanac
from skyfield import api
from skyfield import eclipselib
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.framelib import ecliptic_frame
from skyfield.toposlib import Topos
from wx.lib.ogl.composit import _objectStartY


# –13200 to 17191
ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
kuruKshetra = wgs84.latlon(29.9695 * N, 76.8783 * E)
kuruKshetraObserver = eph['Earth'] + kuruKshetra


startYear = 2024
endYear = 2026
phaseValue = 2  # 0 is new moon , 2 is full moon 

csvFile = open(f"MoonPhase_{ startYear }_{endYear}_{phaseValue}.csv", "w") 
counter = 0
print(f"Processing {csvFile.name}")
prevNewMoon = 0;

for curYear in range(startYear, endYear, 1):
    print(" Processing from ", curYear)
    t0 = ts.utc(curYear, 1, 1)
    t1 = ts.utc(curYear, 12, 31)
    diff = 0

    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
       
    
    for (eventTime , phases ) in zip(t,y) :
            if (phases == phaseValue ) :
                
                year, month, day, hour, minute, second = eventTime.tt_calendar()
                
                # For the day when this event has occurred.
                
                tt1 = api.load.timescale().utc(year, month, day)
                
                tt2 = tt1 + timedelta(days=1)
                
                tr, yr = almanac.find_risings(kuruKshetraObserver, sun, tt1, tt2)
                ts, ys = almanac.find_settings(kuruKshetraObserver, sun, tt1, tt2)
                
                if  ( prevNewMoon == 0 ):
                    prevNewMoon = eventTime.tt
                else :
                    curNewMoon = eventTime.tt
                    diff = curNewMoon - prevNewMoon
                    prevNewMoon = curNewMoon
                 
                mlat, mlon, distance = earth.at(eventTime).observe(moon).frame_latlon(ecliptic_frame)
                slat, slon, distance = earth.at(eventTime).observe(sun).frame_latlon(ecliptic_frame)
                
                slonstr = str(slon.dms()).replace('(','').replace(')','')
                mlonstr = str(mlon.dms()).replace('(','').replace(')','')
                slatstr = str(slat.dms()).replace('(','').replace(')','')
                mlatstr = str(mlat.dms()).replace('(','').replace(')','')  
                
                dt = eventTime.astimezone(pytz.timezone("Asia/Kolkata"))
                surniseTimeDt = tr.astimezone(pytz.timezone("Asia/Kolkata"))
                sunsetTimeDt = ts.astimezone(pytz.timezone("Asia/Kolkata"))
                
               # print(dt , surniseTimeDt , sunsetTimeDt )
                counter = counter + 1
                
                # Check the possibility of eclipse on that day visible from Kurukshetra
                # Ideally it should be after sunset and before sunrise.
                eclipseFlag = "E_N"
                
                if ( phaseValue == 2 and (dt.hour > 18 or dt.hour < 6 )  ):
                    eclipseFlag = "LE_Y"
                    
                if ( phaseValue == 0 and dt.hour > 6 and dt.hour < 18 ):
                    eclipseFlag = "SE_Y"            
                  
                print(counter,dt,surniseTimeDt[0].hour, surniseTimeDt[0].minute,sunsetTimeDt[0].hour, sunsetTimeDt[0].minute, eclipseFlag, dt.year, dt.month, dt.day, dt.hour, dt.minute, int(dt.second), diff, eventTime.tt, slonstr , mlonstr,  slatstr,mlatstr,  sep=",", file=csvFile)
csvFile.close() 