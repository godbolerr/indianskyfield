from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.toposlib import Topos
from skyfield import eclipselib
import datetime
from skyfield.framelib import ecliptic_frame

#Find out date of full moon from Start 0AD


eph = load('../de431t.bsp')

istTz = timezone('Asia/Kolkata')

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon

ts = load.timescale();

sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

for curYear in range(2000, 2010, 1):
    
    nextYear = curYear + 1
    
    t0 = ts.utc(curYear, 1, 1)
    
    t1 = ts.utc(nextYear, 12, 31)
    
    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))

    for (eventTime , phases ) in zip(t,y) :
            if (phases == 0 or phases == 2 ) :
                year, month, day, hour, minute, second = eventTime.tt_calendar()
                dayOfWeek = datetime.datetime(year, month, day).weekday()
                mlat, mlon, distance = earth.at(eventTime).observe(moon).frame_latlon(ecliptic_frame)
                slat, slon, distance = earth.at(eventTime).observe(sun).frame_latlon(ecliptic_frame)                
                
                
                
                print(phases,eventTime.tt, slon.dms() , mlon.dms(),  slat.dms(),mlat.dms(),dayOfWeek,eventTime.tai,eventTime.utc_strftime('%Y-%m-%d %H:%M'), year, month, day, hour, minute, int(second))
