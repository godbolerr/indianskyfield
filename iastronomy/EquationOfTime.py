# Compute equation of time based on the latitude and longitude of the place.
# This is approximate value. Formula is taken from the following source.
from skyfield import api
from skyfield.api import N, E, wgs84, load
from datetime import datetime, timedelta
import numpy as np


# Longitude of the city

cityLon = 74

ts = api.load.timescale()


curDate = ts.utc(2024, 1, 1) 

# Start from 1st Jan and iterate for 366 days


for curDay in range(1, 366, 1):
    
   
    
    B = 360 * ( curDay - 81 )  / 365
    
    B2 = B * 2
    
    # sin(B)
    
    sin_b = np.sin(np.deg2rad(B))
    
    # sin(B2)
    
    sin_2b = np.sin(np.deg2rad(B2))
    
    # COS(B)
    
    cosb = np.cos(np.deg2rad(B))
    
    firstPart = 9.87 * sin_2b
    
    secondPart = -1 * 7.53 * cosb
    
    thirdPart = -1 * 1.15 * sin_b
    
    eotPart = firstPart + secondPart + thirdPart
    
    # LSoT = LST + 4 minutes * (LL - LSTM) + ET
    
    lonAdjustMent = 4 * ( cityLon - 82.56 )
    
    eot = eotPart + lonAdjustMent
    
    curDate = curDate + timedelta(days=1)
    
    print(curDay , curDate.utc_datetime() , eot,sep=",")
    
    