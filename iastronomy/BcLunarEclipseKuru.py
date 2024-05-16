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
from datetime import datetime, timedelta
from wx.lib.ogl.composit import _objectStartY

# –13200 to 17191

ts = api.load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

startYear = -5010
endYear = -5000


csvFile = open(f"LunarEclipse{ startYear }_{endYear}.csv", "w") 
counter = 0
print(f"Processing {csvFile.name}")
prevNewMoon = 0;
for curYear in range(startYear, endYear, 1):
    
    nextYear = curYear - 1
     
    #print(" Processing from ", curYear , nextYear)
    t0 = ts.utc(nextYear, 1, 1)
    t1 = ts.utc(curYear, 12, 31)
    diff = 0
    t, y, details = eclipselib.lunar_eclipses(t0, t1, eph)
    
    for (eventTime , yi ) in zip(t,y) :

        year, month, day, hour, minute, second = eventTime.tt_calendar() 
        
        istTime = ts.utc(year, month, day, hour, minute, second) + timedelta(hours=5,minutes=30)
        

  
        mlat, mlon, distance = earth.at(eventTime).observe(moon).frame_latlon(ecliptic_frame)
        slat, slon, distance = earth.at(eventTime).observe(sun).frame_latlon(ecliptic_frame)
     
        counter = counter + 1
        
  
        print(counter,year, month, day, hour, minute, int(second), diff, eventTime.tt, slon.dms() , mlon.dms(),  slat.dms(),mlat.dms(),  eclipselib.LUNAR_ECLIPSES[yi], sep="," )#, file=csvFile)
        
        
csvFile.close() 