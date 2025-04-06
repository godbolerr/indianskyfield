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

# –13200 to 17191
ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
pune = wgs84.latlon(18.5204 * N, 73.8567 * E)
puneObserver = eph['Earth'] + pune
observer = puneObserver

startYear = 2025
endYear = 2026
phaseValue = 0  # 0 is new moon , 2 is full moon 

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
                
                tr, yr = almanac.find_risings(observer, sun, tt1, tt2)
                ts, ys = almanac.find_settings(observer, sun, tt1, tt2)
                
                if  ( prevNewMoon == 0 ):
                    prevNewMoon = eventTime.tt
                else :
                    curNewMoon = eventTime.tt
                    diff = curNewMoon - prevNewMoon
                    prevNewMoon = curNewMoon
                                
                dt = eventTime.astimezone(pytz.timezone("Asia/Kolkata"))
                surniseTimeDt = tr.astimezone(pytz.timezone("Asia/Kolkata"))
                sunsetTimeDt = ts.astimezone(pytz.timezone("Asia/Kolkata"))
                
               # print(dt , surniseTimeDt , sunsetTimeDt )
                counter = counter + 1
               
                
                
                stellaDate = """{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}""".format(sunsetTimeDt[0].year,sunsetTimeDt[0].month,sunsetTimeDt[0].day,sunsetTimeDt[0].hour,sunsetTimeDt[0].minute,sunsetTimeDt[0].second)
            
                print(counter,dt,stellaDate,dt.year, dt.month, dt.day, dt.hour, dt.minute, int(dt.second), diff, eventTime.tt, sep=",", file=csvFile)
csvFile.close() 