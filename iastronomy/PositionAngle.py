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
import datetime as dt
from skyfield.trigonometry import position_angle_of


# –13200 to 17191
# #################### Constants ########################

ts = api.load.timescale()
istZone = timezone('Asia/Kolkata')
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
pune = wgs84.latlon(18.5204 * N, 73.8567 * E)
puneObserver = eph['Earth'] + pune

# ################## Change start year ##################

moonPhase = 0
counter = 0
prevNewMoon = 0;

ist = timezone('Asia/Kolkata')
now = ist.localize(dt.datetime.now())
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
next_midnight = midnight + dt.timedelta(days=1)

t0 = ts.from_datetime(midnight)
t1 = ts.from_datetime(next_midnight)

# Find phase of moon at midnight

t = ts.utc(2009, 7, 22, 0,38)

dt1 = t.astimezone(pytz.timezone("Asia/Kolkata"))
b = puneObserver.at(t)
m = b.observe(moon).apparent()
s = b.observe(sun).apparent()

print(dt1,position_angle_of(m.altaz(), s.altaz()),sep="  :  ")
    
  










