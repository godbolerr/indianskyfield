from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime as dt
import sqlite3
from numpy._core._multiarray_umath import integer



ts = api.load.timescale()
ist = timezone('Asia/Kolkata')

eph = load('de431t.bsp')
sun = eph['sun']

puneLatLon = wgs84.latlon(18.5204 * N, 73.8567 * E)

puneObserver = eph['Earth'] + puneLatLon

ist = timezone('Asia/Kolkata')


conn = sqlite3.connect('puneTithi.db')

cur = conn.cursor()

cur.execute("select tyear,tmonth,tday,thour,tminute,tsecond from tithi where tithiId = 4 and paksha = 'S'")

results = cur.fetchall()  
  
if results:
    for result in results:
        
        year = result[0]
        month = result[1]
        day = result[2]
        hour = result[3]
        minute = result[4]
        seconds = result[5]
         
        stellaDate = """{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}""".format(year,month,day,hour,minute,int(seconds))
 
        t = ts.utc(year, month, day) #+  timedelta(hours=5,minutes=30)
        next_midnight = t + dt.timedelta(days=1)
        
      
        
        tset, y = almanac.find_settings(puneObserver, sun, t, next_midnight)
 
        sunsetpuneIst = tset.astimezone(ist)
        
        

        year = sunsetpuneIst[0].year
        month = sunsetpuneIst[0].month
        day = sunsetpuneIst[0].day
        hour = sunsetpuneIst[0].hour
        minute = sunsetpuneIst[0].minute
        seconds = sunsetpuneIst[0].second
        
       
        sunsetDate = """{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}""".format(year,month,day,hour,minute,int(seconds))
 
  
        #print(stellaDate, sunsetDate )
        
        print("\"",sunsetDate ,"\",")
            
            
            