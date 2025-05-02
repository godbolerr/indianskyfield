# Find position and time values of the Sirius star over a year.


from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, E, wgs84, load
import datetime
from skyfield.api import Star, load
from skyfield.data import hipparcos
from skyfield.searchlib import find_discrete


ts = api.load.timescale()
ist = timezone('Asia/Kolkata')

eph = load('../de431t.bsp')


loc_18_73 = wgs84.latlon(18.5204 * N, 73.8567 * E)

loc_18_0  = wgs84.latlon(0 * N, 73.8567 * E)

earth = eph['earth']

loc_18_observer = earth + loc_18_73 

loc_0_observer = eph['Earth'] + loc_18_0

observer = loc_18_observer

ist = timezone('Asia/Kolkata')

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)


stars = [["Sirius","32349","Vyadh"],
         ["Canopus","30438","Agastya"],
         ["Aplha Centauri","71681","Mitra"],
         ["Arcturus","69673","Swati"],
         ["Vega","91262","Abhijit"],
         ["Capella","24608","Brahmahriday"],
         ["Rigel","24436","Rajanya"],
         ["Procyon","37279","Prashwa"],
         ["Betelgeuse","27989","Mrug"],
         ["Achernar","7588","Achernar"] 
        ]

latitudes = [ 0, 15,30,45,60,75]
longitude = 73


latValue = loc_18_73.latitude.degrees
longValue = loc_18_73.longitude.degrees

header = "seq,latitude,longitude,starName,Hip code, mode, IST time, status, ra,dec,alt,az"

for i in range(len(stars)):

    print(stars[i][0],stars[i][1],stars[i][2])
    
   
    starName = stars[i][0]
    
    starHip = int(stars[i][1])
    
    star = Star.from_dataframe(df.loc[starHip])

    t0 = ts.utc(2015, 1, 1,0,0,0)
    
    ra,dec,distance = observer.at(t0).observe(star).apparent().radec()

    # Find values at one constant time
    
    csvFileName = stars[i][0] + "_" + stars[i][1]  + "_midnight.csv"
    
    dataFile = open(csvFileName, 'w')
    
    print(header,file=dataFile)
    
    
    
    for curYear in range(1, 365 , 1):
       
        t1 = t0 + datetime.timedelta(days=1)
        
        
        
        raStar,decStar,distance = observer.at(t1).observe(star).apparent().radec()
        altStar,azStar,distance = observer.at(t1).observe(star).apparent().altaz()
            
        observerTime = t1.astimezone(ist).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        print('0,{}, {} ,{}, HIP{}, {}, {}, {}, {:.4f}, {:.4f}, {:.4f}, {:.4f}'.format(latValue,longValue,starName,starHip,"Instance",t1.astimezone(ist).strftime("%Y-%m-%dT%H:%M:%SZ"), "T",raStar.degrees,decStar.degrees,altStar.degrees,azStar.degrees),file=dataFile)
    
        t0=t1
        
        #print(observerTime,raStar.degrees,decStar.degrees,altStar.degrees,azStar.degrees, sep=",")
    dataFile.close() 
    
    csvFileName = stars[i][0] + "_" + stars[i][1]  + "_riseSetTransit.csv"
    
    dataFile = open(csvFileName, 'w')
    
    print(header,file=dataFile)
    
    
    # Find these values for different latitudes and same longitudes
    
    
    for l in range(len(latitudes)):
        
        latValue = latitudes[l]
    
        location  = wgs84.latlon(latValue * N, 73.8567 * E)
    
        observer = eph['Earth'] + location
    
        latValue = location.latitude.degrees
        
        longValue = location.longitude.degrees
        
    # Find values at rise
        
        t0 = ts.utc(2025, 1, 1)
        t1 = ts.utc(2026, 1, 1)
        
        t, y = almanac.find_risings(observer, star, t0, t1)
        raStar,decStar,distance = observer.at(t).observe(star).apparent().radec()
        altStar,azStar,distance = observer.at(t).observe(star).apparent().altaz()
        
        # Find values at rise
        count = 0
        for ti, yi, rai,deci,alti,azi in zip(t, y, raStar.degrees, decStar.degrees,altStar.degrees,azStar.degrees):
            count = count + 1
            print('{}, {},{},{}, HIP{}, {}, {}, {:5}, {:.4f}, {:.4f}, {:.4f}, {:.4f}'.format(count, latValue,longValue,starName,starHip,"Rise",ti.astimezone(ist).strftime("%Y-%m-%dT%H:%M:%SZ"), str(yi), rai,deci,alti,azi),file=dataFile)
        
        # Find values at set
        
        t, y = almanac.find_settings(observer, star, t0, t1)
        raStar,decStar,distance = observer.at(t).observe(star).apparent().radec()
        altStar,azStar,distance = observer.at(t).observe(star).apparent().altaz()
        
        count = 0
        for ti, yi, rai,deci,alti,azi in zip(t, y, raStar.degrees, decStar.degrees,altStar.degrees,azStar.degrees):
            count = count + 1
            print('{},{},{},{}, HIP{}, {}, {}, {:5}, {:.4f}, {:.4f}, {:.4f}, {:.4f}'.format(count,latValue,longValue,starName,starHip,"Set",ti.astimezone(ist).strftime("%Y-%m-%dT%H:%M:%SZ"), str(yi), rai,deci,alti,azi),file=dataFile)
        
        # Find values at transit
         
        t = almanac.find_transits(observer, star, t0, t1)
        raStar,decStar,distance = observer.at(t).observe(star).apparent().radec()
        altStar,azStar,distance = observer.at(t).observe(star).apparent().altaz()
        
        count = 0
        for ti, rai,deci,alti,azi in zip(t, raStar.degrees, decStar.degrees,altStar.degrees,azStar.degrees):
            count = count + 1
            print('{},{},{},{}, HIP{}, {}, {}, {}, {:.4f}, {:.4f}, {:.4f}, {:.4f}'.format(count,latValue,longValue,starName,starHip,"Transit",ti.astimezone(ist).strftime("%Y-%m-%dT%H:%M:%SZ"),"T", rai,deci,alti,azi),file=dataFile)


    dataFile.close()

