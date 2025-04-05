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
import sqlite3
import datetime as dt
import numpy as np



# –13200 to 17191
# #################### Constants ########################
ts = api.load.timescale()
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']


startDay = 1
startMonth = 1
startYear = 2025
totalTithi = 1000




lat=26.9124
long=75.7873
obsLocation="Jaipur"

lat=30.3752
long=76.7821
obsLocation="Ambala"

lat=18.5204
long=73.8567 
obsLocation="Pune"



conn = sqlite3.connect('puneTithi.db')


pune = wgs84.latlon(lat * N, long * E)
puneObserver = eph['Earth'] + pune

#csvFile = open(f"Tithi{ startDay }_{startMonth}_{startYear}_{totalTithi}_{obsLocation}_{lat}_{long}.csv", "a") 

from_dms = lambda degs, mins, secs: degs + mins / 60 + secs / 3600

def convert(seconds):
    hour = int(seconds/3600) 
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def cleaupString(slon):
    return str(slon.dms()).replace('(', '').replace(')', '')

def getDms(slon):
    newStr=  str(slon.dms()).replace('(', '').replace(')', '')
    dmsarray =  newStr.split(',')

    return dmsarray[0],dmsarray[1],dmsarray[2]


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
            
        
        if ( tithiSeq > 15 ) :
            tithi = tithiSeq - 15
            paksha = "K"
        else :
            tithi = tithiSeq
            
        if (lonDiff > 359.99):
            break                 
        
#    print(lonDiff, tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon)


    
    return int(lonDiff), tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon


def insertRow(sqliteConnection,
            seq,
            ktithiSeq,
            kpaksha,
            ktithi,
            ksunriseLocal,
            year,
            month,
            day,
            hour,
            minute,
            second,  
            ktithiEndLocal,     
            flag,
            tyear,
            tmonth,
            tday,
            thour,
            tminute,
            tsecond,   
            timeAfterSunrise,
            tithiDurationSec,
            tithiDurationString,
            kslat, kslon, kmlat, kmlon):

    print("Inserting ", seq , year, month, day, ksunriseLocal,ktithiSeq,ktithiEndLocal)
    ksld,kslm,ksls = getDms(kslat)
    ksod,ksom,ksos = getDms(kslon)    
    kmld,kmlm,kmls = getDms(kmlat)   
    kmod,kmom,kmos = getDms(kmlon)    
    
    
    cursor = sqliteConnection.cursor()

        
    sqlite_insert_with_param = """INSERT INTO tithi
            ( sqid,
              tithiSeq,
              paksha,
              tithiId,            
              sunriseDate,
             
              year,
              month,
              day,
              hour,
              minute,
              
              second,
              tithiDate,
              kshayFlag,
              tyear ,
              tmonth ,
              
              tday ,
              thour ,
              tminute ,
              tsecond,             
              timeFromSunrise ,
              
              duration,
              durationPeriod,
              
              slatd ,
              slatm ,  
              slats ,              
              
              slongd ,
              slongm ,  
              slongs ,
              
              mlatd ,
              mlatm ,
              mlats ,               

              
              mlongd ,
              mlongm ,               
              mlongs 
              
              

              
              ) 
                     VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, 
                             ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, 
                             ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?,?);"""   
    
    
    data_tuple = (
             seq,
             ktithiSeq,
             kpaksha, 
             ktithi,
             ksunriseLocal,
            
                   
            year,
            month,
            day,
            hour,
            minute,
            
            second,  
            ktithiEndLocal,     
            flag,
            tyear,
            tmonth,
            
            tday,
            thour,
            tminute,
            tsecond,   
            timeAfterSunrise,
            
            
            tithiDurationSec,
            tithiDurationString,
            
             ksld,
             kslm,
             ksls,
             
                   
             ksod,
             ksom,
             ksos , 
                
             kmld,
             kmlm,           
             kmls,
             
             kmod,
             kmom,
             kmos  
                
            )
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqliteConnection.commit()
    cursor.close()
    
    return 0
    
def kshyaTithi(refDate,targetLon) :
    
   # print("Target longitude for kshay Tithi " , targetLon)
    mlat, mlon, _ = earth.at(refDate).observe(moon).frame_latlon(ecliptic_frame)
    slat, slon, _ = earth.at(refDate).observe(sun).frame_latlon(ecliptic_frame)        
    lonDiff = mlon.degrees - slon.degrees 
    if (lonDiff < 0) :
        lonDiff = lonDiff + 360
        
    tithiSeq = int(targetLon / 12 ) # Assume that tithin never finishes exactly at sunrise
     
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
    
    return int(lonDiff), tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon
 
 
   
#print("loanDiffRef is " , lonDiffRef)

#Reset if previous day is Amavasya


seq = 0
    
# Get max seq from current table

cur = conn.cursor()
cur.execute("SELECT max(sqid) FROM tithi")

results = cur.fetchall()


if results:
    for result in results:
        print(result[0])
        seq = result[0]


#TODO - Uncomment for the initial Run ONLY then comment back
#seq = 0
    

if ( seq != 1 ) :
            
    cur.execute("SELECT year,month,day FROM tithi where sqid = ? ", (seq,))
    
    results = cur.fetchall()  
      
    if results:
        for result in results:
            print(result)
            startYear = result[0]
            startMonth = result[1]
            startDay = result[2]
            print("Starting with ", startYear,startMonth,startDay , "with start sequencd as " , seq)
        
#Start with the next date 

currentDate = datetime.datetime(startYear,startMonth,startDay,0,0,0) + datetime.timedelta(days=1)
nextDate = currentDate + datetime.timedelta(days=1)

print(nextDate)
sunrise = findSunRise(nextDate, puneObserver, istZone)
lonDiff, tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon = tithiNow(sunrise)

tithiLocal = tithiEndDate.astimezone(istZone)
# Find initial longitude of tithi for comparison

lonDiffRef = int(lonDiff) 

if (lonDiffRef == 360 ) :
    lonDiffRef = 0
    
    

tStartTimeStamp = tithiLocal.timestamp()



for row in range(1,totalTithi,1) :
    seq = seq+1
    sunrise = findSunRise(currentDate, puneObserver, istZone)

    sunriseLocal = sunrise.astimezone(istZone)
    
     
    lonDiff, tithiSeq, paksha, tithi , tithiEndDate, slat, slon, mlat, mlon = tithiNow(sunrise)
    
    ## TODO Detect kshaya tithi at boundary condition, 9 FEB 2024
    
    #print(  lonDiff , lonDiffRef )
    
    if ( lonDiff - lonDiffRef > 12 ) :
        #print("Kshaya tithi detected before ", lonDiff , sunriseLocal)
        kshyaTithiDate = currentDate + datetime.timedelta(days=-1)
        ksunrise = findSunRise(kshyaTithiDate, puneObserver, istZone)
        ksunriseLocal = ksunrise.astimezone(istZone)
        klondiff, ktithiSeq, kpaksha, ktithi , ktithiEndDate, kslat, kslon, kmlat, kmlon = kshyaTithi(ksunrise, (tithiSeq-1)*12 )
        ktithiEndLocal = ktithiEndDate.astimezone(istZone)
        timeAfterSunrise = ktithiEndLocal.timestamp() - ksunriseLocal.timestamp()
        
        tithiDurationSec = ktithiEndLocal.timestamp() - tStartTimeStamp
        
        tStartTimeStamp = ktithiEndLocal.timestamp() 
        
        insertRow(conn,seq,ktithiSeq,kpaksha,ktithi,ksunriseLocal,
           ksunriseLocal.year,
           ksunriseLocal.month,
           ksunriseLocal.day,
           ksunriseLocal.hour,
           ksunriseLocal.minute,
           ksunriseLocal.second,       
           ktithiEndLocal,
           "Y",           
           ktithiEndLocal.year,
           ktithiEndLocal.month,
           ktithiEndLocal.day,
           ktithiEndLocal.hour,
           ktithiEndLocal.minute,
           ktithiEndLocal.second, 
           timeAfterSunrise,
           tithiDurationSec,
           convert(tithiDurationSec),  
           kslat, 
           kslon, 
           kmlat, 
           kmlon )
        seq = seq+1
        
    # Special boundary condition for Kshaya Amvavasay
        
    if ( lonDiffRef - lonDiff == 336 ) :
        #print("Kshaya tithi detected before ", lonDiff , sunriseLocal)
        kshyaTithiDate = currentDate + datetime.timedelta(days=-1)
        ksunrise = findSunRise(kshyaTithiDate, puneObserver, istZone)
        ksunriseLocal = ksunrise.astimezone(istZone)
        klondiff, ktithiSeq, kpaksha, ktithi , ktithiEndDate, kslat, kslon, kmlat, kmlon = kshyaTithi(ksunrise, 360 )
        ktithiEndLocal = ktithiEndDate.astimezone(istZone)
        timeAfterSunrise = ktithiEndLocal.timestamp() - ksunriseLocal.timestamp()
        
        tithiDurationSec = ktithiEndLocal.timestamp() - tStartTimeStamp
        
        tStartTimeStamp = ktithiEndLocal.timestamp() 
               
        insertRow(conn,seq,ktithiSeq,kpaksha,ktithi,ksunriseLocal,
           ksunriseLocal.year,
           ksunriseLocal.month,
           ksunriseLocal.day,
           ksunriseLocal.hour,
           ksunriseLocal.minute,
           ksunriseLocal.second,  
           ktithiEndLocal,     
           "Y",
           ktithiEndLocal.year,
           ktithiEndLocal.month,
           ktithiEndLocal.day,
           ktithiEndLocal.hour,
           ktithiEndLocal.minute,
           ktithiEndLocal.second,   
           timeAfterSunrise,
           tithiDurationSec,
           convert(tithiDurationSec),
           kslat, 
           kslon, 
           kmlat, 
           kmlon )
        
        seq = seq+1        
        
    print("Seq",seq, " of " , totalTithi)

    lonDiffRef = lonDiff
            
    tithiEndLocal = tithiEndDate.astimezone(istZone)
    
    timeAfterSunrise = tithiEndLocal.timestamp() - sunriseLocal.timestamp()
    
    tithiDurationSec = tithiEndLocal.timestamp() - tStartTimeStamp
    
    tStartTimeStamp = tithiEndLocal.timestamp()     
    
    insertRow(conn,seq,tithiSeq,paksha,tithi,sunriseLocal,
          
           sunriseLocal.year,
           sunriseLocal.month,
           sunriseLocal.day,
           sunriseLocal.hour,
           sunriseLocal.minute,
           sunriseLocal.second,
           tithiEndLocal ,       
           "N",
           tithiEndLocal.year,
           tithiEndLocal.month,
           tithiEndLocal.day,
           tithiEndLocal.hour,
           tithiEndLocal.minute,
           tithiEndLocal.second,
           timeAfterSunrise,
           tithiDurationSec,
           convert(tithiDurationSec),
           slat, 
           slon, 
           mlat, 
           mlon)
        
    currentDate += datetime.timedelta(days=1)

    
    if (lonDiffRef == 360 ) :
        lonDiffRef = 0
